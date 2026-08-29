from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from app.database import add_citizen_report, get_all_reports

router = APIRouter(tags=["Incident Reporting"])

class CitizenReportRequest(BaseModel):
    reporter_name: str = Field(..., description="Name of citizen or field observer")
    contact_number: Optional[str] = Field("", description="Phone number")
    state: str = Field(..., description="NER State")
    location_name: str = Field(..., description="Specific landmark or road marker")
    latitude: float = Field(..., ge=20.0, le=32.0)
    longitude: float = Field(..., ge=85.0, le=100.0)
    landslide_type: str = Field("Debris Slide", description="Type of landslide")
    estimated_size: str = Field("Medium", description="Small, Medium, Large, Catastrophic")
    road_blocked: bool = Field(False)
    casualties_reported: int = Field(0, ge=0)
    description: Optional[str] = Field("")
    image_url: Optional[str] = Field("")

@router.post("/api/incidents", status_code=status.HTTP_201_CREATED)
@router.post("/api/reports", status_code=status.HTTP_201_CREATED)
async def submit_incident_report(req: CitizenReportRequest):
    report_id = add_citizen_report(req.dict())
    return {
        "status": "SUCCESS",
        "submission_status": "SUBMITTED",
        "report_id": report_id,
        "message": f"Incident report {report_id} has been logged and forwarded to District Disaster Command."
    }

@router.get("/api/incidents")
@router.get("/api/reports")
async def list_incident_reports():
    return get_all_reports()
