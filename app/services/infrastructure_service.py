"""
Infrastructure Risk & Vulnerability Impact Analyzer for NER.
Monitors critical highways, railway bridges/tunnels, power grids, and public lifelines.
"""

import math
from typing import List, Dict, Any, Optional
from app.data.ner_geospatial import NER_INFRASTRUCTURE

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2.0)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 2)

class InfrastructureService:
    def __init__(self):
        self.assets = NER_INFRASTRUCTURE

    def get_all_infrastructure(self, state: Optional[str] = None) -> List[Dict[str, Any]]:
        if state and state.upper() != "ALL":
            return [a for a in self.assets if a.get("state", "").lower() == state.lower()]
        return self.assets

    def evaluate_impact_around_zone(self, origin_lat: float, origin_lng: float, radius_km: float = 15.0) -> List[Dict[str, Any]]:
        """
        Calculates distance and assigns dynamic risk levels to all infrastructure within the impact radius.
        """
        impacted = []
        for asset in self.assets:
            dist = haversine_distance_km(origin_lat, origin_lng, asset["latitude"], asset["longitude"])
            if dist <= radius_km:
                if dist <= 1.5:
                    risk_level = "CRITICAL"
                    status = "IMMINENT THREAT / STRUCTURAL ALERT"
                elif dist <= 3.5:
                    risk_level = "HIGH"
                    status = "HIGH WATCH / RESTRICTED SPEEDS"
                elif dist <= 8.0:
                    risk_level = "MODERATE"
                    status = "ADVISORY WATCH"
                else:
                    risk_level = "LOW"
                    status = "NORMAL OPERATIONAL"

                item = dict(asset)
                item["distance_km"] = dist
                item["calculated_risk_level"] = risk_level
                item["impact_status"] = status
                impacted.append(item)

        impacted.sort(key=lambda x: x["distance_km"])
        return impacted

infrastructure_service = InfrastructureService()
