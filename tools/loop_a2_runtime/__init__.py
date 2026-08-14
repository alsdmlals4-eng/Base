"""Bounded A2 runtime primitives for approved Loop Engineering packages."""

from .authority_snapshot import (
    AuthorityFile,
    AuthoritySnapshot,
    AuthoritySnapshotError,
    capture_authority_snapshot,
)
from .protocol import ProtocolError, ReviewResult, RunRequest, WorkerResult
from .runner import A2Runtime, RunOutcome

__all__ = [
    "A2Runtime",
    "AuthorityFile",
    "AuthoritySnapshot",
    "AuthoritySnapshotError",
    "ProtocolError",
    "ReviewResult",
    "RunOutcome",
    "RunRequest",
    "WorkerResult",
    "capture_authority_snapshot",
]
