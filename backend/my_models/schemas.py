from pydantic import BaseModel
from typing import List


class SearchRequest(BaseModel):
    source: str
    destination: str


class TransportLeg(BaseModel):
    source: str
    destination: str
    mode: str
    duration_min: int
    price: float
    available: bool


class ItineraryResponse(BaseModel):
    legs: List[TransportLeg]
    total_price: float
    total_duration_min: int
    all_legs_available: bool

class SearchResponse(BaseModel):
    path: List[str]
    total_price: int
    total_duration: int

