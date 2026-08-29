from fastapi import APIRouter
from app.services.telemetry_service import telemetry_service
from app.services.alert_service import alert_service
from app.services.routing_service import routing_service
from app.database import get_all_reports, get_all_sensor_health
from app.data.ner_geospatial import NER_CORRIDORS, NER_RAILWAYS

router = APIRouter(tags=["Authority Command & Geospatial"])

@router.get("/api/corridors")
async def get_corridors():
    return NER_CORRIDORS

@router.get("/api/railways")
async def get_railways():
    return NER_RAILWAYS

@router.get("/api/authority/summary")
async def get_authority_summary():
    stations = telemetry_service.get_all_stations()
    alerts = alert_service.get_all_active_alerts()
    reports = get_all_reports()
    shelters = routing_service.get_all_shelters()
    health = get_all_sensor_health()

    return {
        "system_status": "OPERATIONAL",
        "command_status": "HIGH ALERT MONITORING",
        "total_active_alerts": len(alerts),
        "critical_emergency_alerts": sum(1 for a in alerts if a.get("severity") in ["Extreme", "Severe", "CRITICAL"]),
        "total_citizen_reports": len(reports),
        "evacuation_readiness": "DEPLOYED",
        "shelters_ready": len(shelters),
        "total_shelter_capacity": sum(s["capacity"] for s in shelters),
        "iot_nodes_operational": sum(1 for h in health if h["status"] == "ONLINE"),
        "total_iot_nodes": len(health),
        "disclaimer": "NER-LEWS PROTOTYPE AUTHORITY COMMAND CONSOLE",
        "is_demo": True
    }

@router.get("/api/system/health")
async def get_system_health():
    return {
        "status": "HEALTHY",
        "version": "2.6.0-PROTOTYPE",
        "database": "CONNECTED",
        "ml_engine": "READY (Ensemble + Limit Equilibrium Geotech)",
        "offline_store_and_forward": "ACTIVE",
        "satellite_engine": "READY",
        "is_demo": True
    }
