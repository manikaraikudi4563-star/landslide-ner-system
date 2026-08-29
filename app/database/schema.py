"""
Comprehensive Database Schema, Self-Healing Migrations, and Index Definitions for NER-LEWS.
"""

import sqlite3

SCHEMA_SQL = """
-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL DEFAULT 'VIEWER',
    full_name TEXT NOT NULL,
    department TEXT,
    created_at TEXT NOT NULL
);

-- 2. NER States Master Table
CREATE TABLE IF NOT EXISTS states (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT UNIQUE NOT NULL,
    capital TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    vulnerability_score INTEGER NOT NULL,
    vulnerability_level TEXT NOT NULL,
    geology TEXT NOT NULL,
    seismic_zone TEXT NOT NULL,
    annual_rainfall_mm REAL NOT NULL,
    is_demo INTEGER DEFAULT 1
);

-- 3. Monitoring Stations Table
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
    status TEXT NOT NULL DEFAULT 'ONLINE',
    is_demo INTEGER DEFAULT 1
);

-- 4. IoT Sensor Telemetry & Readings Table
CREATE TABLE IF NOT EXISTS sensor_readings (
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
    warning_level TEXT,
    is_demo INTEGER DEFAULT 1
);

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
    warning_level TEXT,
    is_demo INTEGER DEFAULT 1
);

-- 5. Sensor Network Health Table
CREATE TABLE IF NOT EXISTS sensor_health (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_id TEXT UNIQUE NOT NULL,
    status TEXT NOT NULL DEFAULT 'ONLINE',
    battery_pct INTEGER NOT NULL,
    solar_charging_v REAL,
    signal_strength_dbm INTEGER NOT NULL,
    uptime_pct REAL NOT NULL,
    last_communication TEXT NOT NULL,
    data_quality_pct REAL NOT NULL,
    is_demo INTEGER DEFAULT 1
);

-- 6. Sensor Anomalies Table
CREATE TABLE IF NOT EXISTS sensor_anomalies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    anomaly_id TEXT UNIQUE NOT NULL,
    station_id TEXT NOT NULL,
    station_name TEXT,
    sensor_type TEXT NOT NULL,
    previous_val TEXT,
    anomalous_val TEXT NOT NULL,
    unit TEXT,
    detection_reason TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'ANOMALY DETECTED',
    detected_at TEXT NOT NULL,
    recommended_action TEXT,
    is_demo INTEGER DEFAULT 1
);

-- 7. Regional Risk Zones Table
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
    last_evaluated TEXT NOT NULL,
    is_demo INTEGER DEFAULT 1
);

-- 8. Risk Predictions Table
CREATE TABLE IF NOT EXISTS risk_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    risk_score REAL NOT NULL,
    risk_tier TEXT NOT NULL,
    factor_of_safety REAL NOT NULL,
    xai_breakdown TEXT NOT NULL,
    is_demo INTEGER DEFAULT 1
);

-- 9. Weather Data Stream Table
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
    updated_at TEXT NOT NULL,
    is_demo INTEGER DEFAULT 1
);

-- 10. Historical Landslides Archive Table
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
    infrastructure_damage TEXT NOT NULL,
    is_demo INTEGER DEFAULT 1
);

-- 11. Evacuation Shelters Table
CREATE TABLE IF NOT EXISTS shelters (
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
    amenities TEXT,
    is_demo INTEGER DEFAULT 1
);

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
    amenities TEXT,
    is_demo INTEGER DEFAULT 1
);

-- 12. Monitored Infrastructure Assets Table
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
    description TEXT,
    is_demo INTEGER DEFAULT 1
);

-- 13. Alert Logs Table
CREATE TABLE IF NOT EXISTS alerts (
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
    notified_channels TEXT,
    is_demo INTEGER DEFAULT 1
);

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
    notified_channels TEXT,
    is_demo INTEGER DEFAULT 1
);

-- 14. Multi-Language Alert Translations Table
CREATE TABLE IF NOT EXISTS alert_translations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lang_code TEXT NOT NULL,
    lang_name TEXT NOT NULL,
    alert_title TEXT NOT NULL,
    action_directive TEXT NOT NULL,
    nearest_shelter_label TEXT NOT NULL,
    authority_text TEXT NOT NULL,
    is_demo INTEGER DEFAULT 1
);

-- 15. Citizen / Field Incident Reports Table
CREATE TABLE IF NOT EXISTS incidents (
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
    created_at TEXT NOT NULL,
    is_demo INTEGER DEFAULT 1
);

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
    created_at TEXT NOT NULL,
    is_demo INTEGER DEFAULT 1
);

-- 16. Satellite Terrain Changes Table
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
    polygon_coords TEXT NOT NULL,
    is_demo INTEGER DEFAULT 1
);

-- 17. Offline Messages Queue Table
CREATE TABLE IF NOT EXISTS offline_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    msg_id TEXT UNIQUE NOT NULL,
    alert_id TEXT NOT NULL,
    recipient_group TEXT NOT NULL,
    target_location TEXT NOT NULL,
    channel TEXT NOT NULL,
    payload TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'QUEUED',
    queued_at TEXT NOT NULL,
    delivered_at TEXT,
    is_demo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS communication_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    msg_id TEXT UNIQUE NOT NULL,
    alert_id TEXT NOT NULL,
    recipient_group TEXT NOT NULL,
    target_location TEXT NOT NULL,
    channel TEXT NOT NULL,
    payload TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'QUEUED',
    queued_at TEXT NOT NULL,
    delivered_at TEXT,
    is_demo INTEGER DEFAULT 1
);

-- 18. System Events Table
CREATE TABLE IF NOT EXISTS system_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    event_source TEXT NOT NULL,
    description TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'INFO',
    timestamp TEXT NOT NULL,
    metadata TEXT,
    is_demo INTEGER DEFAULT 1
);
"""

