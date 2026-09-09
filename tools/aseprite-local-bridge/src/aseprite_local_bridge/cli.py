from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable, Sequence

from .bridge import AsepriteBridge, BridgeConfig, BridgeError


BridgeFactory = Callable[..., AsepriteBridge]


def _create_bridge(
    *,
    project_root: str,
    config_path: str | None,
    executable: str | None,
) -> AsepriteBridge:
    config = BridgeConfig.load(Path(project_root), Path(config_path) if config_path else None)
    return AsepriteBridge(config, executable=Path(executable) if executable else None)


def _add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--config")
    parser.add_argument("--aseprite")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aseprite-local-bridge")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="validate config and Aseprite availability")
    _add_common_arguments(doctor)

    inspect = subparsers.add_parser("inspect", help="read layers, tags, and slices")
    _add_common_arguments(inspect)
    inspect.add_argument("--source", required=True)

    export = subparsers.add_parser(
        "export-candidate",
        help="export PNG + JSON into the configured local candidate root",
    )
    _add_common_arguments(export)
    export.add_argument("--source", required=True)
    export.add_argument("--asset-id", required=True)
    export.add_argument("--replace-candidate", action="store_true")

    validate = subparsers.add_parser(
        "validate-candidate",
        help="verify candidate files and receipt hashes",
    )
    _add_common_arguments(validate)
    validate.add_argument("--asset-id", required=True)
    return parser


def main(
    argv: Sequence[str] | None = None,
    *,
    bridge_factory: BridgeFactory | None = None,
) -> int:
    args = _parser().parse_args(argv)
    factory = bridge_factory or _create_bridge
    try:
        bridge = factory(
            project_root=args.project_root,
            config_path=args.config,
            executable=args.aseprite,
        )
        if args.command == "doctor":
            result = bridge.doctor()
        elif args.command == "inspect":
            result = bridge.inspect(args.source)
        elif args.command == "export-candidate":
            result = bridge.export_candidate(
                args.source,
                args.asset_id,
                replace_candidate=args.replace_candidate,
            )
        elif args.command == "validate-candidate":
            result = bridge.validate_candidate(args.asset_id)
        else:  # pragma: no cover - argparse enforces the command set
            raise AssertionError(args.command)
    except BridgeError as error:
        result = error.as_dict()
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 2

    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
