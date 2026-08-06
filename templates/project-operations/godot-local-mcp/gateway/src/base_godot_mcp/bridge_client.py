from __future__ import annotations

import asyncio
import hashlib
import hmac
import secrets
from dataclasses import dataclass
from typing import Any

from .bridge_descriptor import BridgeDescriptor
from .framing import FrameError, canonical_json_bytes, read_frame, write_frame
from .profile_store import ClientProfile
from .project_identity import ProjectIdentity


class BridgeClientError(ValueError):
    """Authenticated Bridge client failure with a stable code."""


def _mac(secret: str, payload: dict[str, Any]) -> str:
    return hmac.new(
        secret.encode("utf-8"),
        canonical_json_bytes(payload),
        hashlib.sha256,
    ).hexdigest()


def _signed(secret: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {**payload, "mac": _mac(secret, payload)}


def _verify_signed(
    secret: str,
    frame: dict[str, Any],
    *,
    code: str,
) -> dict[str, Any]:
    received = frame.get("mac")
    if not isinstance(received, str) or len(received) != 64:
        raise BridgeClientError(code)
    unsigned = dict(frame)
    unsigned.pop("mac", None)
    expected = _mac(secret, unsigned)
    if not hmac.compare_digest(received, expected):
        raise BridgeClientError(code)
    return unsigned


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


@dataclass(frozen=True, slots=True)
class AuthenticatedBridge:
    profile: ClientProfile
    project: ProjectIdentity
    descriptor: BridgeDescriptor
    timeout_seconds: float = 2.0

    def __post_init__(self) -> None:
        if not self.profile.credential_secret:
            raise BridgeClientError("BRIDGE_CREDENTIAL_REQUIRED")
        if self.descriptor.profile_id != self.profile.profile_id:
            raise BridgeClientError("BRIDGE_PROFILE_MISMATCH")
        if self.descriptor.project_fingerprint != self.project.fingerprint:
            raise BridgeClientError("BRIDGE_PROJECT_MISMATCH")
        if not 0.1 <= self.timeout_seconds <= 30:
            raise BridgeClientError("BRIDGE_TIMEOUT_INVALID")

    async def request(self, method: str, payload: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(method, str) or not method or len(method) > 128:
            raise BridgeClientError("BRIDGE_METHOD_INVALID")
        if not isinstance(payload, dict):
            raise BridgeClientError("BRIDGE_PAYLOAD_INVALID")
        try:
            async with asyncio.timeout(self.timeout_seconds):
                return await self._request(method, payload)
        except BridgeClientError:
            raise
        except (OSError, asyncio.TimeoutError, FrameError) as exc:
            raise BridgeClientError("BRIDGE_CONNECTION_FAILED") from exc

    async def _request(self, method: str, payload: dict[str, Any]) -> dict[str, Any]:
        reader, writer = await asyncio.open_connection(
            self.descriptor.host,
            self.descriptor.port,
        )
        try:
            client_nonce = secrets.token_hex(32)
            hello = {
                "type": "HELLO",
                "protocol": self.descriptor.protocol,
                "profile_id": self.profile.profile_id,
                "project_fingerprint": self.project.fingerprint,
                "bridge_instance_id": self.descriptor.bridge_instance_id,
                "descriptor_nonce": self.descriptor.descriptor_nonce,
                "client_nonce": client_nonce,
            }
            await write_frame(
                writer,
                _signed(self.profile.credential_secret, hello),
            )
            ack = _verify_signed(
                self.profile.credential_secret,
                await read_frame(reader),
                code="BRIDGE_HANDSHAKE_AUTH_FAILED",
            )
            if (
                ack.get("type") != "HELLO_ACK"
                or ack.get("protocol") != self.descriptor.protocol
                or ack.get("bridge_instance_id") != self.descriptor.bridge_instance_id
                or ack.get("client_nonce") != client_nonce
            ):
                raise BridgeClientError("BRIDGE_HANDSHAKE_IDENTITY_FAILED")
            session_id = ack.get("session_id")
            server_nonce = ack.get("server_nonce")
            if not isinstance(session_id, str) or not session_id or len(session_id) > 128:
                raise BridgeClientError("BRIDGE_HANDSHAKE_INVALID")
            if not isinstance(server_nonce, str) or len(server_nonce) < 32 or len(server_nonce) > 256:
                raise BridgeClientError("BRIDGE_HANDSHAKE_INVALID")

            request_id = secrets.token_hex(16)
            request = {
                "type": "REQUEST",
                "protocol": self.descriptor.protocol,
                "session_id": session_id,
                "request_id": request_id,
                "server_nonce": server_nonce,
                "method": method,
                "payload": payload,
            }
            await write_frame(
                writer,
                _signed(self.profile.credential_secret, request),
            )
            response = _verify_signed(
                self.profile.credential_secret,
                await read_frame(reader),
                code="BRIDGE_RESPONSE_AUTH_FAILED",
            )
            if (
                response.get("type") != "RESPONSE"
                or response.get("protocol") != self.descriptor.protocol
                or response.get("session_id") != session_id
                or response.get("request_id") != request_id
            ):
                raise BridgeClientError("BRIDGE_RESPONSE_IDENTITY_FAILED")
            result = response.get("result")
            if not isinstance(result, dict):
                raise BridgeClientError("BRIDGE_RESPONSE_INVALID")
            return result
        finally:
            writer.close()
            try:
                await writer.wait_closed()
            except (OSError, ConnectionError):
                pass
