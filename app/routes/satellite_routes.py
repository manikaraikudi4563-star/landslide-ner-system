from fastapi import APIRouter
from app.services.satellite_service import satellite_service

router = APIRouter(tags=["Satellite Change Detection"])

@router.get("/api/satellite/changes")
async def get_satellite_changes():
    return satellite_service.get_change_records()
