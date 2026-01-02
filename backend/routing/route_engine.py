# Python code to generate candidate routes (A → ... → C via intermediate nodes)
# using a transit hub graph. This is a self-contained demo suitable for an MVP route
# generation engine. It enumerates simple paths up to a given maximum number of intermediate stops,
# prunes unrealistic detours using a detour factor, and scores routes by availability of legs,
# total cost and total duration (mocked here).
#
# Run in this notebook; results will be printed below and shown to the user.
#
# Note: In a real system you'd replace mocked availability/prices/durations with real provider data.

from typing import Dict, List, Tuple, Any
import math
import heapq
import pprint

from typing import List, Dict
from routing.graph import Graph

# Data structures
class Node:
    def __init__(self, code: str, name: str, lat: float, lon: float):
        self.code = code
        self.name = name
        self.lat = lat
        self.lon = lon
    def __repr__(self):
        return f"{self.code}"

class Edge:
    def __init__(self, src: str, dst: str, mode: str, distance_km: float, duration_min: int, price: float, availability: bool=True):
        self.src = src
        self.dst = dst
        self.mode = mode  # train / bus / flight / rideshare etc.
        self.distance_km = distance_km
        self.duration_min = duration_min
        self.price = price
        self.availability = availability
    def __repr__(self):
        return f"{self.src}->{self.dst}({self.mode}, {self.distance_km} km, {self.duration_min} min, ₹{self.price}, avail={self.availability})"

class Graph:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.adj: Dict[str, List[Edge]] = {}
    def add_node(self, node: Node):
        self.nodes[node.code] = node
        self.adj.setdefault(node.code, [])
    def add_edge(self, edge: Edge):
        if edge.src not in self.nodes or edge.dst not in self.nodes:
            raise ValueError("Nodes must be added before adding edges")
        self.adj[edge.src].append(edge)
    def neighbors(self, node_code: str) -> List[Edge]:
        return self.adj.get(node_code, [])

# Utilities
def euclidean_km(a: Node, b: Node) -> float:
    # approximate by equirectangular projection (good for short distances)
    R = 6371.0  # earth radius km
    lat1 = math.radians(a.lat); lat2 = math.radians(b.lat)
    lon1 = math.radians(a.lon); lon2 = math.radians(b.lon)
    x = (lon2 - lon1) * math.cos((lat1 + lat2) / 2.0)
    y = (lat2 - lat1)
    d = math.sqrt(x*x + y*y) * R
    return d

# Path enumeration (DFS) with pruning
def enumerate_paths(graph: Graph, src: str, dst: str, max_intermediate: int, max_total_distance_km: float=None) -> List[List[Edge]]:
    max_depth = max_intermediate + 1  # number of edges allowed
    results = []
    visited = set()

    # Precompute direct euclidean distance for detour pruning
    direct_dist = euclidean_km(graph.nodes[src], graph.nodes[dst])

    def dfs(current: str, path_edges: List[Edge]):
        # Check depth
        if len(path_edges) > max_depth:
            return
        # If reached destination, collect path
        if current == dst and 0 < len(path_edges) <= max_depth:
            # compute path distance
            total_dist = sum(e.distance_km for e in path_edges)
            # optional global distance limit
            if max_total_distance_km is not None and total_dist > max_total_distance_km:
                return
            results.append(list(path_edges))
            return
        # Avoid cycles: disallow revisiting nodes already in path
        visited_nodes = {edge.src for edge in path_edges} | {edge.dst for edge in path_edges}
        visited_nodes.add(src)  # ensure source treated as visited
        for edge in graph.neighbors(current):
            if edge.dst in visited_nodes:
                continue  # prevent cycles
            # Detour pruning: if path-so-far distance plus this edge exceeds a reasonable multiple of direct distance
            path_dist_so_far = sum(e.distance_km for e in path_edges) + edge.distance_km
            detour_factor = path_dist_so_far / (direct_dist + 1e-6)
            # Reject paths that are super detours (configurable threshold)
            if detour_factor > 2.0:
                continue
            # proceed
            path_edges.append(edge)
            dfs(edge.dst, path_edges)
            path_edges.pop()

    dfs(src, [])
    return results

