from __future__ import annotations

import logging
import os
import sys
from collections.abc import Mapping
from pathlib import Path

from .bridge_client import AuthenticatedBridge, DisconnectedBridge
from .bridge_descriptor import BridgeDescriptorError, load_bridge_descriptor
from .profile_store import ProfileError, load_profile
from .project_identity import ProjectIdentity, ProjectIdentityError
from .server import GatewayDependencies, build_server


_REQUIRED_ENVIRONMENT = (
    "BASE_GODOT_MCP_PROFILE_ID",
    "BASE_GODOT_MCP_CONFIG_DIR",
    "BASE_GODOT_PROJECT_ROOT",
)


def _required_environment(environment: Mapping[str, str], name: str) -> str:
    value = environment.get(name)
    if not isinstance(value, str) or not value:
        raise ValueError(f"MCP_ENVIRONMENT_REQUIRED:{name}")
    return value


def build_server_from_environment(environment: Mapping[str, str] | None = None):
    values = os.environ if environment is None else environment
    for name in _REQUIRED_ENVIRONMENT:
        _required_environment(values, name)
    profile = load_profile(
        _required_environment(values, "BASE_GODOT_MCP_PROFILE_ID"),
        config_dir=Path(_required_environment(values, "BASE_GODOT_MCP_CONFIG_DIR")),
    )
    project = ProjectIdentity.from_root(
        Path(_required_environment(values, "BASE_GODOT_PROJECT_ROOT"))
    )
    descriptor_path = values.get("BASE_GODOT_MCP_BRIDGE_DESCRIPTOR")
    if descriptor_path:
        descriptor = load_bridge_descriptor(
            Path(descriptor_path),
            profile=profile,
            project=project,
        )
        bridge = AuthenticatedBridge(
            profile=profile,
            project=project,
            descriptor=descriptor,
        )
    else:
        bridge = DisconnectedBridge()
    return build_server(
        GatewayDependencies(
            profile=profile,
            project=project,
            bridge=bridge,
        )
    )


def main() -> int:
    try:
        server = build_server_from_environment()
    except (OSError, ValueError, ProfileError, ProjectIdentityError, BridgeDescriptorError) as exc:
        logging.basicConfig(stream=sys.stderr, level=logging.ERROR)
        logging.error("%s", exc)
        return 2
    server.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
