from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from app.services.telemetry_service import telemetry_service
from app.services.alert_service import alert_service
from app.models.geotech_engine import geotech_engine
from ml import predictRisk

router = APIRouter(tags=["AI What-If Simulation Sandbox"])

class WhatIfSimulationRequest(BaseModel):
    station_id: Optional[str] = Field("STN-MAN-01", description="Target IoT station ID")
    state: Optional[str] = Field("Manipur", description="State name")
    rainfall_offset_pct: Optional[float] = Field(30.0, ge=-100.0, le=500.0, description="% Rainfall Increase/Decrease")
    moisture_offset_pct: Optional[float] = Field(10.0, ge=-100.0, le=100.0, description="% Soil Moisture Offset")
    pwp_offset_pct: Optional[float] = Field(15.0, ge=-100.0, le=300.0, description="% Pore Water Pressure Offset")
    ground_movement_offset_pct: Optional[float] = Field(20.0, ge=-100.0, le=500.0)
    slope_offset_deg: Optional[float] = Field(0.0, ge=-20.0, le=20.0)
    # Direct absolute values support
    slope_deg: Optional[float] = None
    rainfall_intensity_mm_hr: Optional[float] = None
    duration_hrs: Optional[float] = None
    pore_water_pressure_kpa: Optional[float] = None
    soil_moisture_pct: Optional[float] = None
    rainfall_24h_mm: Optional[float] = None
    rainfall_7d_mm: Optional[float] = None
    fault_dist_km: Optional[float] = None
    lithology: Optional[str] = None
    lulc: Optional[str] = None
    seismic_coeff_kh: Optional[float] = None

class DisasterScenarioRequest(BaseModel):
    station_id: str = Field("STN-MAN-01")
    scenario_type: str = Field("EXTREME_DELUGE", description="EXTREME_DELUGE | SEISMIC_SHOCK | DRAINAGE_FAILURE")