def run_migrations(conn: sqlite3.Connection):
    cursor = conn.cursor()
    import re
    # Extract table definitions from SCHEMA_SQL
    table_blocks = re.findall(r"CREATE TABLE IF NOT EXISTS (\w+)\s*\((.*?)\);", SCHEMA_SQL, re.DOTALL)
    for table_name, body in table_blocks:
        try:
            cursor.execute(f"PRAGMA table_info({table_name})")
            existing_cols = {row[1] for row in cursor.fetchall()}
            if existing_cols:
                # Parse column definitions
                lines = [line.strip().rstrip(",") for line in body.split("\n") if line.strip() and not line.strip().startswith("--") and not line.strip().startswith("PRIMARY") and not line.strip().startswith("UNIQUE")]
                for col_line in lines:
                    parts = col_line.split()
                    if len(parts) >= 2:
                        col_name = parts[0]
                        col_def = " ".join(parts[1:])
                        if col_name not in existing_cols and not col_name.upper().startswith("PRIMARY") and not col_name.upper().startswith("UNIQUE") and not col_name.upper().startswith("FOREIGN") and not col_name.upper().startswith("CONSTRAINT"):
                            try:
                                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_def}")
                            except Exception:
                                pass
        except Exception:
            pass

    # Create performance indexes
    index_sqls = [
        "CREATE INDEX IF NOT EXISTS idx_sensor_readings_stn_time ON sensor_readings(station_id, timestamp)",
        "CREATE INDEX IF NOT EXISTS idx_sensor_telemetry_stn_time ON sensor_telemetry(station_id, timestamp)",
        "CREATE INDEX IF NOT EXISTS idx_stations_state ON stations(state)",
        "CREATE INDEX IF NOT EXISTS idx_risk_zones_state ON risk_zones(state)",
        "CREATE INDEX IF NOT EXISTS idx_alerts_state_status ON alerts(state, status)",
        "CREATE INDEX IF NOT EXISTS idx_alert_logs_state_status ON alert_logs(state, status)",
        "CREATE INDEX IF NOT EXISTS idx_infrastructure_state ON infrastructure(state)",
        "CREATE INDEX IF NOT EXISTS idx_shelters_state ON shelters(state)",
        "CREATE INDEX IF NOT EXISTS idx_incidents_status ON incidents(status)",
        "CREATE INDEX IF NOT EXISTS idx_citizen_reports_status ON citizen_reports(status)",
        "CREATE INDEX IF NOT EXISTS idx_offline_messages_status ON offline_messages(status)"
    ]
    for sql in index_sqls:
        try:
            cursor.execute(sql)
        except Exception:
            pass
    conn.commit()


def create_schema(conn: sqlite3.Connection):
    run_migrations(conn)
    cursor = conn.cursor()
    cursor.executescript(SCHEMA_SQL)
    conn.commit()
    run_migrations(conn)

