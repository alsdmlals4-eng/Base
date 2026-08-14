from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.loop_capsule_shadow_adapter import AdapterError, build_shadow_request


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Translate a valid M2 Capsule bundle into one M3 SHADOW request")
    parser.add_argument("capsule", type=Path)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--observed-main-sha", required=True)
    parser.add_argument("--planning-drift", required=True)
    parser.add_argument("--visual-drift", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        request = build_shadow_request(
            args.capsule,
            run_id=args.run_id,
            observed_main_sha=args.observed_main_sha,
            planning_drift=args.planning_drift,
            visual_drift=args.visual_drift,
        )
    except (AdapterError, OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "BLOCKED", "message": str(error)}, ensure_ascii=False, sort_keys=True, indent=2))
        return 2
    print(json.dumps(request, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