@router.post("/api/simulation/run")
@router.post("/api/simulate/whatif")
async def run_whatif_simulation(req: WhatIfSimulationRequest):
    stn_id = req.station_id or "STN-MAN-01"
    stn_details = telemetry_service.get_station_details(stn_id)
    if not stn_details:
        stn_details = telemetry_service.get_all_stations()[0]

    base = stn_details["current_readings"]
    stn = stn_details

    # Baseline prediction
    base_pred = predictRisk({
        "slope_deg": stn.get("slope_deg", 45.0),
        "pore_water_pressure_kpa": base["pore_water_pressure"],
        "tilt_rate": base["tilt_rate"],
        "soil_moisture_pct": base["soil_moisture"],
        "rainfall_24h_mm": base["rainfall_24h"],
        "lithology": stn.get("lithology", stn.get("geology_type", "Weak Disang Shale"))
    })

    # Simulated stress inputs (either direct or offset based)
    if req.slope_deg is not None:
        sim_slope = req.slope_deg
    else:
        sim_slope = max(5.0, min(85.0, stn.get("slope_deg", 45.0) + (req.slope_offset_deg or 0.0)))

    if req.rainfall_intensity_mm_hr is not None:
        sim_rain = req.rainfall_intensity_mm_hr * (req.duration_hrs or 6.0)
    elif req.rainfall_24h_mm is not None:
        sim_rain = req.rainfall_24h_mm
    elif req.rainfall_offset_pct is not None:
        sim_rain = max(0.0, base["rainfall_24h"] * (1.0 + req.rainfall_offset_pct / 100.0))
    else:
        sim_rain = base["rainfall_24h"]

    if req.pore_water_pressure_kpa is not None:
        sim_pwp = req.pore_water_pressure_kpa
    elif req.pwp_offset_pct is not None:
        sim_pwp = max(0.0, base["pore_water_pressure"] * (1.0 + req.pwp_offset_pct / 100.0))
    else:
        sim_pwp = base["pore_water_pressure"]

    if req.soil_moisture_pct is not None:
        sim_sm = req.soil_moisture_pct
    elif req.moisture_offset_pct is not None:
        sim_sm = min(100.0, max(0.0, base["soil_moisture"] * (1.0 + req.moisture_offset_pct / 100.0)))
    else:
        sim_sm = base["soil_moisture"]

    sim_tilt = max(0.0, base["tilt_rate"] * (1.0 + (req.ground_movement_offset_pct or 0.0) / 100.0))
    sim_litho = req.lithology or stn.get("geology_type", "Weak Disang Shale")

    sim_pred = predictRisk({
        "slope_deg": sim_slope,
        "pore_water_pressure_kpa": sim_pwp,
        "tilt_rate": sim_tilt,
        "soil_moisture_pct": sim_sm,
        "rainfall_24h_mm": sim_rain,
        "lithology": sim_litho
    })

    delta_risk = round(sim_pred["risk_score"] - base_pred["risk_score"], 1)

    # I-D calculation
    id_calc = geotech_engine.calculate_id_threshold(
        state=req.state or stn.get("state", "Manipur"),
        intensity_mm_hr=req.rainfall_intensity_mm_hr or (sim_rain / 6.0),
        duration_hrs=req.duration_hrs or 6.0
    )

    fs_calc = geotech_engine.calculate_factor_of_safety(
        slope_deg=sim_slope,
        pore_water_pressure_kpa=sim_pwp,
        seismic_coeff_kh=req.seismic_coeff_kh or 0.05
    )

    risk_score = sim_pred["risk_score"]
    risk_tier = sim_pred["risk_tier"]
    tier_color = "#dc2626" if risk_tier in ["CRITICAL", "RED"] else ("#f97316" if risk_tier in ["HIGH", "ORANGE"] else ("#f59e0b" if risk_tier in ["MODERATE", "YELLOW"] else "#10b981"))

    return {
        "status": "SUCCESS",
        "station_id": stn_id,
        "station_name": stn.get("name", "Monitoring Node"),
        "composite_risk_score": risk_score,
        "composite_tier": risk_tier,
        "composite_color": tier_color,
        "advisory": f"SIMULATED DIRECTIVE: Predicted Risk is {risk_tier} (Score: {risk_score}/100, Fs: {sim_pred['factor_of_safety']}). Follow disaster management protocols.",
        "current_conditions": {
            "rainfall_24h_mm": base["rainfall_24h"],
            "pore_water_pressure_kpa": base["pore_water_pressure"],
            "soil_moisture_pct": base["soil_moisture"],
            "tilt_rate_mm_h": base["tilt_rate"],
            "slope_deg": stn.get("slope_deg", 45.0),
            "factor_of_safety": base_pred["factor_of_safety"],
            "risk_score": base_pred["risk_score"],
            "risk_tier": base_pred["risk_tier"],
            "status_text": base_pred["stability_status"]
        },
        "simulated_offsets": {
            "rainfall_offset_pct": req.rainfall_offset_pct,
            "pwp_offset_pct": req.pwp_offset_pct,
            "moisture_offset_pct": req.moisture_offset_pct,
            "tilt_offset_pct": req.ground_movement_offset_pct,
            "slope_offset_deg": req.slope_offset_deg
        },
        "predicted_result": {
            "rainfall_24h_mm": round(sim_rain, 1),
            "pore_water_pressure_kpa": round(sim_pwp, 2),
            "soil_moisture_pct": round(sim_sm, 1),
            "tilt_rate_mm_h": round(sim_tilt, 3),
            "slope_deg": round(sim_slope, 1),
            "factor_of_safety": sim_pred["factor_of_safety"],
            "risk_score": sim_pred["risk_score"],
            "risk_tier": sim_pred["risk_tier"],
            "status_text": sim_pred["stability_status"],
            "probability_change_pct": delta_risk,
            "factor_breakdown": sim_pred["factor_breakdown"],
            "contributing_factors": sim_pred["factor_breakdown"]
        },
        "rainfall_id_threshold": id_calc,
        "factor_of_safety_analysis": fs_calc,
        "ai_susceptibility_model": sim_pred,
        "disclaimer": "SIMULATION — NOT A REAL-WORLD GUARANTEE",
        "is_simulation_disclaimer": "SIMULATION — NOT A REAL-WORLD GUARANTEE",
        "is_demo": True
    }

@router.post("/api/simulate/disaster-scenario")
async def trigger_disaster_scenario(req: DisasterScenarioRequest):
    updated = telemetry_service.update_telemetry_tick(storm_intensity_multiplier=3.5)
    target_stn = next((s for s in updated if s["id"] == req.station_id), updated[0] if updated else None)

    if target_stn:
        target_stn["current_readings"]["rainfall_1h"] = 42.0
        target_stn["current_readings"]["rainfall_24h"] = 128.0
        target_stn["current_readings"]["pore_water_pressure"] = 44.5
        target_stn["current_readings"]["tilt_rate"] = 0.68
        target_stn["current_readings"]["soil_moisture"] = 94.0
        target_stn["current_readings"]["factor_of_safety"] = 0.42
        target_stn["current_readings"]["risk_score"] = 98.2
        target_stn["current_readings"]["warning_level"] = "RED"
        target_stn["current_readings"]["status_text"] = "DISASTER SCENARIO ACTIVE"

    new_alert = alert_service.generate_dynamic_bulletin(
        station_id=req.station_id,
        region_name="Tupul Railway Yard Sentinel, Noney",
        state="Manipur",
        severity="Extreme",
        headline="CRITICAL DELUGE FAILURE ADVISORY",
        description="Extreme storm scenario injected. Pore water pressure exceeds safety threshold."
    )

    return {
        "status": "SCENARIO_INJECTED",
        "scenario": req.scenario_type,
        "station_affected": req.station_id,
        "resulting_alert": new_alert,
        "message": "Disaster scenario successfully simulated. High-risk CAP bulletin generated.",
        "is_demo": True
    }
