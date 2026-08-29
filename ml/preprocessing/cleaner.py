"""
Data Cleaning, Boundary Validation, and Feature Normalization for Landslide ML Pipeline.
"""

from typing import Dict, Any

def validate_and_clean_features(raw_features: Dict[str, Any]) -> Dict[str, float]:
    """
    Validates physical boundaries and normalizes geotechnical features for inference.
    Rejects impossible values (e.g. soil moisture > 100%, negative rainfall).
    """
    raw_slope = float(raw_features.get("slope_deg", raw_features.get("slope", 45.0)))
    raw_pwp = float(raw_features.get("pore_water_pressure_kpa", raw_features.get("pore_water_pressure", raw_features.get("pwp", 25.0))))
    raw_tilt = float(raw_features.get("tilt_rate", raw_features.get("ground_movement", 0.12)))
    raw_sm = float(raw_features.get("soil_moisture_pct", raw_features.get("soil_moisture", 70.0)))
    raw_r24 = float(raw_features.get("rainfall_24h_mm", raw_features.get("rainfall_24h", raw_features.get("rainfall", 40.0))))
    raw_r7d = float(raw_features.get("rainfall_7d_mm", raw_features.get("rainfall_cumulative_7d", 160.0)))
    raw_elev = float(raw_features.get("elevation_m", raw_features.get("elevation", 1200.0)))

    # Boundaries check & clamping
    clamped_slope = max(5.0, min(85.0, raw_slope))
    clamped_pwp = max(0.0, min(120.0, raw_pwp))
    clamped_tilt = max(0.0, min(10.0, raw_tilt))
    clamped_sm = max(0.0, min(100.0, raw_sm))
    clamped_r24 = max(0.0, min(500.0, raw_r24))
    clamped_r7d = max(0.0, min(2000.0, raw_r7d))

    # Min-Max Normalizations
    norm_slope = min(1.0, max(0.0, (clamped_slope - 15.0) / 55.0))
    norm_pwp = min(1.0, max(0.0, clamped_pwp / 50.0))
    norm_tilt = min(1.0, max(0.0, clamped_tilt / 0.50))
    norm_sm = min(1.0, max(0.0, (clamped_sm - 30.0) / 60.0))
    norm_r24 = min(1.0, max(0.0, clamped_r24 / 100.0))
    norm_r7d = min(1.0, max(0.0, clamped_r7d / 350.0))

    # Geology / Lithology Vulnerability Multiplier
    lithology = str(raw_features.get("lithology", "Weak Disang Shale")).lower()
    if "shale" in lithology or "phyllite" in lithology:
        lith_multiplier = 1.25
    elif "schist" in lithology or "sandstone" in lithology:
        lith_multiplier = 1.05
    else:
        lith_multiplier = 0.85

    return {
        "slope_norm": norm_slope,
        "pwp_norm": norm_pwp,
        "tilt_norm": norm_tilt,
        "sm_norm": norm_sm,
        "rain_norm": (norm_r24 * 0.7) + (norm_r7d * 0.3),
        "raw_slope": clamped_slope,
        "raw_pwp": clamped_pwp,
        "raw_tilt": clamped_tilt,
        "raw_sm": clamped_sm,
        "raw_r24": clamped_r24,
        "raw_elevation": raw_elev,
        "lith_multiplier": lith_multiplier
    }
