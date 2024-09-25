# app/api/routes.py

from fastapi import APIRouter, HTTPException
from app.models.fuel_models import AllFuelsResponse
from app.services.fuel_service import FuelDataService

# Initialize router
router = APIRouter()

# Initialize the fuel service
fuel_service = FuelDataService()

@router.get("/scrape/fuel", response_model=AllFuelsResponse)
async def scrape_all_fuel():
    """Endpoint to scrape data from all fuel providers"""
    try:
        fuel_service.run()
        return AllFuelsResponse(data=[],status=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
