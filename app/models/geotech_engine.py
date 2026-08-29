"""
Geotechnical and Hydro-Meteorological Engineering Engine for Landslide Early Warning in NER.
Calculates Rainfall Intensity-Duration (I-D) Thresholds, Factor of Safety (Fs),
and Inverse Velocity Displacement Failure Acceleration.
"""

import math
from typing import Dict, Any, Tuple

# Regional I-D Empirical Threshold Parameters (I = alpha * D^-beta)
# Calibrated for North Eastern Region geographical sub-units
REGION_ID_PARAMS = {
    "Eastern Himalayas": {"alpha": 14.8, "beta": 0.42, "description": "Sikkim, North Bengal & Arunachal High Slopes"},
    "Shillong Plateau": {"alpha": 24.5, "beta": 0.35, "description": "Meghalaya (Cherrapunji / Mawsynram Escarpments)"},
    "Indo-Burman Ranges": {"alpha": 12.2, "beta": 0.45, "description": "Manipur, Nagaland & Mizoram Sedimentary Ridges"},
    "Brahmaputra/Barak Hills": {"alpha": 15.5, "beta": 0.40, "description": "Dima Hasao & Karbi Anglong Hill Tracts"}
}

class GeotechnicalEngine:
    def calculate_id_threshold(self, state: str, intensity_mm_hr: float, duration_hrs: float) -> Dict[str, Any]:
        """
        Calculates whether current/forecast rainfall exceeds critical I-D threshold.
        """
        duration = max(1.0, float(duration_hrs))
        intensity = max(0.0, float(intensity_mm_hr))

        if state in ["Sikkim", "Arunachal Pradesh"]:
            params = REGION_ID_PARAMS["Eastern Himalayas"]
        elif state == "Meghalaya":
            params = REGION_ID_PARAMS["Shillong Plateau"]
        elif state in ["Manipur", "Nagaland", "Mizoram"]:
            params = REGION_ID_PARAMS["Indo-Burman Ranges"]
        else:
            params = REGION_ID_PARAMS["Brahmaputra/Barak Hills"]

        alpha = params["alpha"]
        beta = params["beta"]

        # Critical intensity I_crit = alpha * D^(-beta)
        i_crit = alpha * math.pow(duration, -beta)
        
        # Cumulative rainfall over the duration
        cumulative_rainfall = intensity * duration
        cumulative_critical = i_crit * duration

        # Ratio of actual vs critical
        ratio = intensity / max(0.01, i_crit)

        if ratio < 0.60:
            stage = "GREEN - NORMAL"
            color = "#10B981"
            description = "Precipitation within safe infiltration capacity of slope overburden."
        elif ratio < 0.85:
            stage = "YELLOW - ADVISORY"
            color = "#F59E0B"
            description = "Rainfall approaching geotechnical threshold. Heightened saturation in progress."
        elif ratio < 1.15:
            stage = "ORANGE - WARNING"
            color = "#F97316"
            description = "Rainfall threshold breached! High probability of shallow debris flows and cut-slope washouts."
        else:
            stage = "RED - CRITICAL EVACUATION"
            color = "#DC2626"
            description = "CRITICAL DELUGE! Severe multiple slope failures imminent. Immediate evacuation & road closure required."

        return {
            "intensity_mm_hr": round(intensity, 2),
            "duration_hrs": round(duration, 1),
            "i_critical_threshold": round(i_crit, 2),
            "cumulative_rainfall_mm": round(cumulative_rainfall, 1),
            "cumulative_critical_mm": round(cumulative_critical, 1),
            "threshold_breach_ratio": round(ratio, 2),
            "threshold_percentage": round(ratio * 100, 1),
            "stage": stage,
            "color": color,
            "description": description,
            "region_model": params["description"]
        }

    def calculate_factor_of_safety(
        self,
        slope_deg: float = 45.0,
        pore_water_pressure_kpa: float = 20.0,
        soil_cohesion_kpa: float = 12.0,
        friction_angle_deg: float = 30.0,
        soil_depth_m: float = 3.0,
        soil_unit_weight_kn_m3: float = 18.5,
        seismic_coeff_kh: float = 0.0
    ) -> Dict[str, Any]:
        """
        Computes the Factor of Safety (Fs) using the Limit Equilibrium Infinite Slope Model
        with pore water pressure and pseudo-static seismic acceleration.
        
        Fs = [ c' + (gamma * z * cos^2(beta) - u) * tan(phi') - kh * W * sin(beta) ] / 
             [ gamma * z * sin(beta) * cos(beta) + kh * W * cos(beta) ]
        """
        beta_rad = math.radians(max(5.0, min(85.0, slope_deg)))
        phi_rad = math.radians(max(5.0, min(50.0, friction_angle_deg)))
        
        gamma = soil_unit_weight_kn_m3
        z = max(1.0, soil_depth_m)
        c_prime = max(0.0, soil_cohesion_kpa)
        u = max(0.0, pore_water_pressure_kpa)
        kh = max(0.0, seismic_coeff_kh)

        # Normal stress on slip surface: sigma_n = gamma * z * cos^2(beta)
        sigma_n = gamma * z * (math.cos(beta_rad) ** 2)
        
        # Effective normal stress: sigma_prime = max(0, sigma_n - u)
        sigma_prime = max(0.0, sigma_n - u)

        # Resisting Shear Strength (Numerator)
        # S = c' + sigma_prime * tan(phi')
        resisting_force = c_prime + (sigma_prime * math.tan(phi_rad))

        # Driving Shear Stress (Denominator)
        # Tau = gamma * z * sin(beta) * cos(beta) + seismic inertial force
        driving_force = (gamma * z * math.sin(beta_rad) * math.cos(beta_rad)) + (kh * gamma * z * math.cos(beta_rad))
        driving_force = max(0.01, driving_force)

        # Factor of Safety
        fs = resisting_force / driving_force
        fs = round(max(0.1, min(5.0, fs)), 3)

        if fs >= 1.50:
            stability_status = "STABLE"
            status_color = "#10B981"
            safety_margin = "High safety reserve under current geotechnical stress."
        elif fs >= 1.20:
            stability_status = "MARGINALLY STABLE"
            status_color = "#F59E0B"
            safety_margin = "Adequate under dry conditions; vulnerable to heavy pore pressure buildup."
        elif fs >= 1.00:
            stability_status = "HIGH FAILURE RISK"
            status_color = "#F97316"
            safety_margin = "Slope is near critical equilibrium. Any additional rainfall or vibration will initiate sliding."
        else:
            stability_status = "IMMINENT COLLAPSE / FAILURE ACTIVE"
            status_color = "#DC2626"
            safety_margin = "Driving shear stress exceeds resisting shear strength. Active catastrophic displacement."

        return {
            "factor_of_safety": fs,
            "resisting_strength_kpa": round(resisting_force, 2),
            "driving_stress_kpa": round(driving_force, 2),
            "effective_normal_stress_kpa": round(sigma_prime, 2),
            "pore_pressure_kpa": round(u, 2),
            "stability_status": stability_status,
            "status_color": status_color,
            "safety_margin": safety_margin
        }

    def predict_failure_time_inverse_velocity(self, tilt_rate_mm_hr: float, acceleration_mm_hr2: float) -> Dict[str, Any]:
        """
        Saito / Fukuzono Inverse Velocity method (1/v vs time).
        When 1/v -> 0, failure time Tf is reached.
        """
        v = max(0.001, float(tilt_rate_mm_hr))
        a = float(acceleration_mm_hr2)

        if v < 0.1 and a <= 0:
            return {
                "estimated_failure_hours": None,
                "status": "DORMANT / STABLE CREEP",
                "inverse_velocity": round(1.0 / v, 2)
            }

        # If accelerating
        if a > 0.01:
            hours_to_collapse = round(v / (a * 2.0), 1)
            hours_to_collapse = max(0.5, min(72.0, hours_to_collapse))
            return {
                "estimated_failure_hours": hours_to_collapse,
                "status": f"ACCELERATING FAILURE (Est. {hours_to_collapse} hrs to runaway collapse)",
                "inverse_velocity": round(1.0 / v, 2)
            }
        else:
            return {
                "estimated_failure_hours": None,
                "status": "STEADY-STATE CREEP",
                "inverse_velocity": round(1.0 / v, 2)
            }

geotech_engine = GeotechnicalEngine()
