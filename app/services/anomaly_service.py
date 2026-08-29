"""
AI-Powered Sensor Anomaly Detection and Data Quality Guard Service.
Protects geotechnical and ML susceptibility models from corrupted, impossible, or drifting sensor signals.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from app.data.ner_geospatial import KNOWN_SENSOR_ANOMALIES

class SensorAnomalyService:
    def __init__(self):
        self.anomalies = list(KNOWN_SENSOR_ANOMALIES)

    def validate_reading(self, station_id: str, sensor_type: str, value: float, unit: str) -> Optional[Dict[str, Any]]:
        """
        Applies physical boundary checks and rate-of-change filters.
        Returns anomaly record if invalid, else None.
        """
        is_anomaly = False
        reason = ""

        if sensor_type == "soil_moisture" and (value < 0.0 or value > 100.0):
            is_anomaly = True
            reason = f"Soil moisture reading ({value}%) is physically impossible (>100% or <0%)."
        elif sensor_type == "pore_water_pressure" and (value < -5.0 or value > 150.0):
            is_anomaly = True
            reason = f"Pore pressure ({value} kPa) breaches realistic geotechnical range."
        elif sensor_type == "tilt_rate" and abs(value) > 10.0:
            is_anomaly = True
            reason = f"Unrealistic instantaneous tilt rate spike ({value} mm/h)."

        if is_anomaly:
            rec = {
                "id": f"ANOM-AUTO-{datetime.now(timezone.utc).strftime('%H%M%S')}",
                "station_id": station_id,
                "sensor_type": sensor_type,
                "anomalous_val": f"{value} {unit}",
                "unit": unit,
                "detection_reason": reason,
                "severity": "CRITICAL",
                "status": "ANOMALY DETECTED",
                "detected_at": datetime.now(timezone.utc).isoformat(),
                "recommended_action": "Isolate reading from AI inference pipeline and schedule recalibration."
            }
            self.anomalies.insert(0, rec)
            return rec
        return None

    def get_all_anomalies(self) -> List[Dict[str, Any]]:
        return self.anomalies

    def update_anomaly_status(self, anomaly_id: str, action: str) -> Optional[Dict[str, Any]]:
        for a in self.anomalies:
            if a["id"] == anomaly_id:
                if action == "acknowledge":
                    a["status"] = "ACKNOWLEDGED"
                elif action == "maintenance":
                    a["status"] = "MAINTENANCE SCHEDULED"
                elif action == "resolve":
                    a["status"] = "RESOLVED"
                return a
        return None

anomaly_service = SensorAnomalyService()
