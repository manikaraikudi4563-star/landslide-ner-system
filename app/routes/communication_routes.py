from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from app.services.communication_service import communication_service

router = APIRouter(tags=["Offline Emergency Communication"])

class TestAlertQueueRequest(BaseModel):
    alert_id: Optional[str] = Field(None)
    location: str = Field("Noney Sector")
    headline: str = Field("TEST EMERGENCY ALARM")

@router.get("/api/communication/status")
async def get_communication_status():
    return communication_service.get_queue_status()

@router.post("/api/communication/sync")
async def sync_communication_queue():
    return communication_service.sync_queue()

@router.post("/api/communication/toggle-network")
async def toggle_network_status():
    return communication_service.toggle_network()

@router.post("/api/communication/test")
async def queue_test_emergency_alert(req: TestAlertQueueRequest):
    return communication_service.queue_test_alert(
        alert_id=req.alert_id,
        location=req.location,
        headline=req.headline
    )
