from typing import List, Dict
import asyncio

class MockTransportProvider:
    """
    Simulates train/bus providers.
    """

    async def get_connections(self, source: str) -> List[Dict]:
        await asyncio.sleep(0.1)  # simulate network delay

        connections = {
            "A": [
                {"to": "B", "mode": "train", "price": 500, "duration": 240, "available": True},
                {"to": "C", "mode": "bus", "price": 150, "duration": 60, "available": False},
            ],
            "B": [
                {"to": "C", "mode": "bus", "price": 300, "duration": 180, "available": True},
            ]
        }

        return connections.get(source, [])
