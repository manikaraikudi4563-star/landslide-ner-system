"""
Database Module for NER-LEWS.
Exports connection managers, initialization, and queries.
"""

from app.database.connection import get_db_connection, get_db
from app.database.schema import create_schema
from app.database.seed import seed_database
from typing import List, Dict, Any, Optional
import json
from datetime import datetime, timezone

def init_db():
    conn = get_db_connection()
    create_schema(conn)
    seed_database(conn)
    conn.close()

def log_telemetry_reading(reading: Dict[str, Any]):
    conn = get_db_connection()
    cursor = conn.cursor()
    now_iso = datetime.now(timezone.utc).isoformat()
    for tbl in ["sensor_readings", "sensor_telemetry"]:
        cursor.execute(f"""
        INSERT INTO {tbl} (
            station_id, timestamp, rainfall_1h, rainfall_6h, rainfall_24h, rainfall_cumulative_7d,
            pore_water_pressure, tilt_rate, soil_moisture, temperature_c, vibration_freq,
            factor_of_safety, risk_score, warning_level, is_demo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            reading.get("station_id"),
            reading.get("timestamp", now_iso),
            reading.get("rainfall_1h", 0.0),
            reading.get("rainfall_6h", 0.0),
            reading.get("rainfall_24h", 0.0),
            reading.get("rainfall_cumulative_7d", 0.0),
            reading.get("pore_water_pressure", 0.0),
            reading.get("tilt_rate", 0.0),
            reading.get("soil_moisture", 0.0),
            reading.get("temperature_c", 22.0),
            reading.get("vibration_freq", 0.0),
            reading.get("factor_of_safety", 1.5),
            reading.get("risk_score", 0.0),
            reading.get("warning_level", "GREEN")
        ))
    conn.commit()
    conn.close()

def get_sensor_history(station_id: str, limit: int = 24) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensor_readings WHERE station_id = ? ORDER BY id DESC LIMIT ?", (station_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_sensor_health() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensor_health")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_weather_for_state(state: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather_data WHERE LOWER(state) = LOWER(?)", (state,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_active_alerts(state: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    if state and state.upper() != "ALL":
        cursor.execute("SELECT * FROM alerts WHERE LOWER(state) = LOWER(?) AND status = 'ACTIVE' ORDER BY id DESC", (state,))
    else:
        cursor.execute("SELECT * FROM alerts WHERE status = 'ACTIVE' ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def insert_alert(alert_data: Dict[str, Any]) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()
    alert_id = alert_data.get("alert_id") or f"ALT-NER-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
    coords_json = json.dumps(alert_data.get("coordinates", [24.7083, 93.6500]))
    channels_json = json.dumps(alert_data.get("notified_channels", ["CAP-XML", "SMS", "RADIO"]))

    for tbl in ["alerts", "alert_logs"]:
        cursor.execute(f"""
        INSERT OR REPLACE INTO {tbl} (
            alert_id, station_id, region_name, state, severity, event_type,
            headline, description, instruction, coordinates, created_at, status, notified_channels, is_demo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            alert_id,
            alert_data.get("station_id", "STN-MAN-01"),
            alert_data.get("region_name", "NER Mountain Corridor"),
            alert_data.get("state", "Manipur"),
            alert_data.get("severity", "Severe"),
            alert_data.get("event_type", "Landslide Warning"),
            alert_data.get("headline", "Landslide Hazard Alert"),
            alert_data.get("description", "Active geotechnical sensor threshold breached."),
            alert_data.get("instruction", "Follow official evacuation routes."),
            coords_json,
            alert_data.get("created_at", datetime.now(timezone.utc).isoformat()),
            alert_data.get("status", "ACTIVE"),
            channels_json
        ))
    conn.commit()
    conn.close()
    return alert_id

def add_citizen_report(report: Dict[str, Any]) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()
    report_id = f"REP-NER-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
    for tbl in ["incidents", "citizen_reports"]:
        cursor.execute(f"""
        INSERT INTO {tbl} (
            report_id, reporter_name, contact_number, state, location_name,
            latitude, longitude, landslide_type, estimated_size, road_blocked,
            casualties_reported, description, image_url, status, created_at, is_demo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'VERIFIED_DISPATCH', ?, 1)
        """, (
            report_id,
            report.get("reporter_name"),
            report.get("contact_number", ""),
            report.get("state"),
            report.get("location_name"),
            report.get("latitude"),
            report.get("longitude"),
            report.get("landslide_type", "Debris Slide"),
            report.get("estimated_size", "Medium"),
            1 if report.get("road_blocked") else 0,
            report.get("casualties_reported", 0),
            report.get("description", ""),
            report.get("image_url", ""),
            datetime.now(timezone.utc).isoformat()
        ))
    conn.commit()
    conn.close()
    return report_id

def get_all_reports() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
