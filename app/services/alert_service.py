"""
Alert Service for Multi-Tier Early Warning and CAP 1.2 Protocol Bulletin Generation.
"""

from datetime import datetime, timezone
from typing import List, Dict, Any
from app.database import get_active_alerts, insert_alert, get_db_connection

class AlertService:
    def get_all_active_alerts(self) -> List[Dict[str, Any]]:
        alerts = get_active_alerts()
        if not alerts:
            # Seed standard monitoring advisory if table is empty
            self._seed_default_advisories()
            alerts = get_active_alerts()
        return alerts

    def _seed_default_advisories(self):
        now = datetime.now(timezone.utc)
        default_alerts = [
            {
                "alert_id": f"CAP-ALERT-MAN-01-{int(now.timestamp())}",
                "station_id": "STN-MAN-01",
                "region_name": "Tupul Railway Yard Sentinel",
                "state": "Manipur",
                "severity": "Severe",
                "event_type": "Landslide High Hazard Warning",
                "headline": "ORANGE WARNING: Saturated Shale Slopes at Tupul-Noney Corridor",
                "description": "Continuous monsoonal precipitation has elevated pore water pressure to 28.0 kPa with continuous micro-seismic activity detected. Critical I-D threshold is at 88% capacity.",
                "instruction": "Heavy vehicular transport restricted on NH-37. Construction crews at railway cuttings ordered to pull back to high ground shelters.",
                "coordinates": [24.7083, 93.6500]
            },
            {
                "alert_id": f"CAP-ALERT-SIK-01-{int(now.timestamp())}",
                "station_id": "STN-SIK-01",
                "region_name": "Gangtok - 29th Mile Observatory",
                "state": "Sikkim",
                "severity": "Moderate",
                "event_type": "Geotechnical Sinking Advisory",
                "headline": "YELLOW ADVISORY: Creep Displacement Detected on NH-10 Corridor",
                "description": "Biaxial inclinometers record 0.08 mm/hr creep. Teesta river scouring toe of slope near 29th Mile.",
                "instruction": "Border Roads Organisation (BRO) quick clearance dozers placed on standby at Singtam and Rangpo checkposts.",
                "coordinates": [27.2340, 88.5240]
            }
        ]
        for a in default_alerts:
            insert_alert(a)

    def generate_cap_xml_bulletin(self, alert: Dict[str, Any]) -> str:
        """
        Generates OASIS / ITU-T Common Alerting Protocol (CAP v1.2) compliant XML payload.
        """
        now = datetime.now(timezone.utc).isoformat()
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<alert xmlns="urn:oasis:names:tc:emergency:cap:1.2">
    <identifier>{alert.get('alert_id', 'NER-LEWS-ALERT')}</identifier>
    <sender>NER-LEWS@ndma.gov.in</sender>
    <sent>{now}</sent>
    <status>Actual</status>
    <msgType>Alert</msgType>
    <scope>Public</scope>
    <info>
        <category>Geo</category>
        <event>{alert.get('event_type', 'Landslide Early Warning')}</event>
        <urgency>Immediate</urgency>
        <severity>{alert.get('severity', 'Severe')}</severity>
        <certainty>Observed</certainty>
        <eventCode>
            <valueName>SAME</valueName>
            <value>LSW</value>
        </eventCode>
        <headline>{alert.get('headline')}</headline>
        <description>{alert.get('description')}</description>
        <instruction>{alert.get('instruction')}</instruction>
        <area>
            <areaDesc>{alert.get('region_name')}, {alert.get('state')}</areaDesc>
            <circle>{alert.get('coordinates')},5.0</circle>
        </area>
    </info>
</alert>"""

    def generate_dynamic_bulletin(self, station_id: str, region_name: str, state: str, severity: str, headline: str, description: str, instruction: str = "", coordinates: List[float] = None) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        alert_id = f"CAP-ALERT-{station_id}-{int(now.timestamp())}"
        alert_data = {
            "alert_id": alert_id,
            "station_id": station_id,
            "region_name": region_name,
            "state": state,
            "severity": severity,
            "event_type": "Landslide Emergency Bulletin",
            "headline": headline,
            "description": description,
            "instruction": instruction or "Execute high-ground evacuation to nearest verified shelter immediately.",
            "coordinates": coordinates or [24.7083, 93.6500]
        }
        insert_alert(alert_data)
        return alert_data

alert_service = AlertService()

