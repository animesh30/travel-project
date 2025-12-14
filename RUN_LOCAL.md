# Running the Project with Flask

This project now includes a minimal Flask web server in `app.py` that exposes the route engine via an HTTP endpoint. You can run and interact with the project locally as follows:

## Prerequisites
- Python 3.x
- Flask (install with `pip install flask`)

## How to Run
1. **Install Flask** (if not already installed):
   ```bash
   pip install flask
   ```
2. **Start the server**:
   ```bash
   python app.py
   ```
   The server will start at `http://127.0.0.1:5000/` by default.

3. **Query for routes**:
   Open your browser or use `curl`/Postman to access:
   ```
   http://127.0.0.1:5000/routes?src=A&dst=C&max_intermediate=2&top_k=5
   ```
   - `src`: Source node code (default: A)
   - `dst`: Destination node code (default: C)
   - `max_intermediate`: Max intermediate stops (default: 2)
   - `top_k`: Number of top routes to return (default: 10)

4. **Response**:
   The endpoint returns a JSON object with the best candidate routes and their details.

## Example
```
GET http://127.0.0.1:5000/routes?src=A&dst=C
```
Response:
```json
{
  "routes": [
    {
      "score": 2250.0,
      "legs": [
        "A->D(flight, 400 km, 60 min, ₹2000, avail=True)",
        "D->C(train, 300 km, 200 min, ₹600, avail=True)"
      ],
      "total_distance_km": 700.0,
      "total_duration_min": 260,
      "total_price": 2600.0,
      "transfers": 1,
      "all_legs_available": true,
      "legs_info": [ ... ]
    },
    ...
  ]
}
```

## Notes
- The graph and data are mocked for demonstration.
- For production, replace the demo graph with real data sources.

