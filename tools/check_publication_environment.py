#!/usr/bin/env python3
"""Report schema v3 publication prerequisites without changing outputs."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import publication_v3 as pub
except ModuleNotFoundError as exc:
    print(json.dumps({
        "status": "FAILED",
        "missing_python_package": exc.name,
        "install": f'"{sys.executable}" -m pip install -r requirements-publication.txt',
    }, ensure_ascii=False, indent=2))
    raise SystemExit(1) from exc


def version(command: str | None, args: list[str]) -> str | None:
    if not command:
        return None
    result = subprocess.run(
        [command, *args], capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=30, check=False,
    )
    text = (result.stdout or result.stderr).strip().splitlines()
    return text[0] if text else f"exit={result.returncode}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=".", help="Directory whose write access must be checked.")
    parser.add_argument("--require-mermaid", action="store_true")
    args = parser.parse_args()
    root = Path.cwd()
    regular, bold = pub.font_paths()
    tools = {
        "python": sys.executable,
        "libreoffice": pub.libreoffice_path(),
        "pdftoppm": pub.pdftoppm_path(),
        "mermaid_cli": pub.mermaid_cli_path(root),
        "chrome": pub.chrome_path(),
        "node": shutil.which("node"),
        "pnpm": shutil.which("pnpm") or shutil.which("pnpm.cmd"),
        "font_regular": regular,
        "font_bold": bold,
    }
    output = Path(args.output).resolve()
    report = {
        "platform": platform.platform(),
        "tools": tools,
        "versions": {
            "python": platform.python_version(),
            "libreoffice": version(tools["libreoffice"], ["--version"]),
            "pdftoppm": version(tools["pdftoppm"], ["-v"]),
            "mermaid_cli": version(tools["mermaid_cli"], ["--version"]),
            "node": version(tools["node"], ["--version"]),
            "pnpm": version(tools["pnpm"], ["--version"]),
        },
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
    missing = [name for name in ("libreoffice", "pdftoppm", "font_regular") if not tools[name]]
    if args.require_mermaid:
        missing.extend(name for name in ("mermaid_cli", "chrome", "node", "pnpm") if not tools[name])
    report["missing"] = sorted(set(missing))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["missing"] or not report["output_writable"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
