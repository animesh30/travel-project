from typing import Dict, List

class Graph:
    def __init__(self):
        self.edges: Dict[str, List[dict]] = {}

    def add_edge(self, source: str, edge: dict):
        if source not in self.edges:
            self.edges[source] = []
        self.edges[source].append(edge)

    def neighbors(self, source: str) -> List[dict]:
        return self.edges.get(source, [])
