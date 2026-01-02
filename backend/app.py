from fastapi import FastAPI, Query
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from routing.graph import Graph
from routing.route_engine import RouteEngine
from my_providers.mock_transport_providers import MockTransportProvider
from my_models.schemas import SearchRequest, ItineraryResponse, SearchResponse

app = FastAPI(
    title="Travel Route Mixer",
    description="Finds mixed-mode travel routes when direct tickets are unavailable",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for MVP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

provider = MockTransportProvider()


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/search", response_model=List[SearchResponse])
async def search(
    source: str = Query(...),
    destination: str = Query(...)
):
    provider = MockTransportProvider()
    graph = Graph()

    # Build graph from mock provider
    connections = await provider.get_connections(source)
    for conn in connections:
        graph.add_edge(source, conn)

    # Add second level connections
    for conn in connections:
        next_connections = await provider.get_connections(conn["to"])
        for nc in next_connections:
            graph.add_edge(conn["to"], nc)

    engine = RouteEngine(graph)
    routes = engine.find_routes(source, destination)

    return routes

