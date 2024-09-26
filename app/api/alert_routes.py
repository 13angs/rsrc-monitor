from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.models.success_response import SuccessResponse
from app.services.alert_service import AlertService
from app.errors.handlers import error_types

# Initialize the router
router = APIRouter()

# Initialize the alert service
alert_service = AlertService()


@router.get('/alert/fuel')
async def send_fuel_alert():
    """Endpoint to send a fuel price alert via Telegram"""
    try:
        # Run the async fuel alert service
        await alert_service.send_fuel_price_alert()
        return SuccessResponse(status=200, message="Fuel price alert sent!")
    except Exception as e:
        return JSONResponse(status_code=error_types['internal_server']['status'], content=f"Error sending alert: {str(e)}")