# Compute metrics & scoring
def compute_path_metrics(path: List[Edge]) -> Dict[str, Any]:
    total_distance = sum(e.distance_km for e in path)
    total_duration = sum(e.duration_min for e in path)
    total_price = sum(e.price for e in path)
    transfers = max(0, len(path)-1)
    # availability rule: itinerary is feasible if ALL legs have availability True OR at least one confirmed leg? 
    # For MVP we'll mark as 'confirmed' only if all legs available; otherwise 'partial'.
    all_available = all(e.availability for e in path)
    legs_info = [(e.src, e.dst, e.mode, e.duration_min, e.price, e.availability) for e in path]
    return {
        "legs": path,
        "total_distance_km": total_distance,
        "total_duration_min": total_duration,
        "total_price": total_price,
        "transfers": transfers,
        "all_legs_available": all_available,
        "legs_info": legs_info
    }

def score_path(metrics: Dict[str, Any]) -> float:
    # Lower score is better. Combine availability, price, duration, transfers.
    score = 0.0
    # Big penalty if not all legs available
    if not metrics["all_legs_available"]:
        score += 10000
    # price weight
    score += metrics["total_price"] * 1.0
    # time weight (per hour)
    score += (metrics["total_duration_min"] / 60.0) * 50.0
    # transfer penalty
    score += metrics["transfers"] * 200.0
    # small distance addition
    score += metrics["total_distance_km"] * 0.1
    return score

def generate_candidate_routes(graph: Graph, src: str, dst: str, max_intermediate: int=2, top_k:int=10, max_total_distance_km:float=None):
    raw_paths = enumerate_paths(graph, src, dst, max_intermediate, max_total_distance_km)
    scored = []
    for p in raw_paths:
        m = compute_path_metrics(p)
        s = score_path(m)
        scored.append((s, m))
    # sort by score ascending
    scored.sort(key=lambda x: x[0])
    # package results
    results = []
    for score_val, metrics in scored[:top_k]:
        results.append({"score": score_val, **metrics})
    return results

# --- Example demo graph ---
g = Graph()
# Add nodes with mock coordinates (lat, lon)
g.add_node(Node("A","Alpha",17.3850,78.4867))
g.add_node(Node("B","Beta",17.6868,83.2185))
g.add_node(Node("C","Gamma",17.4474,78.3762))
g.add_node(Node("D","Delta",16.5062,80.6480))
g.add_node(Node("E","Epsilon",19.07598,72.87766))

# Add edges (bidirectional where appropriate)
edges = [
    Edge("A","B","train",350,240,500, availability=True),
    Edge("B","A","train",350,240,500, availability=True),
    Edge("A","C","bus",40,60,150, availability=False),  # direct but unavailable
    Edge("C","A","bus",40,60,150, availability=False),
    Edge("B","C","bus",200,180,300, availability=True),
    Edge("C","B","bus",200,180,300, availability=True),
    Edge("A","D","flight",400,60,2000, availability=True),
    Edge("D","C","train",300,200,600, availability=True),
    Edge("A","E","train",700,480,800, availability=True),
    Edge("E","C","flight",900,90,2500, availability=False),
    Edge("B","D","bus",220,180,350, availability=True),
    Edge("D","B","bus",220,180,350, availability=True),
]
for e in edges:
    g.add_edge(e)

class RouteEngine:
    def __init__(self, graph: Graph):
        self.graph = graph

    def find_routes(self, source: str, destination: str, max_hops: int = 2):
        results = []

        def dfs(current, path, cost, duration):
            if len(path) > max_hops + 1:
                return

            if current == destination:
                results.append({
                    "path": path.copy(),
                    "total_price": cost,
                    "total_duration": duration
                })
                return

            for edge in self.graph.neighbors(current):
                if edge["to"] in path:
                    continue
                if not edge["available"]:
                    continue

                dfs(
                    edge["to"],
                    path + [edge["to"]],
                    cost + edge["price"],
                    duration + edge["duration"]
                )

        dfs(source, [source], 0, 0)
        return results



