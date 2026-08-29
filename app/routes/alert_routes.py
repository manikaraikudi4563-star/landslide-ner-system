from fastapi import APIRouter, HTTPException, Query, Response, status
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from app.services.alert_service import alert_service
from app.database import insert_alert
from app.data.alert_translations import get_translated_alert
from app.data.ner_geospatial import CHRONOLOGICAL_ALERT_TIMELINE

router = APIRouter(tags=["Alerts & Early Warnings"])

class CreateAlertRequest(BaseModel):
    station_id: Optional[str] = Field("STN-MAN-01", description="Associated monitoring station ID")
    region_name: str = Field(..., description="Region or corridor name")
    state: str = Field("Manipur", description="NER State")
    severity: str = Field("Severe", description="Severity tier: Extreme, Severe, Moderate, Minor")
    event_type: str = Field("Landslide Warning", description="CAP event classification")
    headline: str = Field(..., description="Short urgent headline")
    description: str = Field(..., description="Detailed geotechnical alert explanation")
    instruction: str = Field(..., description="Action directive for civil defense")
    coordinates: Optional[List[float]] = Field([24.7083, 93.6500], description="[lat, lng]")

@router.get("/api/alerts")
async def get_alerts(state: Optional[str] = Query(None, description="Filter alerts by NER state")):
    alerts = alert_service.get_all_active_alerts()
    if state and state.upper() != "ALL":
        return [a for a in alerts if a.get("state", "").lower() == state.lower()]
    return alerts

@router.post("/api/alerts", status_code=status.HTTP_201_CREATED)
async def create_alert(req: CreateAlertRequest):
    alert_id = insert_alert(req.dict())
    return {
        "status": "CREATED",
        "alert_id": alert_id,
        "message": f"Alert {alert_id} successfully logged into CAP feed."
    }

@router.get("/api/alerts/timeline")
async def get_alert_timeline():
    return CHRONOLOGICAL_ALERT_TIMELINE

@router.get("/api/alerts/translations")
async def get_alert_translations(lang: str = Query("en", description="Language code: en, hi, as, mni, lus, kha, nag, bn"), alert_id: Optional[str] = Query(None)):
    alerts = alert_service.get_all_active_alerts()
    matched_alert = next((a for a in alerts if a.get("alert_id") == alert_id), alerts[0] if alerts else {})
    return get_translated_alert(matched_alert, lang)

@router.get("/api/alerts/{alert_id}/cap-xml")
async def get_cap_xml(alert_id: str):
    alerts = alert_service.get_all_active_alerts()
    matched = next((a for a in alerts if a.get("alert_id") == alert_id), None)
    if not matched:
        matched = {
            "alert_id": alert_id,
            "event_type": "Landslide Hazard Alert",
            "severity": "Severe",
            "headline": "Landslide Critical Hazard Notification",
            "description": "Geotechnical sensor threshold breached in NER mountain corridor.",
            "instruction": "Follow official evacuation directions.",
            "region_name": "NER Mountain Corridor",
            "state": "Assam",
            "coordinates": [25.5, 92.5]
        }
    xml_content = alert_service.generate_cap_xml_bulletin(matched)
    return Response(content=xml_content, media_type="application/xml")
