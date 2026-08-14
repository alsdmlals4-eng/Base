#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.loop_a2_runtime.contract_bridge import ContractBridgeError, build_request_from_capsule
from tools.loop_a2_runtime.protocol import Budgets, ProtocolError, RunRequest
from tools.loop_a2_runtime.provider_gate import real_provider_gate
from tools.loop_a2_runtime.providers import FakeBuilder, FakeCritic
from tools.loop_a2_runtime.runner import A2Runtime


def _fake_output_path(request: RunRequest) -> str:
    pattern = request.allowed_paths[0]
    if pattern.endswith("/**"):
        return pattern[:-3].rstrip("/") + "/fake-provider-output.txt"
    if any(marker in pattern for marker in ("*", "?", "[")):
        return pattern.replace("**", "fake").replace("*", "fake").replace("?", "x")
    return pattern


def _fake_runtime(request: RunRequest) -> A2Runtime:
    return A2Runtime(
        builder=FakeBuilder(changed_paths=(_fake_output_path(request),)),
        critic=FakeCritic(verdict="PASS", checked_requirement_ids=request.requirement_ids),
    )


def _load_request_fixture(path: Path) -> RunRequest:
    return RunRequest.from_dict(json.loads(path.read_text(encoding="utf-8")))


def main() -> int:
    parser = argparse.ArgumentParser(description="Bounded Loop Engineering A2 foundation.")
    commands = parser.add_subparsers(dest="command", required=True)

    fixture = commands.add_parser("burn-in-fixture", help="Run deterministic fake-provider protocol tests only.")
    fixture.add_argument("request", type=Path)
    fixture.add_argument("--observed-main-sha", required=True)
    fixture.add_argument("--runs", type=int, default=3)

    run = commands.add_parser("run", help="Derive authority from an adopted M2 Capsule.")
    run.add_argument("--project-root", type=Path, required=True)
    run.add_argument("--capsule", required=True)
    run.add_argument("--run-id", required=True)
    run.add_argument("--observed-main-sha", required=True)
    run.add_argument("--provider", choices=("fake", "real"), default="fake")
    run.add_argument("--max-turns", type=int, default=12)
    run.add_argument("--max-repair-cycles", type=int, default=2)
    run.add_argument("--timeout-seconds", type=int, default=600)

    args = parser.parse_args()

    try:
        if args.command == "burn-in-fixture":
            request = _load_request_fixture(args.request)
            if request.provider_mode != "FAKE":
                raise ProtocolError("burn-in fixtures must use provider_mode FAKE")
            result = _fake_runtime(request).burn_in(
                request, observed_main_sha=args.observed_main_sha, runs=args.runs
            )
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0 if result["status"] == "FAKE_PROVIDER_BURNIN_GREEN" else 1

        request = build_request_from_capsule(
            project_root=args.project_root,
            capsule_relative=args.capsule,
            run_id=args.run_id,
            provider_mode=args.provider.upper(),
            budgets=Budgets(args.max_turns, args.max_repair_cycles, args.timeout_seconds),
        )
    except (OSError, json.JSONDecodeError, ProtocolError, ContractBridgeError, ValueError) as exc:
        print(json.dumps({"status": "CONTRACT_INVALID", "message": str(exc)}, sort_keys=True))
        return 2

    if args.provider == "real":
        gate = real_provider_gate()
        if gate["status"] != "READY":
            print(json.dumps(gate, sort_keys=True))
            return 2
        result = {
            "status": "BLOCKED_UNVERIFIED",
            "code": "REAL_PROVIDER_WORKER_NOT_IMPLEMENTED",
            "message": "The paid transport gate passed, but the Codex/GPT workers are not part of this foundation.",
        }
        print(json.dumps(result, sort_keys=True))
        return 2

    outcome = _fake_runtime(request).run(request, observed_main_sha=args.observed_main_sha)
    print(json.dumps(outcome.evidence, ensure_ascii=False, sort_keys=True))
    return 0 if outcome.state == "WAITING_INTEGRATION" else 1


if __name__ == "__main__":
    raise SystemExit(main())
