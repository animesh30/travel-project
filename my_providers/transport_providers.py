import asyncio
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class TransportOption:
    source: str
    destination: str
    mode: str          # train / bus / flight
    duration_min: int
    price: float
    available: bool


class MockTransportProvider:
    """
    Simulates external transport providers.
    Later this will be replaced by IRCTC / RedBus / etc.
    """

    async def get_options(
        self,
        source: str,
        destination: str
    ) -> List[TransportOption]:
        # Simulate network latency
        await asyncio.sleep(0.2)

        mock_db: Dict[str, List[TransportOption]] = {
            "A_B": [
                TransportOption("A", "B", "train", 120, 400, True),
                TransportOption("A", "B", "bus", 180, 300, False),
            ],
            "B_C": [
                TransportOption("B", "C", "bus", 150, 250, True),
                TransportOption("B", "C", "train", 130, 350, False),
            ],
            "A_C": [
                TransportOption("A", "C", "bus", 240, 600, False),
                TransportOption("A", "C", "flight", 60, 2500, True),
            ],
        }

        return mock_db.get(f"{source}_{destination}", [])
