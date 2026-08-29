from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.services.routing_service import routing_service

router = APIRouter(tags=["Shelters"])

@router.get("/api/shelters")
async def get_shelters(state: Optional[str] = Query(None, description="Filter shelters by NER state")):
    shelters = routing_service.get_all_shelters()
    if state and state.upper() != "ALL":
        return [s for s in shelters if s.get("state", "").lower() == state.lower()]
    return shelters

@router.get("/api/shelters/nearest")
async def get_nearest_shelter(lat: float = Query(..., ge=20.0, le=32.0), lng: float = Query(..., ge=85.0, le=100.0)):
    routes = routing_service.find_nearest_shelters(lat, lng, limit=1)
    if not routes:
        raise HTTPException(status_code=404, detail="No available shelters found in radius")
    return routes[0]

@router.get("/api/shelters/recommend")
async def recommend_smart_shelters(lat: float = Query(..., ge=20.0, le=32.0), lng: float = Query(..., ge=85.0, le=100.0), limit: int = Query(4, ge=1, le=10)):
    return routing_service.recommend_smart_shelters(lat, lng, limit=limit)

@router.get("/api/shelters/{shelter_id}")
async def get_shelter_detail(shelter_id: str):
    shelter = routing_service.get_shelter_by_id(shelter_id)
    if not shelter:
        raise HTTPException(status_code=404, detail=f"Shelter '{shelter_id}' not found")
    return shelter
