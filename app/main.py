# app/main.py

from fastapi import FastAPI
from app.api.routes import router as fuel_router

# Initialize the FastAPI app
app = FastAPI()

# Include routes for fuel scraping
app.include_router(fuel_router, prefix="/api", tags=["Fuel Scraper"])

@app.get("/")
async def root():
    return {"message": "Fuel Scraper API is running!"}
