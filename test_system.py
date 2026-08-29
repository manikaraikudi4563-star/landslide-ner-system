"""
Direct Automated Test Suite for the AI-Based Landslide Risk Early Warning System in NER.
Tests ML inference, geotechnical physics, database persistence, and FastAPI REST endpoints.
"""

import os
import sys

# Set UTF-8 encoding for stdout on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure root is in path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from fastapi.testclient import TestClient
from app.main import app
from app.models.ml_engine import ml_engine
from app.models.geotech_engine import geotech_engine
from app.services.routing_service import routing_service
from app.services.telemetry_service import telemetry_service
from app.services.alert_service import alert_service
from app.database import init_db, add_citizen_report, get_all_reports, get_active_alerts

client = TestClient(app)

def run_all_tests():
    print("=" * 60)
    print("  RUNNING AI LANDSLIDE SYSTEM TESTS (DIRECT ASYNC/SYNC)")
    print("=" * 60)

    # 1. Initialize Database
    init_db()
    print("  [PASS] SQLite Database schema initialized")

    # 2. ML Engine Tests
    pred = ml_engine.predict_susceptibility({
        "slope_deg": 52.0,
        "aspect_deg": 180.0,
        "elevation_m": 1600.0,
        "fault_dist_km": 1.5,
        "lithology_code": 3,
        "lulc_code": 3,
        "soil_moisture_pct": 85.0,
        "rainfall_7d_mm": 320.0
    })
    assert "risk_score" in pred, "ML response missing risk_score"
    assert 0.0 <= pred["risk_score"] <= 100.0, "Risk score out of range"
    assert "factor_breakdown" in pred, "ML response missing factor_breakdown"
    print(f"  [PASS] ML Susceptibility Inference: Score={pred['risk_score']} Tier={pred['tier']}")

    # 3. Geotechnical Factor of Safety Test
    fs_stable = geotech_engine.calculate_factor_of_safety(
        slope_deg=22.0,
        pore_water_pressure_kpa=6.0,
        soil_cohesion_kpa=14.0,
        friction_angle_deg=30.0
    )
    assert fs_stable["factor_of_safety"] >= 1.3, "Stable Fs calculation error"

    fs_failure = geotech_engine.calculate_factor_of_safety(
        slope_deg=62.0,
        pore_water_pressure_kpa=42.0,
        soil_cohesion_kpa=4.0,
        friction_angle_deg=20.0
    )
    assert fs_failure["factor_of_safety"] < 1.0, "Failure Fs calculation error"
    print(f"  [PASS] Geotechnical Fs: Stable={fs_stable['factor_of_safety']} | Failure={fs_failure['factor_of_safety']}")

    # 4. Rainfall I-D Threshold Test
    id_res = geotech_engine.calculate_id_threshold("Sikkim", intensity_mm_hr=65.0, duration_hrs=10.0)
    assert "RED" in id_res["stage"], "Cloudburst should trigger RED stage"
    print(f"  [PASS] Rainfall I-D Threshold: Stage={id_res['stage']} (Breach={id_res['threshold_percentage']}%)")

    # 5. Evacuation Routing Test
    evac_routes = routing_service.find_nearest_shelters(origin_lat=24.7083, origin_lng=93.6500, limit=2)
    assert len(evac_routes) > 0, "No evacuation routes found"
    top_shelter = evac_routes[0]
    print(f"  [PASS] Evacuation Routing: Nearest={top_shelter['shelter']['name']} ({top_shelter['estimated_road_km']} km, ~{top_shelter['drive_time_mins']} min drive)")

    # 6. Telemetry & Stations Test
    stations = telemetry_service.get_all_stations()
    assert len(stations) == 12, f"Expected 12 stations, got {len(stations)}"
    
    updated_stations = telemetry_service.update_telemetry_tick(1.2)
    assert len(updated_stations) == 12, "Telemetry update failed"
    print(f"  [PASS] IoT Telemetry: 12 monitoring stations verified & simulated")

    # 7. Endpoint Tests via TestClient
    overview_resp = client.get("/api/overview")
    assert overview_resp.status_code == 200
    overview = overview_resp.json()
    assert overview["system_status"] == "OPERATIONAL"
    assert overview["total_monitoring_stations"] == 12

    # What-If Simulation
    sim_req = {
        "state": "Meghalaya",
        "slope_deg": 50.0,
        "rainfall_intensity_mm_hr": 40.0,
        "duration_hrs": 6.0,
        "pore_water_pressure_kpa": 34.0,
        "soil_moisture_pct": 80.0,
        "rainfall_7d_mm": 260.0
    }
    sim_resp = client.post("/api/simulate/whatif", json=sim_req)
    assert sim_resp.status_code == 200
    sim_res = sim_resp.json()
    assert "composite_risk_score" in sim_res
    assert "factor_of_safety_analysis" in sim_res

    # Citizen Report
    rep_req = {
        "reporter_name": "Field Officer Sangma",
        "contact_number": "+91-9876543210",
        "state": "Meghalaya",
        "location_name": "Sohra-Shella Escarpment",
        "latitude": 25.2986,
        "longitude": 91.7180,
        "landslide_type": "Debris Slide",
        "estimated_size": "Medium",
        "road_blocked": True,
        "casualties_reported": 0,
        "description": "Active toppling on cut slope after 250mm downpour."
    }
    rep_resp = client.post("/api/reports", json=rep_req)
    assert rep_resp.status_code in [200, 201]
    assert rep_resp.json()["status"] == "SUCCESS"

    reports = get_all_reports()
    assert any(r["location_name"] == "Sohra-Shella Escarpment" for r in reports)
    print("  [PASS] FastAPI Async Endpoints: Overview, What-If Simulation, and Citizen Reporting verified")

    print("=" * 60)
    print("  ALL 7 SYSTEM TEST MODULES PASSED (100% SUCCESS)")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()
