from fastapi import APIRouter, HTTPException
from app.services.alert_service import AlertService

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
        return {"message": "Fuel price alert sent!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending alert: {str(e)}")