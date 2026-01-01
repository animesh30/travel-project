from fastapi import FastAPI
from typing import List
from fastapi.middleware.cors import CORSMiddleware


from my_providers.mock_transport_providers import MockTransportProvider
from my_models.schemas import SearchRequest, ItineraryResponse

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


@app.post("/search", response_model=List[ItineraryResponse])
async def search_routes(request: SearchRequest):
    """
    Entry point for UI.
    Example:
    Source: A
    Destination: C
    """

    source = request.source
    destination = request.destination

    itineraries = []

    # Direct options
    direct_options = await provider.get_options(source, destination)

    for option in direct_options:
        itineraries.append(
            ItineraryResponse(
                legs=[option],
                total_price=option.price,
                total_duration_min=option.duration_min,
                all_legs_available=option.available
            )
        )

    # Example: A → B → C (hardcoded for MVP)
    if source == "A" and destination == "C":
        ab = await provider.get_options("A", "B")
        bc = await provider.get_options("B", "C")

        for leg1 in ab:
            if not leg1.available:
                continue
            for leg2 in bc:
                if not leg2.available:
                    continue

                itineraries.append(
                    ItineraryResponse(
                        legs=[leg1, leg2],
                        total_price=leg1.price + leg2.price,
                        total_duration_min=leg1.duration_min + leg2.duration_min,
                        all_legs_available=True
                    )
                )

    return itineraries

