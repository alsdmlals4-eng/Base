#!/usr/bin/env python3
"""Report schema v3 publication prerequisites without changing outputs."""

from __future__ import annotations

import argparse
import json
import os
import platform
import sys
from pathlib import Path

try:
    import publication_readiness as readiness
except ModuleNotFoundError as exc:
    print(json.dumps({
        "status": "FAILED",
        "missing_python_package": exc.name,
        "install": f'"{sys.executable}" -m pip install -r requirements-publication.txt',
    }, ensure_ascii=False, indent=2))
    raise SystemExit(1) from exc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=".", help="Directory whose write access must be checked.")
    parser.add_argument("--require-mermaid", action="store_true")
    args = parser.parse_args()
    root = Path.cwd()
    output = Path(args.output).resolve()
    runtime = readiness.publication_readiness(
        root,
        require_mermaid=args.require_mermaid,
    )
    runtime_report = runtime.as_dict()
    runtime_report["tools"] = {
        "python": sys.executable,
        **runtime_report["tools"],
    }
    runtime_report["versions"] = {
        "python": platform.python_version(),
        **runtime_report["versions"],
    }
    report = {
        "platform": platform.platform(),
        **runtime_report,
        "output_path": str(output),
        "output_parent_exists": output.parent.exists(),
        "output_writable": os.access(output if output.exists() else output.parent, os.W_OK),
        "recovery": {
            "python": f'"{sys.executable}" -m pip install -r requirements-publication.txt',
            "node": "pnpm install --frozen-lockfile",
            "overrides": [
                "BASE_LIBREOFFICE", "BASE_PDFTOPPM", "BASE_MERMAID_CLI",
                "BASE_FONT_REGULAR", "BASE_FONT_BOLD", "PUPPETEER_EXECUTABLE_PATH",
            ],
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if not runtime.ready or not report["output_writable"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
