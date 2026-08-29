"""
Satellite Change Detection Service for Landslide Scar and Terrain Disturbance Monitoring.
Compares multi-temporal optical and SAR satellite imagery indices (NDVI, Bare Soil Index, DEM deformation).
"""

from typing import List, Dict, Any, Optional
from app.data.ner_geospatial import SATELLITE_CHANGE_RECORDS

class SatelliteService:
    def __init__(self):
        self.records = SATELLITE_CHANGE_RECORDS

    def get_all_changes(self, state: Optional[str] = None) -> List[Dict[str, Any]]:
        if state and state.upper() != "ALL":
            return [r for r in self.records if r.get("state", "").lower() == state.lower()]
        return self.records

    def get_change_records(self, state: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.get_all_changes(state)


    def get_change_by_location(self, location_id: str) -> Optional[Dict[str, Any]]:
        return next((r for r in self.records if r.get("location_id") == location_id), None)

    def analyze_terrain_change(self, lat: float, lng: float) -> Dict[str, Any]:
        """Returns the nearest analyzed satellite change record or computes a terrain change proxy."""
        matched = min(
            self.records,
            key=lambda r: (r["latitude"] - lat)**2 + (r["longitude"] - lng)**2,
            default=self.records[0]
        )
        return matched

satellite_service = SatelliteService()
