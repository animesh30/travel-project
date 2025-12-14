# Travel Route Engine

This project is a minimal viable product (MVP) for a route generation engine that computes candidate travel itineraries between two locations using a transit hub graph. It demonstrates how to enumerate, score, and present possible routes using mocked data for availability, price, and duration.

## Features
- **Graph-based route generation**: Nodes represent locations, edges represent travel legs (train, bus, flight, etc.).
- **Path enumeration**: Finds all simple paths between source and destination up to a configurable number of intermediate stops.
- **Detour pruning**: Discards routes that are excessively circuitous using a detour factor.
- **Route scoring**: Ranks routes by availability, price, duration, and number of transfers.
- **Mock data**: Uses hardcoded nodes and edges for demonstration.

## How It Works
- The engine builds a graph of locations and possible travel legs.
- It enumerates all feasible paths from a source to a destination, subject to constraints (max stops, detour factor).
- Each route is scored based on leg availability, total price, total duration, and number of transfers.
- The top candidate routes are printed with details for each leg.

## Usage
1. **Requirements**: Python 3.x (no external dependencies required).
2. **Run the script**:
   ```bash
   python route_engine.py
   ```
3. **Output**: The script prints the top candidate itineraries from node A to C, showing:
   - Each leg (mode, distance, duration, price, availability)
   - Total price, duration, distance, transfers, and availability status

## Customization
- To change the graph, edit the `nodes` and `edges` sections in `route_engine.py`.
- Adjust `max_intermediate` or detour factor in the `generate_candidate_routes` call to control route complexity.
- Replace mocked data with real provider data for production use.

## Example Output
```
Found 3 candidate itineraries. Showing top results:

Itinerary #1 — Score: 2250.0
 Legs:
   A->D(flight, 400 km, 60 min, ₹2000, avail=True)
   D->C(train, 300 km, 200 min, ₹600, avail=True)
 Total price: ₹2600.00, Total duration: 260 min, Distance: 700.0 km, Transfers: 1, All legs available: True
... (other itineraries)
```

## License
This project is provided as a demonstration and is not intended for production use. No warranty is provided.
