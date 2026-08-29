"""
Automated Verification Test Suite for the 7 Advanced Features of NER-LEWS.
Tests:
1. Satellite Change Detection API
2. Infrastructure Exposure API
3. Sensor Anomaly Detection API
4. Upgraded AI What-If Simulation Sandbox API
5. Smart Multi-Criteria Shelter Allocation API
6. Offline Emergency Communication & Store-and-Forward API
7. Multi-Language Emergency Alerts Localization API (8 Regional Languages)
"""

import sys
import os
import json

# Ensure parent directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_feature_1_satellite_change_detection():
    print("Testing Feature 1: Satellite Change Detection API...")
    res = client.get("/api/satellite/changes")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    data = res.json()
    assert len(data) >= 3, f"Expected >= 3 records, got {len(data)}"
    tupul = next((r for r in data if r["location_id"] == "STN-MAN-01"), None)
    assert tupul is not None, "STN-MAN-01 change record not found"
    assert tupul["change_pct"] == 18.4
    assert tupul["risk_indicator"] == "HIGH"
    print("  [PASS] Feature 1: Satellite Change Detection verified.")

def test_feature_2_infrastructure_risk():
    print("Testing Feature 2: Infrastructure Risk & Impact Analysis API...")
    # Tupul coordinate: 24.7083, 93.6500
    res = client.get("/api/infrastructure?lat=24.7083&lng=93.6500&radius_km=15")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    data = res.json()
    assert len(data) >= 4, f"Expected >= 4 infrastructure assets near Tupul, got {len(data)}"
    
    bridge = next((a for a in data if "Railway Bridge 164" in a["name"]), None)
    assert bridge is not None, "Railway Bridge 164 not found in impacted assets"
    assert bridge["distance_km"] < 2.0, f"Expected distance < 2.0 km, got {bridge['distance_km']}"
    assert bridge["calculated_risk_level"] in ["CRITICAL", "HIGH"]
    print("  [PASS] Feature 2: Infrastructure Risk Impact Analysis verified.")

def test_feature_3_sensor_anomaly_detection():
    print("Testing Feature 3: Sensor Anomaly Detection & Quality Guard API...")
    res = client.get("/api/sensors/anomalies")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 2, f"Expected >= 2 anomalies, got {len(data)}"
    
    anom_id = data[0]["id"]
    # Test Acknowledge action
    act_res = client.post("/api/sensors/anomalies/action", json={"anomaly_id": anom_id, "action": "acknowledge"})
    assert act_res.status_code == 200
    assert act_res.json()["anomaly"]["status"] == "ACKNOWLEDGED"

    # Test Maintenance action
    act_res2 = client.post("/api/sensors/anomalies/action", json={"anomaly_id": anom_id, "action": "maintenance"})
    assert act_res2.status_code == 200
    assert act_res2.json()["anomaly"]["status"] == "MAINTENANCE SCHEDULED"
    print("  [PASS] Feature 3: Sensor Anomaly Detection and Quality Guard verified.")

def test_feature_4_upgraded_whatif_simulation():
    print("Testing Feature 4: Upgraded AI What-If Simulation Sandbox API...")
    payload = {
        "station_id": "STN-MAN-01",
        "rainfall_offset_pct": 30.0,
        "moisture_offset_pct": 10.0,
        "pwp_offset_pct": 15.0,
        "slope_deg": 49.0
    }
    res = client.post("/api/simulation/run", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "current_conditions" in data
    assert "simulated_offsets" in data
    assert "predicted_result" in data
    assert "contributing_factors" in data["predicted_result"]
    assert "SIMULATION" in data["is_simulation_disclaimer"]
    print("  [PASS] Feature 4: Upgraded AI What-If Simulation verified.")

def test_feature_5_smart_shelter_allocation():
    print("Testing Feature 5: Smart Multi-Criteria Shelter Allocation API...")
    res = client.get("/api/shelters/recommend?lat=24.7083&lng=93.6500")
    assert res.status_code == 200
    data = res.json()
    assert "best_recommended" in data
    assert "all_ranked_options" in data
    best = data["best_recommended"]
    assert best["suitability_score"] > 80.0, f"Expected high score for optimal shelter, got {best['suitability_score']}"
    assert "Noney" in best["shelter"]["name"]
    print("  [PASS] Feature 5: Smart Multi-Criteria Shelter Allocation verified.")

def test_feature_6_offline_emergency_communication():
    print("Testing Feature 6: Offline Emergency Communication & Store-and-Forward API...")
    # Check initial status
    status_res = client.get("/api/communication/status")
    assert status_res.status_code == 200
    
    # Toggle offline
    toggle_res = client.post("/api/communication/toggle-network")
    assert toggle_res.status_code == 200
    assert toggle_res.json()["is_online"] == False
    assert toggle_res.json()["network_status"] == "OFFLINE"

    # Queue an emergency alert while offline
    test_msg = {
        "alert_id": "ALT-TEST-OFFLINE-01",
        "location": "Tupul Valley, Manipur",
        "headline": "CRITICAL LANDSLIDE ALARM: Immediate ridge evacuation."
    }
    queue_res = client.post("/api/communication/test", json=test_msg)
    assert queue_res.status_code == 200
    assert queue_res.json()["pending_messages_count"] >= 2

    # Toggle online & auto sync
    toggle_res2 = client.post("/api/communication/toggle-network")
    assert toggle_res2.status_code == 200
    assert toggle_res2.json()["is_online"] == True
    assert toggle_res2.json()["network_status"] == "ONLINE"
    assert toggle_res2.json()["pending_messages_count"] == 0
    print("  [PASS] Feature 6: Offline Emergency Communication & Store-and-Forward verified.")

def test_feature_7_multilingual_emergency_alerts():
    print("Testing Feature 7: Multi-Language Emergency Alerts Localization API...")
    languages = ["en", "hi", "as", "mni", "lus", "kha", "nag", "bn"]
    for lang in languages:
        res = client.get(f"/api/alerts/translations?lang={lang}")
        assert res.status_code == 200, f"Failed for language {lang}"
        data = res.json()
        assert data["lang_code"] == lang
        assert len(data["title"]) > 0
        assert len(data["action_directive"]) > 0
        assert len(data["nearest_shelter"]) > 0
    print("  [PASS] Feature 7: Multi-Language Emergency Alerts (8 Languages) verified.")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("RUNNING COMPLETE NER-LEWS 7 ADVANCED FEATURES VERIFICATION SUITE")
    print("="*70 + "\n")

    test_feature_1_satellite_change_detection()
    test_feature_2_infrastructure_risk()
    test_feature_3_sensor_anomaly_detection()
    test_feature_4_upgraded_whatif_simulation()
    test_feature_5_smart_shelter_allocation()
    test_feature_6_offline_emergency_communication()
    test_feature_7_multilingual_emergency_alerts()

    print("\n" + "="*70)
    print("ALL 7 ADVANCED FEATURES PASSED 100% VERIFICATION!")
    print("="*70 + "\n")
