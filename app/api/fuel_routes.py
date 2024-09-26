# app/api/routes.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.errors.handlers import DatabaseException, error_types
from app.errors.models import ErrorDetails
from app.models.success_response import SuccessResponse
from app.services.fuel_service import FuelDataService

# Initialize router
router = APIRouter()

# Initialize the fuel service
fuel_service = FuelDataService()


@router.get("/scrape/fuel")
async def scrape_all_fuel():
    """Endpoint to scrape data from all fuel providers"""
    try:

        fuel_service.run()
        return SuccessResponse(status=200, message=f"Fuel data inserted successfully.")
    except DatabaseException as e:
        error_response = ErrorDetails(
            type=e.error_type,
            message=e.message,
            status=404
        )
        return JSONResponse(status_code=error_types['conflict']['status'], content=error_response.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
