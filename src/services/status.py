from __future__ import annotations


class StatusService:
    def get_status(self) -> dict[str, object]:
        return {
            "service": "haelite",
            "status": "operational",
            "incidents": [],
        }
