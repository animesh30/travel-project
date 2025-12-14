# mock_transport_providers.py

from dataclasses import dataclass
from typing import List
import random


@dataclass
class TransportOption:
    mode: str            # train / bus
    source: str
    destination: str
    duration_min: int
    price: float
    available: bool


class MockTransportProvider:
    """
    Simulates transport availability between two points.
    """

    def get_options(self, source: str, destination: str) -> List[TransportOption]:
        """
        Returns a list of possible transport options between source and destination.
        """
        options = []

        # ---- TRAIN OPTION ----
        train_available = random.choice([True, False, True])  # higher probability
        options.append(
            TransportOption(
                mode="train",
                source=source,
                destination=destination,
                duration_min=random.randint(120, 360),
                price=random.randint(300, 800),
                available=train_available
            )
        )

        # ---- BUS OPTION ----
        bus_available = random.choice([True, True, False])  # higher probability
        options.append(
            TransportOption(
                mode="bus",
                source=source,
                destination=destination,
                duration_min=random.randint(180, 420),
                price=random.randint(200, 600),
                available=bus_available
            )
        )

        return options
