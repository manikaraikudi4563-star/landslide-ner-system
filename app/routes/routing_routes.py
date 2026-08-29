from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from app.services.routing_service import routing_service

router = APIRouter(tags=["Evacuation & Safe Routing"])

class EvacuationPlanRequest(BaseModel):
    latitude: float = Field(..., ge=20.0, le=32.0)
    longitude: float = Field(..., ge=85.0, le=100.0)
    shelter_id: Optional[str] = Field(None, description="Optional target shelter ID")

@router.post("/api/evacuation/plan")
async def plan_evacuation_route(req: EvacuationPlanRequest):
    routes = routing_service.find_nearest_shelters(
        origin_lat=req.latitude,
        origin_lng=req.longitude,
        limit=3,
        target_shelter_id=req.shelter_id
    )
    return {
        "origin": {"lat": req.latitude, "lng": req.longitude},
        "target_shelter_id": req.shelter_id,
        "recommended_routes": routes,
        "is_demo": True
    }

@router.get("/api/routes/recommended")
async def get_recommended_route(origin_lat: float = Query(..., ge=20.0, le=32.0), origin_lng: float = Query(..., ge=85.0, le=100.0), shelter_id: Optional[str] = Query(None)):
    routes = routing_service.find_nearest_shelters(
        origin_lat=origin_lat,
        origin_lng=origin_lng,
        limit=1,
        target_shelter_id=shelter_id
    )
    if not routes:
        raise HTTPException(status_code=404, detail="No suitable evacuation route could be calculated")
    return routes[0]
