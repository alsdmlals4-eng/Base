from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import time

from .control_plane import GhControlPlane
from .repositories import ManagedRepositoryStore
from .runtime import LocalA2Runtime
from .service import LocalExecutorService


CONTROL_REPOSITORY = "alsdmlals4-eng/Base"
TRUSTED_AUTHOR = "alsdmlals4-eng"
QUEUE_LABEL = "loop-a2-local-job"


def _poll_seconds(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("poll interval must be an integer") from exc
    if parsed < 15 or parsed > 3600:
        raise argparse.ArgumentTypeError("poll interval must be 15..3600 seconds")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="loop-a2-local-executor")
    parser.add_argument("--state-root", type=Path)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("preflight")
    sub.add_parser("once")
    daemon = sub.add_parser("daemon")
    daemon.add_argument("--poll-seconds", type=_poll_seconds, default=60)
    return parser


def _default_state_root() -> Path:
    local = os.environ.get("LOCALAPPDATA")
    if local:
        return Path(local) / "BaseLoopA2LocalExecutor"
    return Path.home() / ".base-loop-a2-local-executor"


def _require_executable(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"{name.upper()}_UNAVAILABLE")
    return path


def build_service(state_root: Path) -> LocalExecutorService:
    gh = _require_executable("gh")
    git = _require_executable("git")
    docker = _require_executable("docker")
    store = ManagedRepositoryStore(
        state_root=state_root,
        repository_sources={},
        git_executable=git,
        allow_github_sources=True,
    )
    plane = GhControlPlane(
        control_repository=CONTROL_REPOSITORY,
        required_label=QUEUE_LABEL,
        gh_executable=gh,
    )
    runtime = LocalA2Runtime(
        store=store,
        python_executable=sys.executable,
        docker_executable=docker,
        base_repository=CONTROL_REPOSITORY,
    )
    return LocalExecutorService(
        control_plane=plane,
        runtime=runtime,
        trusted_author=TRUSTED_AUTHOR,
        required_label=QUEUE_LABEL,
    )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    state_root = (args.state_root or _default_state_root()).resolve(strict=False)
    state_root.mkdir(parents=True, exist_ok=True)
    try:
        service = build_service(state_root)
        if args.command == "preflight":
            print(json.dumps(service.preflight(), sort_keys=True))
            return 0
        if args.command == "once":
            result = service.once()
            print(json.dumps(result, sort_keys=True))
            return 0 if result.get("status") in {"PASS", "IDLE"} else 2
        while True:
            service.once()
            time.sleep(args.poll_seconds)
    except KeyboardInterrupt:
        return 0
    except Exception as exc:
        code = getattr(exc, "code", type(exc).__name__)
        print(json.dumps({"status": "BLOCKED", "code": str(code)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
