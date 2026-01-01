
# Travel Route Engine (Full Stack)

This project is a minimal viable product (MVP) for a travel route generation engine with a FastAPI backend and a React (Vite) frontend. It computes candidate travel itineraries between two locations using a transit hub graph and demonstrates how to enumerate, score, and present possible routes using mocked data.

## Features
- **Graph-based route generation**: Nodes represent locations, edges represent travel legs (train, bus, flight, etc.).
- **Path enumeration**: Finds all simple paths between source and destination up to a configurable number of intermediate stops.
- **Detour pruning**: Discards routes that are excessively circuitous using a detour factor.
- **Route scoring**: Ranks routes by availability, price, duration, and number of transfers.
- **Mock data**: Uses hardcoded nodes and edges for demonstration.
- **REST API**: FastAPI backend exposes endpoints for route search.
- **Modern UI**: React frontend for user-friendly search and results display.

## How It Works
- The backend builds a graph of locations and possible travel legs.
- It enumerates all feasible paths from a source to a destination, subject to constraints (max stops, detour factor).
- Each route is scored based on leg availability, total price, total duration, and number of transfers.
- The frontend allows users to search for routes and displays the best options.

## Usage
See `RUN_LOCAL.md` for detailed setup and run instructions for both backend and frontend.

## Customization
- To change the graph, edit the backend logic in the relevant provider or engine files.
- Adjust detour or intermediate stop constraints in the backend.
- Replace mocked data with real provider data for production use.

## Example API Output
```
POST /search {"source": "A", "destination": "C"}

[
   {
      "legs": [
         {"source": "A", "destination": "B", "mode": "bus", "price": 100, "duration_min": 120, "available": true}
      ],
      "total_price": 100,
      "total_duration_min": 120,
      "all_legs_available": true
   }
]
```

## License
This project is provided as a demonstration and is not intended for production use. No warranty is provided.
