from __future__ import annotations

import argparse
from dataclasses import asdict, is_dataclass
import json
from pathlib import Path

from .ntn import BridgeError, NtnClient


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="notion-native-file-bridge")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("preflight")

    upload = sub.add_parser("upload")
    upload.add_argument("--file", type=Path, required=True)

    append_image = sub.add_parser("append-image")
    append_image.add_argument("--page-id", required=True)
    append_image.add_argument("--upload-id", required=True)

    set_cover = sub.add_parser("set-cover")
    set_cover.add_argument("--page-id", required=True)
    set_cover.add_argument("--upload-id", required=True)

    set_files = sub.add_parser("set-files-property")
    set_files.add_argument("--page-id", required=True)
    set_files.add_argument("--property", required=True)
    set_files.add_argument("--upload-id", required=True)
    set_files.add_argument("--filename", required=True)

    return parser


def _json_ready(value: object) -> dict[str, object]:
    if is_dataclass(value):
        payload = asdict(value)
        if isinstance(payload, dict):
            return payload
    if isinstance(value, dict):
        return value
    raise TypeError(f"unsupported receipt type: {type(value).__name__}")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        client = NtnClient()
        if args.command == "preflight":
            receipt = client.preflight()
        elif args.command == "upload":
            receipt = client.upload(args.file)
        elif args.command == "append-image":
            receipt = client.append_image(args.page_id, args.upload_id)
        elif args.command == "set-cover":
            receipt = client.set_cover(args.page_id, args.upload_id)
        else:
            receipt = client.set_files_property(
                args.page_id,
                args.property,
                args.upload_id,
                args.filename,
            )
        print(json.dumps(_json_ready(receipt), ensure_ascii=False, sort_keys=True))
        return 0
    except BridgeError as exc:
        print(
            json.dumps(
                {
                    "status": "BLOCKED",
                    "code": exc.code,
                    "detail": exc.detail,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
