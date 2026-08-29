from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.services.telemetry_service import telemetry_service

router = APIRouter(tags=["Monitoring Stations"])

@router.get("/api/stations")
async def get_stations(state: Optional[str] = Query(None, description="Filter by NER State")):
    stations = telemetry_service.get_all_stations()
    if state and state.upper() != "ALL":
        return [s for s in stations if s["state"].lower() == state.lower()]
    return stations

@router.get("/api/stations/{station_id}")
async def get_station_detail(station_id: str):
    detail = telemetry_service.get_station_details(station_id)
    if not detail:
        raise HTTPException(status_code=404, detail=f"Monitoring station '{station_id}' not found")
    return detail
