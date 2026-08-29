from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from ml import predictRisk

router = APIRouter(tags=["ML Prediction"])

class DirectPredictionRequest(BaseModel):
    slope_deg: float = Field(45.0, ge=5.0, le=85.0, description="Slope inclination angle in degrees")
    pore_water_pressure_kpa: float = Field(25.0, ge=0.0, le=120.0, description="Pore-water pressure in kPa")
    tilt_rate: float = Field(0.12, ge=0.0, le=10.0, description="Inclinometer tilt rate in mm/h")
    soil_moisture_pct: float = Field(70.0, ge=0.0, le=100.0, description="Soil volumetric moisture percentage")
    rainfall_24h_mm: float = Field(40.0, ge=0.0, le=500.0, description="24-hour cumulative rainfall in mm")
    rainfall_7d_mm: Optional[float] = Field(160.0, ge=0.0, le=2000.0, description="7-day cumulative rainfall in mm")
    elevation_m: Optional[float] = Field(1200.0, ge=0.0, le=8000.0, description="Elevation above sea level in meters")
    fault_dist_km: Optional[float] = Field(3.5, ge=0.0, le=100.0, description="Distance to nearest active fault in km")
    lithology: Optional[str] = Field("Weak Disang Shale", description="Geological class or rock formation")

@router.post("/api/predict")
async def run_direct_prediction(req: DirectPredictionRequest):
    return predictRisk(req.dict())
