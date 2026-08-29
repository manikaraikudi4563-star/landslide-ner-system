from fastapi import APIRouter, Query
from typing import Optional
from app.services.infrastructure_service import infrastructure_service

router = APIRouter(tags=["Infrastructure"])

@router.get("/api/infrastructure")
async def get_infrastructure(
    state: Optional[str] = Query(None, description="Filter by NER State"),
    lat: Optional[float] = Query(None, ge=20.0, le=32.0),
    lng: Optional[float] = Query(None, ge=85.0, le=100.0),
    radius_km: float = Query(15.0, ge=1.0, le=100.0)
):
    if lat is not None and lng is not None:
        return infrastructure_service.evaluate_impact_around_zone(lat, lng, radius_km)
    return infrastructure_service.get_all_infrastructure(state)
