# app/main.py

from fastapi import FastAPI
from app.api.fuel_routes import router as fuel_router
from app.api.alert_routes import router as alert_router

# Initialize the FastAPI app
app = FastAPI()

# Include routes for fuel scraping
app.include_router(fuel_router, prefix="/api", tags=["Fuel Scraper"])
app.include_router(alert_router, prefix="/api", tags=["Fuel Alerts"])

@app.get("/")
async def root():
    return {"message": "Fuel Scraper API is running!"}
