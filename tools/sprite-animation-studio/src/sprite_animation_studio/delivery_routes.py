"""Server-owned Sprite Studio mode to Tool Hub route mapping."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .service import SpriteAnimationService


SPRITE_DELIVERY_ROUTES = {
    "pose_sequence": "sprite_action_runs",
    "sprite_action": "sprite_action_runs",
    "effect_stages": "effect_runs",
}

SPRITE_DELIVERY_TARGETS = {
    "sprite_action_runs": "Sprite Action Runs",
    "effect_runs": "Effect Runs",
}


def resolve_delivery_route(service: "SpriteAnimationService", run_id: str) -> str:
    """Resolve a delivery route only from the server-owned stored request mode."""
    from .service import RunBlockedError

    record = service.get_run(run_id)
    try:
        return SPRITE_DELIVERY_ROUTES[record.request.mode]
    except KeyError as error:
        raise RunBlockedError("DELIVERY_TOOL_ROUTE_UNAVAILABLE") from error


def install_service_delivery_route() -> None:
    """Install the reviewed method on the existing service without duplicating its large lifecycle owner."""
    from .service import SpriteAnimationService

    if not hasattr(SpriteAnimationService, "delivery_route_id"):
        setattr(SpriteAnimationService, "delivery_route_id", resolve_delivery_route)
