"""Shared contracts consumed by Base interactive tools."""

from .figma_routing import (
    DeliveryBlockedError,
    ProjectFigmaRegistry,
    ProjectFigmaTarget,
)
from .staging import StableStagingTree, StagingViolation, assert_verified_staging_path, create_verified_run_directories, safe_staging_write_bytes, safe_staging_write_text, stable_staging_path, stable_staging_tree, staging_identity, staging_read_bytes
from .approved_anchor import AnchorEvidenceError, ApprovedAnchorRegistry

__all__ = ["AnchorEvidenceError", "ApprovedAnchorRegistry", "DeliveryBlockedError", "ProjectFigmaRegistry", "ProjectFigmaTarget", "StableStagingTree", "StagingViolation", "assert_verified_staging_path", "create_verified_run_directories", "safe_staging_write_bytes", "safe_staging_write_text", "stable_staging_path", "stable_staging_tree", "staging_identity", "staging_read_bytes"]
