from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.loop_shadow_kernel import RunState, ShadowKernel


def _json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"request must be a JSON object: {path}")
    return value


def _print(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))


def _add_roots(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--state-root", type=Path, required=True)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Deterministic Universal Loop SHADOW control plane")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate one SHADOW request without writing state")
    validate.add_argument("request", type=Path)
    _add_roots(validate)

    shadow = subparsers.add_parser("shadow", help="execute one deterministic read-only SHADOW run")
    shadow.add_argument("request", type=Path)
    _add_roots(shadow)
    shadow.add_argument("--now", default=None)

    status = subparsers.add_parser("status", help="read and verify one immutable receipt")
    status.add_argument("--project-id", required=True)
    status.add_argument("--run-id", required=True)
    _add_roots(status)

    leases = subparsers.add_parser("leases", help="read current semantic resource leases")
    leases.add_argument("--project-id", required=True)
    _add_roots(leases)
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        arguments = _parser().parse_args(argv)
        kernel = ShadowKernel(
            arguments.project_root,
            arguments.state_root,
            now=getattr(arguments, "now", None),
        )

        if arguments.command == "validate":
            outcome = kernel.validate(_json_object(arguments.request))
            payload = outcome.to_dict()
            payload["status"] = "PASS" if not outcome.findings else "BLOCKED"
            _print(payload)
            return 0 if not outcome.findings else 2

        if arguments.command == "shadow":
            outcome = kernel.shadow(_json_object(arguments.request))
            _print(outcome.to_dict())
            return 0 if outcome.state is RunState.SHADOW_COMPLETE else 2

        if arguments.command == "status":
            _print(kernel.status(arguments.project_id, arguments.run_id))
            return 0

        if arguments.command == "leases":
            _print(kernel.leases(arguments.project_id))
            return 0

        raise ValueError(f"unsupported command: {arguments.command}")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        _print(
            {
                "status": "ERROR",
                "code": type(error).__name__.upper(),
                "message": str(error),
            }
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
