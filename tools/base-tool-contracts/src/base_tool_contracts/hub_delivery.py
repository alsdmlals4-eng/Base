"""Child-only loopback client for confirmed Studio-to-Tool-Hub delivery."""

from __future__ import annotations

import json
import os
import re
from typing import Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import ProxyHandler, Request, build_opener


class HubDeliveryError(RuntimeError):
    """Raised when the private Studio-to-Hub delivery handoff cannot be verified."""


class HubDeliverySender(Protocol):
    def __call__(
        self,
        run_id: str,
        image_bytes: bytes,
        media_type: str,
        tool_route_id: str | None = None,
    ) -> dict[str, object]:
        raise NotImplementedError

    def status(self, delivery_id: str) -> dict[str, object]:
        raise NotImplementedError


_RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$")
_DELIVERY_ID = re.compile(r"^[0-9a-f]{32}$")
_ROUTE_ID = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
_MAX_RESPONSE_BYTES = 64 * 1024


def _validated_origin(value: str) -> str:
    parsed = urlsplit(value)
    if (
        parsed.scheme != "http"
        or parsed.hostname != "127.0.0.1"
        or parsed.username is not None
        or parsed.password is not None
        or parsed.path not in {"", "/"}
        or parsed.query
        or parsed.fragment
        or parsed.port is None
        or not 0 < parsed.port < 65536
    ):
        raise HubDeliveryError("Tool Hub delivery origin is invalid")
    return f"http://127.0.0.1:{parsed.port}"


class LocalHubDeliveryClient:
    """Exchange confirmed raster bytes and delivery status with the owning loopback Tool Hub."""

    def __init__(self, origin: str, token: str) -> None:
        self._origin = _validated_origin(origin)
        if not isinstance(token, str) or len(token) < 32:
            raise HubDeliveryError("Tool Hub delivery credential is invalid")
        self._token = token
        self._opener = build_opener(ProxyHandler({}))

    def _json_request(
        self,
        path: str,
        *,
        method: str,
        data: bytes | None = None,
        content_type: str | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> dict[str, object]:
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Accept": "application/json",
        }
        if content_type is not None:
            headers["Content-Type"] = content_type
        if extra_headers:
            headers.update(extra_headers)
        request = Request(
            f"{self._origin}{path}",
            data=data,
            method=method,
            headers=headers,
        )
        try:
            with self._opener.open(request, timeout=5.0) as response:
                raw = response.read(_MAX_RESPONSE_BYTES + 1)
        except HTTPError as error:
            try:
                detail = json.loads(error.read(_MAX_RESPONSE_BYTES).decode("utf-8")).get("detail")
            except Exception:
                detail = None
            raise HubDeliveryError(str(detail or "Tool Hub rejected confirmed delivery")) from error
        except (OSError, URLError) as error:
            raise HubDeliveryError("Tool Hub confirmed delivery endpoint is unavailable") from error
        if len(raw) > _MAX_RESPONSE_BYTES:
            raise HubDeliveryError("Tool Hub delivery response is oversized")
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as error:
            raise HubDeliveryError("Tool Hub delivery response is invalid") from error
        if not isinstance(payload, dict):
            raise HubDeliveryError("Tool Hub delivery response is invalid")
        return payload

    def __call__(
        self,
        run_id: str,
        image_bytes: bytes,
        media_type: str,
        tool_route_id: str | None = None,
    ) -> dict[str, object]:
        if _RUN_ID.fullmatch(run_id) is None:
            raise HubDeliveryError("delivery run identity is invalid")
        if media_type != "image/png" or not isinstance(image_bytes, bytes) or not image_bytes:
            raise HubDeliveryError("delivery content is invalid")
        extra_headers: dict[str, str] = {}
        if tool_route_id is not None:
            if _ROUTE_ID.fullmatch(tool_route_id) is None:
                raise HubDeliveryError("delivery tool route identity is invalid")
            extra_headers["X-Base-Tool-Route"] = tool_route_id
        payload = self._json_request(
            f"/internal/studio-delivery/{quote(run_id, safe='')}",
            method="POST",
            data=image_bytes,
            content_type="image/png",
            extra_headers=extra_headers,
        )
        required = {
            "status",
            "delivery_id",
            "tool_id",
            "project_id",
            "run_id",
            "content_sha256",
            "tool_route_id",
            "target_node_name",
            "bridge_state",
            "delivery_state",
            "figma_url",
        }
        if not required.issubset(payload) or payload.get("run_id") != run_id:
            raise HubDeliveryError("Tool Hub delivery response identity is invalid")
        if tool_route_id is not None and payload.get("tool_route_id") != tool_route_id:
            raise HubDeliveryError("Tool Hub delivery response route identity is invalid")
        return payload

    def status(self, delivery_id: str) -> dict[str, object]:
        if _DELIVERY_ID.fullmatch(delivery_id) is None:
            raise HubDeliveryError("delivery identity is invalid")
        payload = self._json_request(
            f"/internal/studio-delivery/{delivery_id}/status",
            method="GET",
        )
        required = {
            "status",
            "delivery_id",
            "tool_id",
            "project_id",
            "run_id",
            "content_sha256",
            "tool_route_id",
            "target_node_name",
            "bridge_state",
            "delivery_state",
            "figma_url",
        }
        if not required.issubset(payload) or payload.get("delivery_id") != delivery_id:
            raise HubDeliveryError("Tool Hub delivery status identity is invalid")
        return payload


def sender_from_environment() -> HubDeliverySender | None:
    """Resolve the private Hub sender only when the complete child-only identity exists."""
    origin = os.environ.get("BASE_TOOL_HUB_DELIVERY_ORIGIN")
    token = os.environ.get("BASE_TOOL_HUB_DELIVERY_TOKEN")
    if origin is None and token is None:
        return None
    if origin is None or token is None:
        raise HubDeliveryError("Tool Hub delivery identity is incomplete")
    return LocalHubDeliveryClient(origin, token)
