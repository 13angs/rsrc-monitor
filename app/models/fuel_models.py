# app/models/fuel_models.py

from pydantic import BaseModel
from typing import List

class FuelData(BaseModel):
    provider: str
    type: str
    price: float

class AllFuelsResponse(BaseModel):
    data: List[FuelData]
    status: int