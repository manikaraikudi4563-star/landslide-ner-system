from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from app.database import get_all_sensor_health
from app.services.telemetry_service import telemetry_service
from app.services.anomaly_service import anomaly_service

router = APIRouter(tags=["Sensors & Telemetry"])

class AnomalyActionRequest(BaseModel):
    anomaly_id: str = Field(..., description="Unique ID of the anomaly record")
    action: str = Field("acknowledge", description="Action: acknowledge | maintenance | resolve")

@router.get("/api/sensors")
async def get_all_sensors(state: Optional[str] = None):
    stations = telemetry_service.get_all_stations()
    if state and state.upper() != "ALL":
        stations = [s for s in stations if s["state"].lower() == state.lower()]
    return {
        "total_sensor_arrays": len(stations) * 4,
        "stations": stations,
        "is_demo": True
    }

@router.get("/api/sensor-readings")
async def get_sensor_readings(station_id: str = Query(..., description="Target station ID"), interval: str = Query("24h", description="Timeframe: 1h, 6h, 12h, 24h, 7d")):
    detail = telemetry_service.get_station_details(station_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Station not found")
    
    timeseries = detail.get("timeseries_history", [])
    if interval == "1h":
        return timeseries[-2:]
    elif interval == "6h":
        return timeseries[-4:]
    elif interval == "12h":
        return timeseries[-6:]
    elif interval == "7d":
        return timeseries * 2
    return timeseries

@router.get("/api/sensors/anomalies")
async def get_sensor_anomalies():
    return anomaly_service.get_all_anomalies()

@router.post("/api/sensors/anomalies/action")
async def handle_anomaly_action(req: AnomalyActionRequest):
    updated = anomaly_service.update_anomaly_status(req.anomaly_id, req.action)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Anomaly ID '{req.anomaly_id}' not found")
    return {
        "status": "SUCCESS",
        "anomaly": updated,
        "message": f"Anomaly {req.anomaly_id} updated to status {updated['status']}."
    }

@router.get("/api/sensor-health")
async def get_sensor_health():
    health_records = get_all_sensor_health()
    online_count = sum(1 for h in health_records if h["status"] == "ONLINE")
    warning_count = sum(1 for h in health_records if h["status"] == "WARNING")
    offline_count = sum(1 for h in health_records if h["status"] == "OFFLINE")

    return {
        "total_sensors": len(health_records) * 4,
        "total_stations": len(health_records),
        "online_stations": online_count,
        "warning_stations": warning_count,
        "offline_stations": offline_count,
        "average_battery_pct": round(sum(h["battery_pct"] for h in health_records) / max(1, len(health_records)), 1),
        "average_uptime_pct": round(sum(h["uptime_pct"] for h in health_records) / max(1, len(health_records)), 2),
        "network_status": "OPTIMAL",
        "station_records": health_records,
        "is_demo": True
    }

@router.post("/api/telemetry/tick")
async def trigger_telemetry_tick(intensity_multiplier: float = Query(1.0, ge=0.0, le=10.0)):
    updated = telemetry_service.update_telemetry_tick(intensity_multiplier)
    return {
        "status": "TELEMETRY_UPDATED",
        "updated_stations_count": len(updated),
        "stations": updated,
        "is_demo": True
    }
