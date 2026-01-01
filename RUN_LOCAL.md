
# Running the Project Locally (FastAPI + React)

This project uses a FastAPI backend and a React (Vite) frontend. Follow these steps to run both locally:

## Prerequisites
- Python 3.x
- Node.js and npm (https://nodejs.org/)

## Backend (API)
1. Open a terminal and navigate to the backend root (project root):
  ```bash
  cd /Users/animeshgupta/travel-project
  ```
2. Install dependencies:
  ```bash
  python3 -m pip install fastapi uvicorn
  ```
3. Start the FastAPI server:
  ```bash
  PYTHONPATH=. python3 -m uvicorn app:app --reload
  ```
  The server will start at `http://127.0.0.1:8000/` by default.

## Frontend (UI)
1. Open a new terminal and navigate to the frontend directory:
  ```bash
  cd /Users/animeshgupta/travel-project/frontend
  ```
2. Install dependencies:
  ```bash
  npm install
  ```
3. Start the React development server:
  ```bash
  npm run dev
  ```
  The frontend will start at `http://localhost:5173/` (or similar, see terminal output).

## Usage
- Open the frontend in your browser and enter a source and destination (e.g., A and C) to search for routes.
- The frontend will call the backend API at `http://localhost:8000/search`.

## Example API Request
POST to `http://localhost:8000/search` with JSON body:
```json
{
  "source": "A",
  "destination": "C"
}
```

## Notes
- The graph and data are mocked for demonstration.
- For production, replace the demo graph with real data sources and secure the API as needed.

