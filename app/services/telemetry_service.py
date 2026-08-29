"""
IoT Sensor Telemetry Service.
Maintains state, generates real-time telemetry, logs timeseries, and detects anomalies.
"""

import time
import math
import random
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from app.data.ner_geospatial import IOT_STATIONS, NER_STATES
from app.models.ml_engine import ml_engine
from app.models.geotech_engine import geotech_engine
from app.database import log_telemetry_reading, insert_alert

class TelemetryService:
    def __init__(self):
        self.stations: Dict[str, Dict[str, Any]] = {}
        self.history: Dict[str, List[Dict[str, Any]]] = {}
        self._init_stations()

    def _init_stations(self):
        current_time = datetime.now(timezone.utc)
        for stn in IOT_STATIONS:
            stn_id = stn["id"]
            base = stn["baseline"]
            
            # Geotechnical initial evaluation
            fs_res = geotech_engine.calculate_factor_of_safety(
                slope_deg=stn.get("slope_deg", 45.0),
                pore_water_pressure_kpa=base["pwp"]
            )
            fs_val = fs_res["factor_of_safety"]

            if fs_val < 1.0 or base["tilt_rate"] > 0.25:
                warning_level = "RED"
                status_text = "CRITICAL FAILURE IMMINENT"
                risk_score = 94.8
                rain_24h = 68.4
            elif fs_val < 1.25 or base["tilt_rate"] > 0.10:
                warning_level = "ORANGE"
                status_text = "SEVERE RISK WATCH"
                risk_score = 78.4
                rain_24h = 42.0
            elif fs_val < 1.45:
                warning_level = "YELLOW"
                status_text = "ELEVATED ADVISORY"
                risk_score = 48.0
                rain_24h = 24.0
            else:
                warning_level = "GREEN"
                status_text = "STABLE EQUILIBRIUM"
                risk_score = 18.0
                rain_24h = 12.0

            self.stations[stn_id] = {
                **stn,
                "current_readings": {
                    "rainfall_1h": round(rain_24h / 12.0, 1),
                    "rainfall_24h": rain_24h,
                    "rainfall_cumulative_7d": round(rain_24h * 3.5, 1),
                    "pore_water_pressure": base["pwp"],
                    "tilt_rate": base["tilt_rate"],
                    "soil_moisture": base["soil_moisture"],
                    "vibration_freq": base["vibration"],
                    "factor_of_safety": fs_val,
                    "risk_score": risk_score,
                    "warning_level": warning_level,
                    "status_text": status_text,
                    "last_updated": current_time.isoformat()
                }
            }
            # Pre-populate 24 hours of realistic history for chart rendering
            self.history[stn_id] = []
            for h in range(24, 0, -1):
                hist_time = current_time - timedelta(hours=h)
                hour_factor = math.sin((hist_time.hour / 24.0) * math.pi * 2)
                sim_rain_1h = max(0.0, round(2.0 + hour_factor * 3.5 + random.uniform(-0.5, 1.5), 1))
                sim_pwp = round(base["pwp"] + hour_factor * 4.0 + random.uniform(-0.5, 0.8), 2)
                sim_tilt = round(base["tilt_rate"] + random.uniform(0.0, 0.02), 3)
                sim_sm = round(base["soil_moisture"] + hour_factor * 3.0 + random.uniform(-1, 1), 1)
                sim_fs = round(max(0.45, fs_val + hour_factor * 0.15), 2)

                self.history[stn_id].append({
                    "timestamp": hist_time.strftime("%H:%M"),
                    "rainfall_1h": sim_rain_1h,
                    "pore_water_pressure": sim_pwp,
                    "tilt_rate": sim_tilt,
                    "soil_moisture": sim_sm,
                    "factor_of_safety": sim_fs,
                    "risk_score": round(max(5.0, min(95.0, (1.8 - sim_fs) * 60 + sim_sm * 0.3)), 1)
                })


    def update_telemetry_tick(self, storm_intensity_multiplier: float = 1.0) -> List[Dict[str, Any]]:
        """
        Simulates dynamic sensor tick across all stations.
        """
        now = datetime.now(timezone.utc)
        updated_stations = []

        for stn_id, stn_data in self.stations.items():
            base = stn_data["baseline"]
            
            # Simulate natural stochastic variations + regional rainfall conditions
            # High rain in Sohra/Cherrapunji, Tupul, and 29th Mile Sikkim
            is_rain_heavy_hub = stn_id in ["STN-MEG-01", "STN-SIK-01", "STN-MAN-01", "STN-ASM-01"]
            rain_bias = 6.0 if is_rain_heavy_hub else 1.5

            noise_rain = random.uniform(-0.8, 1.8)
            rain_1h = max(0.0, round((rain_bias + noise_rain) * storm_intensity_multiplier, 1))
            rain_24h = round(stn_data["current_readings"]["rainfall_24h"] * 0.98 + rain_1h, 1)
            rain_7d = round(stn_data["current_readings"]["rainfall_cumulative_7d"] * 0.99 + (rain_1h * 0.8), 1)

            # Pore pressure increases with rainfall infiltration
            pwp_delta = (rain_1h * 0.45) - 0.2
            pwp = max(base["pwp"], round(stn_data["current_readings"]["pore_water_pressure"] + pwp_delta + random.uniform(-0.2, 0.3), 2))

            # Soil moisture
            sm_delta = (rain_1h * 0.6) - 0.1
            sm = min(98.0, max(base["soil_moisture"], round(stn_data["current_readings"]["soil_moisture"] + sm_delta, 1)))

            # Geophone micro-vibration
            vib = round(base["vibration"] + (rain_1h * 0.08) + random.uniform(-0.1, 0.2), 2)

            # Inclinometer tilt rate (increases when pore pressure is elevated)
            tilt_multiplier = 1.0 + max(0.0, (pwp - 25.0) * 0.15)
            tilt_rate = round(base["tilt_rate"] * tilt_multiplier + random.uniform(0.001, 0.01), 3)

            # Compute Factor of Safety
            fs_result = geotech_engine.calculate_factor_of_safety(
                slope_deg=stn_data["slope_deg"],
                pore_water_pressure_kpa=pwp,
                soil_cohesion_kpa=14.0,
                friction_angle_deg=29.0,
                soil_depth_m=3.2
            )
            fs = fs_result["factor_of_safety"]

            # Compute ML Susceptibility Risk
            ml_pred = ml_engine.predict_susceptibility({
                "slope_deg": stn_data["slope_deg"],
                "elevation_m": stn_data["elevation_m"],
                "soil_moisture_pct": sm,
                "rainfall_7d_mm": rain_7d,
                "fault_dist_km": 3.0,
                "lithology_code": 3 if "Shale" in stn_data["lithology"] or "Phyllite" in stn_data["lithology"] else 2,
                "lulc_code": 3
            })

            risk_score = ml_pred["risk_score"]
            tier = ml_pred["tier"]

            # Set warning level
            if fs < 1.0 or risk_score >= 90:
                warning_level = "RED"
                status_text = "CRITICAL / IMMINENT FAILURE"
            elif fs < 1.20 or risk_score >= 75:
                warning_level = "ORANGE"
                status_text = "WARNING / HIGH INSTABILITY"
            elif fs < 1.40 or risk_score >= 45:
                warning_level = "YELLOW"
                status_text = "ADVISORY / WATCH"
            else:
                warning_level = "GREEN"
                status_text = "NORMAL / STABLE"

            # Update in-memory state
            reading_dict = {
                "rainfall_1h": rain_1h,
                "rainfall_24h": rain_24h,
                "rainfall_cumulative_7d": rain_7d,
                "pore_water_pressure": pwp,
                "tilt_rate": tilt_rate,
                "soil_moisture": sm,
                "vibration_freq": vib,
                "factor_of_safety": fs,
                "risk_score": risk_score,
                "warning_level": warning_level,
                "status_text": status_text,
                "last_updated": now.isoformat()
            }
            stn_data["current_readings"] = reading_dict

            # Append to timeseries
            self.history[stn_id].append({
                "timestamp": now.strftime("%H:%M:%S"),
                "rainfall_1h": rain_1h,
                "pore_water_pressure": pwp,
                "tilt_rate": tilt_rate,
                "soil_moisture": sm,
                "factor_of_safety": fs,
                "risk_score": risk_score
            })
            if len(self.history[stn_id]) > 40:
                self.history[stn_id].pop(0)

            # Persist to SQLite
            log_telemetry_reading({
                "station_id": stn_id,
                **reading_dict
            })

            updated_stations.append({
                **stn_data,
                "current_readings": reading_dict
            })

        return updated_stations

    def get_all_stations(self) -> List[Dict[str, Any]]:
        return list(self.stations.values())

    def get_station_details(self, station_id: str) -> Optional[Dict[str, Any]]:
        stn = self.stations.get(station_id)
        if not stn:
            return None
        return {
            **stn,
            "timeseries_history": self.history.get(station_id, [])
        }

    def inject_disaster_scenario(self, station_id: str, intensity: str = "EXTREME_DELUGE"):
        """
        Allows live demonstration of catastrophe / early warning alarm triggers.
        """
        stn = self.stations.get(station_id)
        if not stn:
            return
        
        now = datetime.now(timezone.utc)
        if intensity == "EXTREME_DELUGE":
            stn["current_readings"]["rainfall_1h"] = 78.5
            stn["current_readings"]["rainfall_24h"] = 390.0
            stn["current_readings"]["rainfall_cumulative_7d"] = 580.0
            stn["current_readings"]["pore_water_pressure"] = 52.4
            stn["current_readings"]["tilt_rate"] = 0.85
            stn["current_readings"]["soil_moisture"] = 96.5
            stn["current_readings"]["vibration_freq"] = 6.8
            stn["current_readings"]["factor_of_safety"] = 0.88
            stn["current_readings"]["risk_score"] = 96.8
            stn["current_readings"]["warning_level"] = "RED"
            stn["current_readings"]["status_text"] = "CRITICAL / RUNAWAY FAILURE IMMINENT"
            stn["current_readings"]["last_updated"] = now.isoformat()
            
            # Record CAP alert
            insert_alert({
                "alert_id": f"CAP-ALERT-{station_id}-{int(now.timestamp())}",
                "station_id": station_id,
                "region_name": stn["name"],
                "state": stn["state"],
                "severity": "Extreme",
                "event_type": "Catastrophic Landslide Early Warning",
                "headline": f"CRITICAL RED ALERT: Imminent Slope Collapse at {stn['name']}",
                "description": f"Telemetry at {stn['name']} ({stn['corridor']}) records extreme pore water pressure (52.4 kPa) and accelerated displacement tilt (0.85 mm/hr). Factor of safety has plunged below 1.0 (Fs = 0.88).",
                "instruction": f"IMMEDIATE EVACUATION MANDATED. Shut down traffic along {stn['corridor']}. Dispatch SDRF/NDRF rescue units and sound community sirens immediately.",
                "coordinates": [stn["lat"], stn["lng"]]
            })

telemetry_service = TelemetryService()
