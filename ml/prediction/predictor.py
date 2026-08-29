"""
ML Inference Service for Landslide Susceptibility Estimation.
Implements the predictRisk(input) contract:
Returns: { probability, riskLevel, factors, confidence, modelVersion, isDemo }
"""

import math
from typing import Dict, Any
from ml.model_interface import ILandslideModel
from ml.preprocessing.cleaner import validate_and_clean_features

class LandslidePredictor(ILandslideModel):
    def __init__(self):
        self.model_version = "2.6.0-Ensemble-DEMO"
        self.is_demo_mode = True

    def preprocess(self, raw_features: Dict[str, Any]) -> Dict[str, float]:
        return validate_and_clean_features(raw_features)

    def calculate_infinite_slope_fs(self, slope_deg: float, pwp_kpa: float, soil_cohesion: float = 12.0, friction_angle_deg: float = 28.0) -> float:
        beta = math.radians(max(5.0, min(80.0, slope_deg)))
        phi = math.radians(friction_angle_deg)
        z = 3.0
        gamma = 18.5

        tau_d = gamma * z * math.sin(beta) * math.cos(beta)
        if tau_d <= 0.001:
            return 3.0

        total_normal = gamma * z * (math.cos(beta) ** 2)
        eff_normal = max(1.0, total_normal - pwp_kpa)
        tau_r = soil_cohesion + (eff_normal * math.tan(phi))
        return round(max(0.1, min(4.0, tau_r / tau_d)), 3)

    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        norm = self.preprocess(features)

        w_rain = 0.32
        w_sm = 0.24
        w_slope = 0.20
        w_pwp = 0.14
        w_tilt = 0.10

        c_rain = norm["rain_norm"] * w_rain * norm["lith_multiplier"]
        c_sm = norm["sm_norm"] * w_sm
        c_slope = norm["slope_norm"] * w_slope * norm["lith_multiplier"]
        c_pwp = norm["pwp_norm"] * w_pwp
        c_tilt = norm["tilt_norm"] * w_tilt

        raw_score = (c_rain + c_sm + c_slope + c_pwp + c_tilt) * 100.0
        risk_score = round(min(100.0, max(0.0, raw_score)), 1)
        fs = self.calculate_infinite_slope_fs(norm["raw_slope"], norm["raw_pwp"])

        if fs < 1.0:
            risk_score = max(risk_score, 88.0)
        elif fs < 1.25:
            risk_score = max(risk_score, 68.0)

        if risk_score >= 80.0 or fs < 1.0:
            risk_tier = "CRITICAL"
            color = "#ef4444"
            status_text = "CRITICAL / ACTIVE FAILURE"
        elif risk_score >= 60.0 or fs < 1.25:
            risk_tier = "HIGH"
            color = "#f97316"
            status_text = "HIGH RISK / SEVERE"
        elif risk_score >= 35.0:
            risk_tier = "MODERATE"
            color = "#f59e0b"
            status_text = "ELEVATED WATCH"
        else:
            risk_tier = "LOW"
            color = "#10b981"
            status_text = "STABLE EQUILIBRIUM"

        total_contrib = max(0.01, (c_rain + c_sm + c_slope + c_pwp + c_tilt))
        factors = {
            "Rainfall": round((c_rain / total_contrib) * 100, 1),
            "Soil Moisture": round((c_sm / total_contrib) * 100, 1),
            "Slope Angle": round((c_slope / total_contrib) * 100, 1),
            "Pore Water Pressure": round((c_pwp / total_contrib) * 100, 1),
            "Ground Movement / Tilt": round((c_tilt / total_contrib) * 100, 1)
        }

        # Return comprehensive contract supporting both standard and legacy schemas
        return {
            "probability": risk_score,
            "riskLevel": risk_tier,
            "risk_score": risk_score,
            "risk_tier": risk_tier,
            "risk_color": color,
            "factor_of_safety": fs,
            "stability_status": status_text,
            "factors": factors,
            "factor_breakdown": factors,
            "confidence": 0.94,
            "modelVersion": self.model_version,
            "model_version": self.model_version,
            "isDemo": self.is_demo_mode,
            "is_demo": self.is_demo_mode,
            "features_analyzed": norm
        }

predictor = LandslidePredictor()

def predictRisk(features: Dict[str, Any]) -> Dict[str, Any]:
    return predictor.predict(features)
