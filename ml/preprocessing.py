"""
Feature Preprocessing and Transformation Pipeline for Landslide ML Modeling.
Encodes geotechnical lithology, land-use land-cover (LULC), and normalizes hydro-meteorological inputs.
"""

from typing import Dict, Any

LITHOLOGY_WEIGHTS = {
    "weak disang shale": 1.45,
    "daling phyllite": 1.40,
    "weathered silt": 1.35,
    "sandstone": 1.10,
    "limestone": 1.05,
    "mica schist": 1.00,
    "quartzite": 0.85,
    "hard granite": 0.60,
    "massive gneiss": 0.65
}

LULC_WEIGHTS = {
    "highway road cut": 1.40,
    "railway excavation": 1.35,
    "urban settlement": 1.30,
    "deforested slope": 1.25,
    "agricultural terrace": 1.00,
    "dense forest": 0.70
}

def normalize_features(raw_features: Dict[str, Any]) -> Dict[str, float]:
    """
    Cleans, clips, and transforms raw sensor/terrain features into standard ML inputs.
    """
    # 1. Slope Steepness in degrees (range 0 - 90, clamped)
    slope_deg = float(raw_features.get("slope_deg", 35.0))
    slope_norm = min(1.0, max(0.0, slope_deg / 70.0))

    # 2. Pore Water Pressure in kPa (baseline ~ 5-50 kPa)
    pwp_kpa = float(raw_features.get("pore_water_pressure_kpa", raw_features.get("pore_water_pressure", 20.0)))
    pwp_norm = min(1.0, max(0.0, pwp_kpa / 50.0))

    # 3. Inclinometer Tilt Rate in mm/hr (baseline ~ 0.01 - 1.0 mm/hr)
    tilt_rate = float(raw_features.get("tilt_rate", raw_features.get("tilt_mm_hr", 0.05)))
    tilt_norm = min(1.0, max(0.0, tilt_rate / 0.50))

    # 4. Volumetric Soil Moisture in % (range 0 - 100)
    soil_moisture = float(raw_features.get("soil_moisture_pct", raw_features.get("soil_moisture", 50.0)))
    sm_norm = min(1.0, max(0.0, soil_moisture / 100.0))

    # 5. Rainfall 24h and 7-day cumulative in mm
    rain_24h = float(raw_features.get("rainfall_24h_mm", raw_features.get("rainfall_24h", 30.0)))
    rain_7d = float(raw_features.get("rainfall_7d_mm", raw_features.get("rainfall_cumulative_7d", 120.0)))
    rain_norm = min(1.0, max(0.0, (rain_24h * 0.6 + (rain_7d / 7.0) * 0.4) / 100.0))

    # 6. Lithology vulnerability factor
    lith_str = str(raw_features.get("lithology", "Weak Disang Shale")).lower()
    lith_factor = 1.0
    for k, v in LITHOLOGY_WEIGHTS.items():
        if k in lith_str:
            lith_factor = v
            break

    # 7. Fault Line Proximity in km (closer = higher vulnerability)
    fault_dist = float(raw_features.get("fault_dist_km", 5.0))
    fault_norm = min(1.0, max(0.0, 1.0 - (fault_dist / 15.0)))

    return {
        "slope_norm": slope_norm,
        "pwp_norm": pwp_norm,
        "tilt_norm": tilt_norm,
        "sm_norm": sm_norm,
        "rain_norm": rain_norm,
        "lith_factor": lith_factor,
        "fault_norm": fault_norm,
        "raw_slope": slope_deg,
        "raw_pwp": pwp_kpa,
        "raw_tilt": tilt_rate,
        "raw_sm": soil_moisture,
        "raw_rain_24h": rain_24h,
        "raw_rain_7d": rain_7d
    }
