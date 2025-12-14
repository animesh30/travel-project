

# Ensure local imports work

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'routing'))

# Minimal Flask app to expose route engine via HTTP
from flask import Flask, jsonify, request
from route_engine import Graph, Node, Edge, generate_candidate_routes

app = Flask(__name__)

# Demo graph setup (same as in route_engine.py)
def build_demo_graph():
    g = Graph()
    g.add_node(Node("A","Alpha",17.3850,78.4867))
    g.add_node(Node("B","Beta",17.6868,83.2185))
    g.add_node(Node("C","Gamma",17.4474,78.3762))
    g.add_node(Node("D","Delta",16.5062,80.6480))
    g.add_node(Node("E","Epsilon",19.07598,72.87766))
    edges = [
        Edge("A","B","train",350,240,500, availability=True),
        Edge("B","A","train",350,240,500, availability=True),
        Edge("A","C","bus",40,60,150, availability=False),
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
    return g

@app.route("/routes", methods=["GET"])
def get_routes():
    src = request.args.get("src", "A")
    dst = request.args.get("dst", "C")
    max_intermediate = int(request.args.get("max_intermediate", 2))
    top_k = int(request.args.get("top_k", 10))
    g = build_demo_graph()
    candidates = generate_candidate_routes(g, src, dst, max_intermediate, top_k)
    # Convert objects to serializable form
    for c in candidates:
        c["legs"] = [str(leg) for leg in c["legs"]]
    return jsonify({"routes": candidates})

if __name__ == "__main__":
    app.run(debug=True)
# app.py

from mock_transport_providers import MockTransportProvider
from typing import List


class TripPlannerApp:

    def __init__(self):
        self.provider = MockTransportProvider()

        # Hardcoded hubs for MVP
        self.hubs = ["B", "D", "E"]

    def find_routes(self, source: str, destination: str):
        """
        Finds direct and one-stop routes between source and destination.
        """
        results = []

        # ---- Direct Route ----
        direct_options = self.provider.get_options(source, destination)
        for option in direct_options:
            if option.available:
                results.append({
                    "route": f"{source} → {destination}",
                    "legs": [option],
                    "total_price": option.price,
                    "total_duration": option.duration_min
                })

        # ---- One-stop Routes ----
        for hub in self.hubs:
            if hub in (source, destination):
                continue

            first_legs = self.provider.get_options(source, hub)
            second_legs = self.provider.get_options(hub, destination)

            for leg1 in first_legs:
                if not leg1.available:
                    continue

                for leg2 in second_legs:
                    if not leg2.available:
                        continue

                    results.append({
                        "route": f"{source} → {hub} → {destination}",
                        "legs": [leg1, leg2],
                        "total_price": leg1.price + leg2.price,
                        "total_duration": leg1.duration_min + leg2.duration_min
                    })

        return results


if __name__ == "__main__":
    app = TripPlannerApp()

    source = "A"
    destination = "C"

    routes = app.find_routes(source, destination)

    if not routes:
        print("No feasible routes found 😕")
    else:
        print(f"Found {len(routes)} feasible routes:\n")
        for idx, route in enumerate(routes, start=1):
            print(f"Route #{idx}: {route['route']}")
            for leg in route["legs"]:
                print(
                    f"  {leg.mode.upper()} | {leg.source} → {leg.destination} "
                    f"| {leg.duration_min} min | ₹{leg.price}"
                )
            print(
                f"  TOTAL: ₹{route['total_price']} | {route['total_duration']} min\n"
            )
