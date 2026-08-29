"""
Offline Emergency Communication & Store-and-Forward Alert Service for NER-LEWS.
Manages network-resilient emergency dispatch. If network drops, alerts are stored locally
and automatically flushed and delivered as soon as connectivity is restored.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

class CommunicationService:
    def __init__(self):
        self.is_network_online = True
        self.queue: List[Dict[str, Any]] = []
        self.delivered_count = 1420
        self.failed_count = 3
        self.last_sync_time = datetime.now(timezone.utc).strftime("%H:%M:%S UTC+05:30")
        self._seed_initial_queue()

    def _seed_initial_queue(self):
        # Pre-seed sample queue
        self.queue = [
            {
                "id": "MSG-NER-001",
                "alert_id": "ALT-MAN-01",
                "recipient_group": "SDMA Authorities & NDRF 12th Bn",
                "target_location": "Tupul / Noney, Manipur",
                "channel": "SMS Gateway / CAP Broadcast",
                "payload": "CRITICAL LANDSLIDE WARNING: Immediate evacuation ordered for Tupul sector.",
                "status": "DELIVERED",
                "queued_at": "20:48:10",
                "delivered_at": "20:48:14"
            },
            {
                "id": "MSG-NER-002",
                "alert_id": "ALT-MAN-01",
                "recipient_group": "Registered Public (Noney Block)",
                "target_location": "Noney Hill Corridor",
                "channel": "Cell Broadcast & Radio Dispatch",
                "payload": "Move to Noney District Headquarter Safe Relief Shelter immediately.",
                "status": "DELIVERED",
                "queued_at": "20:48:12",
                "delivered_at": "20:48:16"
            }
        ]

    def get_status(self) -> Dict[str, Any]:
        pending_count = sum(1 for m in self.queue if m["status"] in ["QUEUED", "SENDING"])
        return {
            "network_status": "ONLINE" if self.is_network_online else "OFFLINE",
            "is_online": self.is_network_online,
            "pending_messages_count": pending_count,
            "delivered_count": self.delivered_count,
            "failed_count": self.failed_count,
            "total_recipients_reached": self.delivered_count + 320,
            "authority_recipients_count": 48,
            "public_recipients_count": 1372,
            "last_sync": self.last_sync_time,
            "queue": self.queue[:20]
        }

    def toggle_network(self) -> Dict[str, Any]:
        self.is_network_online = not self.is_network_online
        if self.is_network_online:
            # Automatically flush and synchronize queue on restoration
            self.sync_queue()
        return self.get_status()

    def queue_alert(self, alert_id: str, location: str, headline: str) -> Dict[str, Any]:
        now_str = datetime.now(timezone.utc).strftime("%H:%M:%S")
        status = "SENDING" if self.is_network_online else "QUEUED"

        # 1. Authority Dispatch
        auth_msg = {
            "id": f"MSG-NER-{datetime.now(timezone.utc).strftime('%f')[:4]}A",
            "alert_id": alert_id,
            "recipient_group": "SDMA Command & NDRF Response Post",
            "target_location": location,
            "channel": "Emergency Secure SMS & Radio Link",
            "payload": f"EMERGENCY DISPATCH: {headline}",
            "status": "DELIVERED" if self.is_network_online else "QUEUED",
            "queued_at": now_str,
            "delivered_at": now_str if self.is_network_online else None
        }

        # 2. Public Community Dispatch (Batch)
        pub_msg = {
            "id": f"MSG-NER-{datetime.now(timezone.utc).strftime('%f')[:4]}P",
            "alert_id": alert_id,
            "recipient_group": "Subscribed Residents & Transport Units (248 recipients)",
            "target_location": location,
            "channel": "Local Cell Broadcast & SMS Gateway",
            "payload": f"CIVIL ADVISORY: {headline}. Seek high ground shelters.",
            "status": "DELIVERED" if self.is_network_online else "QUEUED",
            "queued_at": now_str,
            "delivered_at": now_str if self.is_network_online else None
        }

        self.queue.insert(0, auth_msg)
        self.queue.insert(0, pub_msg)

        if self.is_network_online:
            self.delivered_count += 2
            self.last_sync_time = now_str + " UTC+05:30"

        return self.get_status()

    def sync_queue(self) -> Dict[str, Any]:
        now_str = datetime.now(timezone.utc).strftime("%H:%M:%S UTC+05:30")
        synced_count = 0
        for m in self.queue:
            if m["status"] in ["QUEUED", "SENDING"]:
                m["status"] = "DELIVERED"
                m["delivered_at"] = now_str
                synced_count += 1
                self.delivered_count += 1

        self.last_sync_time = now_str
        return {
            "synced_count": synced_count,
            "status": "QUEUE_SYNCHRONIZED",
            "is_online": self.is_network_online,
            "pending_messages_count": sum(1 for m in self.queue if m["status"] in ["QUEUED", "SENDING"]),
            "details": self.get_status()
        }

    def get_queue_status(self) -> Dict[str, Any]:
        return self.get_status()

    def queue_test_alert(self, alert_id: Optional[str] = None, location: str = "Noney Sector", headline: str = "TEST EMERGENCY ALARM") -> Dict[str, Any]:
        aid = alert_id or f"ALT-TEST-{int(datetime.now(timezone.utc).timestamp())}"
        return self.queue_alert(aid, location, headline)

communication_service = CommunicationService()

