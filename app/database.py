"""
Database models and initialization for the NER Landslide Early Warning System.
Uses SQLite for persistent storage of telemetry histories, sensor health, alerts,
risk predictions, weather streams, historical landslides, shelters, citizen reports,
satellite changes, infrastructure, sensor anomalies, and offline communication queue.
"""

import sqlite3
import os
import json
from datetime import datetime, timezone
from app.config.settings import settings

DB_PATH = settings.DATABASE_URL

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

def run_migrations(conn: sqlite3.Connection):
    """Ensures existing SQLite tables have all required columns."""
    cursor = conn.cursor()
    
    # Check sensor_telemetry columns
    cursor.execute("PRAGMA table_info(sensor_telemetry)")
    columns = [row[1] for row in cursor.fetchall()]
    if columns:
        required_cols = [
            ("rainfall_1h", "REAL"),
            ("rainfall_6h", "REAL"),
            ("rainfall_24h", "REAL"),
            ("rainfall_cumulative_7d", "REAL"),
            ("pore_water_pressure", "REAL"),
            ("tilt_rate", "REAL"),
            ("soil_moisture", "REAL"),
            ("temperature_c", "REAL"),
            ("vibration_freq", "REAL"),
            ("factor_of_safety", "REAL"),
            ("risk_score", "REAL"),
            ("warning_level", "TEXT")
        ]
        for col_name, col_type in required_cols:
            if col_name not in columns:
                try:
                    cursor.execute(f"ALTER TABLE sensor_telemetry ADD COLUMN {col_name} {col_type}")
                except Exception:
                    pass
    conn.commit()

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        role TEXT NOT NULL DEFAULT 'VIEWER',
        full_name TEXT NOT NULL,
        department TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # 2. Stations Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        station_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        state TEXT NOT NULL,
        district TEXT NOT NULL,
        corridor TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        elevation_m REAL NOT NULL,
        slope_deg REAL NOT NULL,
        lithology TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'ONLINE'
    )
    """)

    # 3. IoT Sensor Readings History
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_telemetry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        station_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        rainfall_1h REAL,
        rainfall_6h REAL,
        rainfall_24h REAL,
        rainfall_cumulative_7d REAL,
        pore_water_pressure REAL,
        tilt_rate REAL,
        soil_moisture REAL,
        temperature_c REAL,
        vibration_freq REAL,
        factor_of_safety REAL,
        risk_score REAL,
        warning_level TEXT
    )
    """)

    # 4. Sensor Network Health Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_health (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        station_id TEXT UNIQUE NOT NULL,
        status TEXT NOT NULL DEFAULT 'ONLINE',
        battery_pct INTEGER NOT NULL,
        solar_charging_v REAL,
        signal_strength_dbm INTEGER NOT NULL,
        uptime_pct REAL NOT NULL,
        last_communication TEXT NOT NULL,
        data_quality_pct REAL NOT NULL
    )
    """)

    # 5. Regional Risk Zones Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS risk_zones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        zone_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        state TEXT NOT NULL,
        district TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        risk_tier TEXT NOT NULL,
        ai_probability REAL NOT NULL,
        nearby_highway TEXT,
        nearby_railway TEXT,
        last_evaluated TEXT NOT NULL
    )
    """)

    # 6. Risk Predictions & XAI Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS risk_predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        risk_score REAL NOT NULL,
        risk_tier TEXT NOT NULL,
        factor_of_safety REAL NOT NULL,
        xai_breakdown TEXT NOT NULL
    )
    """)

    # 7. Weather Data Stream Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        state TEXT UNIQUE NOT NULL,
        station_id TEXT,
        temp_c REAL NOT NULL,
        rainfall_current REAL NOT NULL,
        rainfall_1h REAL NOT NULL,
        rainfall_6h REAL NOT NULL,
        rainfall_24h REAL NOT NULL,
        forecast_rain_24h REAL NOT NULL,
        condition TEXT NOT NULL,
        trend TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)

    # 8. Alert Logs (CAP 1.2 Compliant) & Timeline Events
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alert_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_id TEXT UNIQUE NOT NULL,
        station_id TEXT,
        region_name TEXT NOT NULL,
        state TEXT NOT NULL,
        severity TEXT NOT NULL,
        event_type TEXT NOT NULL,
        headline TEXT NOT NULL,
        description TEXT NOT NULL,
        instruction TEXT NOT NULL,
        coordinates TEXT NOT NULL,
        created_at TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'ACTIVE',
        notified_channels TEXT
    )
    """)

    # 9. Citizen / Field Incident Reports
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS citizen_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_id TEXT UNIQUE NOT NULL,
        reporter_name TEXT NOT NULL,
        contact_number TEXT,
        state TEXT NOT NULL,
        location_name TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        landslide_type TEXT NOT NULL,
        estimated_size TEXT NOT NULL,
        road_blocked INTEGER DEFAULT 0,
        casualties_reported INTEGER DEFAULT 0,
        description TEXT,
        image_url TEXT,
        status TEXT DEFAULT 'VERIFIED_DISPATCH',
        created_at TEXT NOT NULL
    )
    """)

    # 10. Evacuation Shelters
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evacuation_shelters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shelter_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        state TEXT NOT NULL,
        district TEXT NOT NULL,
        location TEXT,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        capacity INTEGER NOT NULL,
        occupied INTEGER DEFAULT 0,
        available_capacity INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'AVAILABLE',
        drinking_water INTEGER DEFAULT 1,
        first_aid INTEGER DEFAULT 1,
        food INTEGER DEFAULT 1,
        toilets INTEGER DEFAULT 1,
        emergency_power INTEGER DEFAULT 1,
        satellite_comms INTEGER DEFAULT 1,
        contact_authority TEXT,
        contact_phone TEXT,
        amenities TEXT
    )
    """)

    # 11. Historical Landslides Archive
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historical_landslides (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        state TEXT NOT NULL,
        district TEXT NOT NULL,
        event_date TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        casualties INTEGER DEFAULT 0,
        volume_m3 INTEGER NOT NULL,
        trigger_factor TEXT NOT NULL,
        landslide_type TEXT NOT NULL,
        infrastructure_damage TEXT NOT NULL
    )
    """)

    # 12. Satellite Changes Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS satellite_changes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        change_id TEXT UNIQUE NOT NULL,
        location_id TEXT,
        name TEXT NOT NULL,
        state TEXT NOT NULL,
        district TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        before_date TEXT NOT NULL,
        after_date TEXT NOT NULL,
        change_pct REAL NOT NULL,
        change_class TEXT NOT NULL,
        risk_indicator TEXT NOT NULL,
        polygon_coords TEXT NOT NULL
    )
    """)

    # 13. Infrastructure Assets Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS infrastructure (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        infra_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        category TEXT NOT NULL,
        state TEXT NOT NULL,
        district TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        criticality TEXT NOT NULL,
        status TEXT NOT NULL,
        description TEXT
    )
    """)

    # 14. Sensor Anomalies Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_anomalies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        anomaly_id TEXT UNIQUE NOT NULL,
        station_id TEXT NOT NULL,
        sensor_type TEXT NOT NULL,
        anomalous_val TEXT NOT NULL,
        detection_reason TEXT NOT NULL,
        severity TEXT NOT NULL,
        status TEXT NOT NULL,
        detected_at TEXT NOT NULL
    )
    """)

    # 15. Offline Communication Queue Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS communication_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        msg_id TEXT UNIQUE NOT NULL,
        alert_id TEXT NOT NULL,
        recipient_group TEXT NOT NULL,
        target_location TEXT NOT NULL,
        channel TEXT NOT NULL,
        payload TEXT NOT NULL,
        status TEXT NOT NULL,
        queued_at TEXT NOT NULL,
        delivered_at TEXT
    )
    """)

    conn.commit()
    run_migrations(conn)
    seed_initial_data(conn)
    conn.close()

def seed_initial_data(conn: sqlite3.Connection):
    cursor = conn.cursor()
    now_str = datetime.now(timezone.utc).isoformat()

    # Seed Default Users
    users = [
        ("admin@ner-lews.gov.in", "ADMIN", "Dr. T. Sharma", "Director of Disaster Management"),
        ("authority@sdma.in", "AUTHORITY", "Inspector K. Roy", "State Disaster Response Force"),
        ("field@survey.gov.in", "FIELD_USER", "Tenzing Norbu", "Geological Survey Field Sentinel"),
        ("public@viewer.in", "VIEWER", "Public Citizen", "NER Community Observer")
    ]
    for u in users:
        cursor.execute("INSERT OR IGNORE INTO users (username, role, full_name, department, created_at) VALUES (?, ?, ?, ?, ?)", (*u, now_str))

    # Seed Sensor Network Health for 12 Stations
    station_ids = [
        ("STN-SIK-01", "ONLINE", 98, 14.2, -62, 99.8, 99.4),
        ("STN-SIK-02", "ONLINE", 94, 13.8, -68, 99.5, 98.9),
        ("STN-MEG-01", "ONLINE", 91, 13.6, -72, 99.1, 98.7),
        ("STN-MEG-02", "ONLINE", 88, 13.4, -75, 98.8, 97.5),
        ("STN-ASM-01", "ONLINE", 96, 14.0, -65, 99.9, 99.6),
        ("STN-ASM-02", "ONLINE", 100, 14.4, -58, 100.0, 99.9),
        ("STN-MAN-01", "WARNING", 76, 12.8, -82, 97.4, 95.8),
        ("STN-NAG-01", "ONLINE", 92, 13.9, -70, 99.2, 99.0),
        ("STN-MIZ-01", "ONLINE", 89, 13.5, -74, 98.9, 98.2),
        ("STN-ARU-01", "ONLINE", 85, 13.1, -78, 98.5, 97.8),
        ("STN-ARU-02", "ONLINE", 97, 14.1, -64, 99.7, 99.5),
        ("STN-TRI-01", "ONLINE", 95, 14.0, -66, 99.6, 99.3)
    ]
    for s in station_ids:
        cursor.execute("""
        INSERT OR REPLACE INTO sensor_health (
            station_id, status, battery_pct, solar_charging_v, signal_strength_dbm,
            uptime_pct, last_communication, data_quality_pct
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (s[0], s[1], s[2], s[3], s[4], s[5], now_str, s[6]))

    # Seed Weather Data for all 8 NER States
    weather_states = [
        ("Meghalaya", 21.5, 38.5, 12.0, 45.0, 92.0, 120.0, "Heavy Monsoonal Rain", "Increasing"),
        ("Sikkim", 16.8, 18.0, 6.5, 28.0, 64.0, 85.0, "Continuous Torrential Drizzle", "Steady"),
        ("Manipur", 24.2, 28.0, 9.5, 36.0, 68.0, 95.0, "Active Cloudburst Storm", "Increasing"),
        ("Assam", 27.5, 14.0, 4.0, 22.0, 48.0, 65.0, "Scattered Severe Thunderstorms", "Steady"),
        ("Nagaland", 19.8, 16.5, 5.0, 25.0, 52.0, 70.0, "Overcast Monsoon Showers", "Steady"),
        ("Mizoram", 22.0, 22.5, 7.0, 32.0, 58.0, 78.0, "Continuous Ridge Rain", "Decreasing"),
        ("Arunachal Pradesh", 14.5, 12.0, 4.0, 19.0, 42.0, 55.0, "High Altitude Fog & Showers", "Steady"),
        ("Tripura", 28.0, 8.5, 2.5, 14.0, 26.0, 35.0, "Humid Intermittent Rain", "Decreasing")
    ]
    for w in weather_states:
        cursor.execute("""
        INSERT OR REPLACE INTO weather_data (
            state, temp_c, rainfall_current, rainfall_1h, rainfall_6h, rainfall_24h,
            forecast_rain_24h, condition, trend, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (*w, now_str))

    conn.commit()

def log_telemetry_reading(reading: Dict[str, Any]):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO sensor_telemetry (
        station_id, timestamp, rainfall_1h, rainfall_6h, rainfall_24h, rainfall_cumulative_7d,
        pore_water_pressure, tilt_rate, soil_moisture, temperature_c, vibration_freq,
        factor_of_safety, risk_score, warning_level
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        reading.get("station_id"),
        reading.get("timestamp", datetime.now(timezone.utc).isoformat()),
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
    cursor.execute("SELECT * FROM sensor_telemetry WHERE station_id = ? ORDER BY id DESC LIMIT ?", (station_id, limit))
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
        cursor.execute("SELECT * FROM alert_logs WHERE LOWER(state) = LOWER(?) AND status = 'ACTIVE' ORDER BY id DESC", (state,))
    else:
        cursor.execute("SELECT * FROM alert_logs WHERE status = 'ACTIVE' ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_citizen_report(report: Dict[str, Any]) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()
    report_id = f"REP-NER-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
    cursor.execute("""
    INSERT INTO citizen_reports (
        report_id, reporter_name, contact_number, state, location_name,
        latitude, longitude, landslide_type, estimated_size, road_blocked,
        casualties_reported, description, image_url, status, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        "VERIFIED_DISPATCH",
        datetime.now(timezone.utc).isoformat()
    ))
    conn.commit()
    conn.close()
    return report_id

def get_all_reports() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM citizen_reports ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def insert_alert(alert_data: Dict[str, Any]) -> str:
    conn = get_db_connection()
    cursor = conn.cursor()
    alert_id = alert_data.get("alert_id") or f"ALT-NER-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
    coords_json = json.dumps(alert_data.get("coordinates", [24.7083, 93.6500]))
    channels_json = json.dumps(alert_data.get("notified_channels", ["CAP-XML", "SMS", "RADIO"]))

    cursor.execute("""
    INSERT OR REPLACE INTO alert_logs (
        alert_id, station_id, region_name, state, severity, event_type,
        headline, description, instruction, coordinates, created_at, status, notified_channels
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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

