"""
Initial database seeding script for NER-LEWS with verified demo data flags.
"""

import sqlite3
import json
from datetime import datetime, timezone
from app.data.ner_geospatial import (
    NER_STATES, IOT_STATIONS, NER_INFRASTRUCTURE, SATELLITE_CHANGE_RECORDS,
    EVACUATION_SHELTERS, HISTORICAL_LANDSLIDES, KNOWN_SENSOR_ANOMALIES
)

def seed_database(conn: sqlite3.Connection):
    cursor = conn.cursor()
    now_str = datetime.now(timezone.utc).isoformat()

    # 1. Users
    users = [
        ("admin@ner-lews.gov.in", "ADMIN", "Dr. T. Sharma", "Directorate of Disaster Management"),
        ("authority@sdma.in", "AUTHORITY", "Inspector K. Roy", "State Disaster Response Force"),
        ("field@survey.gov.in", "FIELD_USER", "Tenzing Norbu", "Geological Survey Field Sentinel"),
        ("viewer@public.in", "VIEWER", "Public Citizen", "NER Community Observer")
    ]
    for u in users:
        cursor.execute("INSERT OR IGNORE INTO users (username, role, full_name, department, created_at) VALUES (?, ?, ?, ?, ?)", (*u, now_str))

    # 2. States
    for st_name, s in NER_STATES.items():
        cursor.execute("""
        INSERT OR IGNORE INTO states (
            code, name, capital, latitude, longitude, vulnerability_score, vulnerability_level,
            geology, seismic_zone, annual_rainfall_mm, is_demo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            st_name[:3].upper(), st_name, s["capital"], s["lat"], s["lng"],
            s["vulnerability_score"], s["vulnerability_level"], s["geology"],
            s["seismic_zone"], s["annual_rainfall_mm"]
        ))

    # 3. Stations
    for stn in IOT_STATIONS:
        lith = stn.get("lithology", stn.get("geology_type", stn.get("geology", "Weak Disang Shale")))
        cursor.execute("""
        INSERT OR REPLACE INTO stations (
            station_id, name, state, district, corridor, latitude, longitude,
            elevation_m, slope_deg, lithology, status, is_demo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            stn["id"], stn["name"], stn["state"], stn["district"], stn.get("corridor", "Mountain Highway Lifeline"),
            stn["lat"], stn["lng"], stn.get("elevation_m", 1200.0), stn.get("slope_deg", 45.0),
            lith, "ONLINE"
        ))

    # 4. Sensor Health
    for stn in IOT_STATIONS:
        cursor.execute("""
        INSERT OR REPLACE INTO sensor_health (
            station_id, status, battery_pct, solar_charging_v, signal_strength_dbm,
            uptime_pct, last_communication, data_quality_pct, is_demo
        ) VALUES (?, 'ONLINE', 94, 13.8, -68, 99.5, ?, 99.2, 1)
        """, (stn["id"], now_str))

    # 5. Infrastructure
    for inf in NER_INFRASTRUCTURE:
        cursor.execute("""
        INSERT OR REPLACE INTO infrastructure (
            infra_id, name, type, category, state, district, latitude, longitude,
            criticality, status, description, is_demo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            inf["id"], inf["name"], inf["type"], inf["category"], inf["state"],
            inf["district"], inf["latitude"], inf["longitude"], inf["criticality"],
            inf["status"], inf["description"]
        ))

    # 6. Satellite Changes
    for chg in SATELLITE_CHANGE_RECORDS:
        cursor.execute("""
        INSERT OR REPLACE INTO satellite_changes (
            change_id, location_id, name, state, district, latitude, longitude,
            before_date, after_date, change_pct, change_class, risk_indicator, polygon_coords, is_demo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            chg["id"], chg["location_id"], chg["name"], chg["state"], chg["district"],
            chg["latitude"], chg["longitude"], chg["before_date"], chg["after_date"],
            chg["change_pct"], chg["change_class"], chg["risk_indicator"],
            json.dumps(chg["polygon_coordinates"])
        ))

    # 7. Shelters
    for shl in EVACUATION_SHELTERS:
        amenities_json = json.dumps(shl.get("amenities", []))
        for tbl in ["shelters", "evacuation_shelters"]:
            cursor.execute(f"""
            INSERT OR REPLACE INTO {tbl} (
                shelter_id, name, state, district, location, latitude, longitude,
                capacity, occupied, available_capacity, status, drinking_water,
                first_aid, food, toilets, emergency_power, satellite_comms,
                contact_authority, contact_phone, amenities, is_demo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """, (
                shl["id"], shl["name"], shl["state"], shl["district"], shl.get("location", ""),
                shl["lat"], shl["lng"], shl["capacity"], 0, shl["available_capacity"],
                "AVAILABLE", 1 if shl.get("drinking_water") else 0,
                1 if shl.get("first_aid") else 0, 1 if shl.get("food") else 0,
                1 if shl.get("toilets") else 0, 1 if shl.get("emergency_power") else 0,
                1 if shl.get("satellite_comms") else 0, shl.get("contact_authority", ""),
                shl.get("contact_phone", ""), amenities_json
            ))

    # 8. Historical Landslides
    for ev in HISTORICAL_LANDSLIDES:
        cursor.execute("""
        INSERT OR REPLACE INTO historical_landslides (
            event_id, name, state, district, event_date, latitude, longitude,
            casualties, volume_m3, trigger_factor, landslide_type, infrastructure_damage, is_demo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            ev["id"], ev["name"], ev["state"], ev["district"], ev["event_date"],
            ev["latitude"], ev["longitude"], ev["casualties"], ev["volume_m3"],
            ev["trigger_factor"], ev["landslide_type"], ev["infrastructure_damage"]
        ))

    # 9. Sensor Anomalies
    for anom in KNOWN_SENSOR_ANOMALIES:
        cursor.execute("""
        INSERT OR REPLACE INTO sensor_anomalies (
            anomaly_id, station_id, station_name, sensor_type, previous_val,
            anomalous_val, unit, detection_reason, severity, status, detected_at,
            recommended_action, is_demo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            anom["id"], anom["station_id"], anom["station_name"], anom["sensor_type"],
            anom["previous_val"], anom["anomalous_val"], anom["unit"],
            anom["detection_reason"], anom["severity"], anom["status"],
            anom["detected_at"], anom["recommended_action"]
        ))

    # 10. Weather Data
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
            forecast_rain_24h, condition, trend, updated_at, is_demo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (*w, now_str))

    # 11. Alert Translations
    from app.data.alert_translations import ALERT_TRANSLATIONS
    for lcode, tdict in ALERT_TRANSLATIONS.items():
        cursor.execute("""
        INSERT OR REPLACE INTO alert_translations (
            lang_code, lang_name, alert_title, action_directive, nearest_shelter_label, authority_text, is_demo
        ) VALUES (?, ?, ?, ?, ?, ?, 1)
        """, (
            lcode,
            tdict.get("lang_name", lcode),
            tdict.get("alert_title", "Landslide Alert"),
            tdict.get("action_directive_critical", "Evacuate immediately"),
            tdict.get("nearest_shelter_label", "Nearest Shelter"),
            tdict.get("authority_text", "SDMA")
        ))

    cursor.execute("""
    INSERT INTO system_events (
        event_type, event_source, description, severity, timestamp, is_demo
    ) VALUES ('SYSTEM_INITIALIZED', 'DatabaseSeeder', 'NER-LEWS production-ready prototype database initialized and seeded.', 'INFO', ?, 1)
    """, (now_str,))

    conn.commit()

