
from my_models.schemas import TransportLeg

class MockTransportProvider:
    async def get_options(self, source: str, destination: str):
        # Return a dummy list of TransportLeg objects for demo purposes
        return [
            TransportLeg(
                source=source,
                destination=destination,
                mode="bus",
                price=100.0,
                duration_min=120,
                available=True
            )
        ]
