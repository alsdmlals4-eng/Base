from __future__ import annotations

from typing import Any


class DisconnectedBridge:
    """Fail-closed Bridge used until a verified live descriptor is configured."""

    async def request(self, method: str, payload: dict[str, Any]) -> dict[str, Any]:
        if method == "editor.status":
            return {
                "success": True,
                "code": "BRIDGE_NOT_CONNECTED",
                "data": {
                    "connected": False,
                    "active_scene_path": None,
                    "dirty_state": "UNKNOWN",
                },
            }
        if method == "capabilities.list":
            return {
                "success": True,
                "code": "BRIDGE_NOT_CONNECTED",
                "data": {"capabilities": []},
            }
        data: dict[str, Any] = {}
        operation_id = payload.get("operation_id")
        if isinstance(operation_id, str):
            data["operation_id"] = operation_id
        return {
            "success": False,
            "code": "BRIDGE_NOT_CONNECTED",
            "data": data,
        }
