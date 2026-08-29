from fastapi import APIRouter, Query
from typing import Optional
from app.database import get_weather_for_state

router = APIRouter(tags=["Weather Telemetry"])

@router.get("/api/weather")
async def get_weather(state: Optional[str] = Query("Manipur", description="Target NER State")):
    weather = get_weather_for_state(state)
    if not weather:
        weather = {
            "state": state,
            "temp_c": 22.5,
            "rainfall_current": 18.0,
            "rainfall_1h": 6.5,
            "rainfall_6h": 24.0,
            "rainfall_24h": 52.0,
            "forecast_rain_24h": 75.0,
            "condition": "Continuous Monsoon Rain",
            "trend": "Increasing",
            "is_demo": True
        }
    return weather
