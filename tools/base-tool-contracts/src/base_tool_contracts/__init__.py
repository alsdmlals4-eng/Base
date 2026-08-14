"""Shared contracts consumed by Base interactive tools."""

from .approved_anchor import AnchorEvidenceError, ApprovedAnchorRegistry
from .figma_routing import (
    DeliveryBlockedError,
    ProjectFigmaRegistry,
    ProjectFigmaTarget,
    ProjectRepositoryPointer,
)
from .figma_tool_routing import ProjectFigmaToolRoute, ProjectFigmaToolRouteRegistry
from .hub_startup import (
    HubLaunchIdentity,
    HubStartupError,
    hub_identity_from_environment,
    open_loopback_listener,
    write_startup_report,
)
from .project_identity import ProjectIdentityError, ProjectIdentityEvidence, validate_project_identity
from .request_limits import BoundedRequestBodyMiddleware
from .staging import (
    StableStagingTree,
    StagingViolation,
    assert_verified_staging_path,
    confined_staging_read_bytes,
    create_verified_run_directories,
    safe_staging_write_bytes,
    safe_staging_write_text,
    stable_staging_path,
    stable_staging_tree,
    staging_identity,
    staging_read_bytes,
)
from .subscription_handoff import (
    SubscriptionHandoffError,
    SubscriptionHandoffPacket,
    build_subscription_handoff_packet,
)
from .windows_project_identity import validate_windows_project_identity

__all__ = [
    "AnchorEvidenceError",
    "ApprovedAnchorRegistry",
    "BoundedRequestBodyMiddleware",
    "DeliveryBlockedError",
    "HubLaunchIdentity",
    "HubStartupError",
    "ProjectFigmaRegistry",
    "ProjectFigmaTarget",
    "ProjectFigmaToolRoute",
    "ProjectFigmaToolRouteRegistry",
    "ProjectRepositoryPointer",
    "ProjectIdentityError",
    "ProjectIdentityEvidence",
    "StableStagingTree",
    "StagingViolation",
    "SubscriptionHandoffError",
    "SubscriptionHandoffPacket",
    "assert_verified_staging_path",
    "build_subscription_handoff_packet",
    "confined_staging_read_bytes",
    "create_verified_run_directories",
    "hub_identity_from_environment",
    "open_loopback_listener",
    "safe_staging_write_bytes",
    "safe_staging_write_text",
    "stable_staging_path",
    "stable_staging_tree",
    "staging_identity",
    "staging_read_bytes",
    "validate_project_identity",
    "validate_windows_project_identity",
    "write_startup_report",
]
