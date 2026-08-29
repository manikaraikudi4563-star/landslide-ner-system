"""
Comprehensive Full-Stack Backend Test Suite for NER-LEWS.
Tests API success, validation error rejections (422, 400, 404), database operations,
ML prediction contract, anomaly actions, shelter MCDA, risk-aware routing,
multi-language alert localization, and offline store-and-forward synchronization.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from ml import predictRisk

client = TestClient(app)

def test_system_health():
    res = client.get("/api/system/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "HEALTHY"
    assert data["is_demo"] is True

def test_states_endpoint():
    res = client.get("/api/states")
    assert res.status_code == 200
    states = res.json()
    assert len(states) == 8
    assert "Manipur" in states
    assert "Sikkim" in states

def test_stations_and_detail():
    res = client.get("/api/stations")
    assert res.status_code == 200
    stns = res.json()
    assert len(stns) == 12

    # Detail
    res_det = client.get("/api/stations/STN-MAN-01")
    assert res_det.status_code == 200
    assert res_det.json()["name"] == "Tupul Railway Yard Sentinel"

    # 404 on invalid
    res_404 = client.get("/api/stations/NON-EXISTENT-99")
    assert res_404.status_code == 404

def test_ml_prediction_contract():
    # Valid inference
    res = client.post("/api/predict", json={
        "slope_deg": 50.0,
        "pore_water_pressure_kpa": 35.0,
        "tilt_rate": 0.40,
        "soil_moisture_pct": 85.0,
        "rainfall_24h_mm": 70.0,
        "rainfall_7d_mm": 250.0,
        "lithology": "Weak Disang Shale"
    })
    assert res.status_code == 200
    data = res.json()
    assert "probability" in data
    assert "riskLevel" in data
    assert "factors" in data
    assert "confidence" in data
    assert "modelVersion" in data
    assert data["isDemo"] is True

    # Validation rejection (out of bounds)
    res_bad = client.post("/api/predict", json={
        "slope_deg": 120.0, # invalid slope > 85
        "soil_moisture_pct": -10.0 # negative moisture
    })
    assert res_bad.status_code == 422

def test_sensor_anomalies_and_actions():
    res = client.get("/api/sensors/anomalies")
    assert res.status_code == 200
    anoms = res.json()
    assert len(anoms) >= 1
    anom_id = anoms[0]["id"]

    # Action: Acknowledge
    res_ack = client.post("/api/sensors/anomalies/action", json={
        "anomaly_id": anom_id,
        "action": "acknowledge"
    })
    assert res_ack.status_code == 200
    assert res_ack.json()["anomaly"]["status"] == "ACKNOWLEDGED"

def test_smart_shelter_recommendation_and_details():
    res = client.get("/api/shelters/recommend?lat=24.7083&lng=93.6500")
    assert res.status_code == 200
    data = res.json()
    assert "best_recommended" in data
    assert data["best_recommended"]["suitability_score"] > 80.0

    # Shelter Detail
    res_det = client.get("/api/shelters/SHL-MAN-01")
    assert res_det.status_code == 200
    assert res_det.json()["capacity"] == 850

def test_risk_aware_routing():
    res = client.post("/api/evacuation/plan", json={
        "latitude": 24.7083,
        "longitude": 93.6500,
        "shelter_id": "SHL-MAN-01"
    })
    assert res.status_code == 200
    data = res.json()
    assert len(data["recommended_routes"]) > 0
    route = data["recommended_routes"][0]
    assert route["estimated_road_km"] > 0
    assert "route_path" in route

def test_multi_language_alerts():
    languages = ["en", "hi", "as", "mni", "lus", "kha", "nag", "bn"]
    for l in languages:
        res = client.get(f"/api/alerts/translations?lang={l}")
        assert res.status_code == 200
        assert res.json()["lang_code"] == l

def test_offline_communication_and_sync():
    # Toggle offline
    client.post("/api/communication/toggle-network")
    q_res = client.post("/api/communication/test", json={
        "alert_id": "ALT-TEST-COMM",
        "location": "Noney",
        "headline": "TEST ALARM"
    })
    assert q_res.status_code == 200
    assert q_res.json()["is_online"] is False

    # Sync restoration
    sync_res = client.post("/api/communication/sync")
    assert sync_res.status_code == 200
    assert sync_res.json()["status"] == "QUEUE_SYNCHRONIZED"

    # Toggle back online
    client.post("/api/communication/toggle-network")

def test_incident_reporting():
    res = client.post("/api/incidents", json={
        "reporter_name": "Test Sentinel",
        "contact_number": "+91-9999999999",
        "state": "Manipur",
        "location_name": "Tupul Hill Mile 42",
        "latitude": 24.7083,
        "longitude": 93.6500,
        "landslide_type": "Debris Slide",
        "estimated_size": "Medium",
        "road_blocked": True,
        "casualties_reported": 0,
        "description": "Test incident report."
    })
    assert res.status_code in [200, 201]
    assert "report_id" in res.json()

if __name__ == "__main__":
    test_system_health()
    print("test_system_health: PASS")
    test_states_endpoint()
    print("test_states_endpoint: PASS")
    test_stations_and_detail()
    print("test_stations_and_detail: PASS")
    test_ml_prediction_contract()
    print("test_ml_prediction_contract: PASS")
    test_sensor_anomalies_and_actions()
    print("test_sensor_anomalies_and_actions: PASS")
    test_smart_shelter_recommendation_and_details()
    print("test_smart_shelter_recommendation_and_details: PASS")
    test_risk_aware_routing()
    print("test_risk_aware_routing: PASS")
    test_multi_language_alerts()
    print("test_multi_language_alerts: PASS")
    test_offline_communication_and_sync()
    print("test_offline_communication_and_sync: PASS")
    test_incident_reporting()
    print("test_incident_reporting: PASS")
    print("==================================================")
    print("ALL FULL-STACK BACKEND SUITE TESTS PASSED (100%)")
    print("==================================================")

