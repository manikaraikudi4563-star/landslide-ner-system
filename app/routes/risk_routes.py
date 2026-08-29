from fastapi import APIRouter, Query
from typing import Optional
from app.services.telemetry_service import telemetry_service
from app.services.alert_service import alert_service
from app.services.routing_service import routing_service
from app.data.ner_geospatial import NER_STATES, NER_CORRIDORS, REGIONAL_RISK_SUMMARY

router = APIRouter(tags=["Risk Zones & Overview"])

@router.get("/api/overview")
async def get_system_overview(state: Optional[str] = None):
    all_stations = telemetry_service.get_all_stations()
    stations = [s for s in all_stations if s["state"].lower() == state.lower()] if (state and state.upper() != "ALL") else all_stations

    critical_count = sum(1 for s in stations if s["current_readings"]["warning_level"] == "RED" or s["current_readings"]["factor_of_safety"] < 1.0)
    high_count = sum(1 for s in stations if s["current_readings"]["warning_level"] == "ORANGE" or (s["current_readings"]["factor_of_safety"] < 1.25 and s["current_readings"]["factor_of_safety"] >= 1.0))
    moderate_count = sum(1 for s in stations if s["current_readings"]["warning_level"] == "YELLOW")
    low_count = sum(1 for s in stations if s["current_readings"]["warning_level"] == "GREEN")

    max_rain = max((s["current_readings"]["rainfall_24h"] for s in stations), default=0.0)
    active_alerts = alert_service.get_all_active_alerts()
    all_shelters = routing_service.get_all_shelters()

    return {
        "system_status": "OPERATIONAL",
        "is_demo_mode": True,
        "is_demo": True,
        "region": "North Eastern Region (NER) - 8 States",
        "total_monitoring_stations": len(stations),
        "total_shelters": len(all_shelters),
        "active_alerts_count": len(active_alerts),
        "high_risk_stations_count": critical_count + high_count,
        "critical_emergency_count": critical_count,
        "max_regional_rainfall_24h_mm": max_rain,
        "risk_breakdown": {
            "critical": critical_count if state and state.upper() != "ALL" else REGIONAL_RISK_SUMMARY["critical_count"],
            "high": high_count if state and state.upper() != "ALL" else REGIONAL_RISK_SUMMARY["high_risk_count"],
            "moderate": moderate_count if state and state.upper() != "ALL" else REGIONAL_RISK_SUMMARY["moderate_risk_count"],
            "low": low_count if state and state.upper() != "ALL" else REGIONAL_RISK_SUMMARY["low_risk_count"]
        },
        "states_monitored": list(NER_STATES.keys()),
        "key_corridors_count": len(NER_CORRIDORS),
        "active_alerts": active_alerts[:5]
    }

@router.get("/api/risk-zones")
async def get_risk_zones(state: Optional[str] = None):
    stations = telemetry_service.get_all_stations()
    if state and state.upper() != "ALL":
        stations = [s for s in stations if s["state"].lower() == state.lower()]
    return {
        "summary": REGIONAL_RISK_SUMMARY,
        "hotspots": stations,
        "is_demo": True
    }

@router.get("/api/predictions")
async def get_all_predictions():
    stations = telemetry_service.get_all_stations()
    preds = []
    for s in stations:
        r = s["current_readings"]
        preds.append({
            "station_id": s["id"],
            "name": s["name"],
            "state": s["state"],
            "risk_score": r["risk_score"],
            "risk_tier": r["warning_level"],
            "factor_of_safety": r["factor_of_safety"],
            "status_text": r["status_text"],
            "is_demo": True
        })
    return preds

@router.get("/api/heatmap")
async def get_heatmap_grid(lat: float = Query(25.5, ge=20.0, le=32.0), lng: float = Query(92.5, ge=85.0, le=100.0), radius: float = Query(0.6, ge=0.1, le=5.0)):
    points = []
    steps = 8
    d_step = (radius * 2) / steps
    for i in range(steps):
        for j in range(steps):
            pt_lat = round(lat - radius + (i * d_step), 4)
            pt_lng = round(lng - radius + (j * d_step), 4)
            dist_center = ((pt_lat - lat)**2 + (pt_lng - lng)**2)**0.5
            score = round(max(20.0, min(95.0, 88.0 - (dist_center * 45.0) + (i % 3) * 6)), 1)
            tier = "CRITICAL" if score > 80 else ("HIGH" if score > 60 else ("MODERATE" if score > 35 else "LOW"))
            color = "#ef4444" if tier == "CRITICAL" else ("#f97316" if tier == "HIGH" else ("#f59e0b" if tier == "MODERATE" else "#10b981"))
            points.append({
                "lat": pt_lat,
                "lng": pt_lng,
                "risk_score": score,
                "tier": tier,
                "color": color
            })
    return {"grid_points": points, "is_demo": True}
