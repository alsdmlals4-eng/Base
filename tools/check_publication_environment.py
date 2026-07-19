#!/usr/bin/env python3
"""Report schema v3 publication prerequisites without changing outputs."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import signal
import subprocess
import sys
import tempfile
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


def _terminate_process_tree(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(process.pid), "/T", "/F"],
            capture_output=True,
            check=False,
        )
    else:
        os.killpg(process.pid, signal.SIGKILL)
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()


def version(command: str | None, args: list[str]) -> tuple[str | None, str | None]:
    if not command:
        return None, "not found"
    with tempfile.TemporaryDirectory(prefix="base-tool-probe-") as temporary:
        process = subprocess.Popen(
            [command, *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            start_new_session=os.name != "nt",
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0,
        )
        try:
            stdout, stderr = process.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            _terminate_process_tree(process)
            return None, "timed out after 30 seconds"
    output = (stdout or stderr).strip().splitlines()
    first_line = output[0] if output else f"exit={process.returncode}"
    if process.returncode:
        return None, first_line
    return first_line, None


def libreoffice_smoke(command: str | None) -> tuple[str | None, str | None]:
    if not command:
        return None, "not found"
    with tempfile.TemporaryDirectory(prefix="base-libreoffice-probe-") as temporary:
        root = Path(temporary)
        profile = root / "profile"
        profile.mkdir()
        source = root / "probe.html"
        output = root / "probe.pdf"
        source.write_text("<!doctype html><meta charset='utf-8'><title>Base probe</title><p>Base</p>", encoding="utf-8")
        process = subprocess.Popen(
            [
                command,
                f"-env:UserInstallation={profile.resolve().as_uri()}",
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                str(root),
                str(source),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            start_new_session=os.name != "nt",
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0,
        )
        try:
            stdout, stderr = process.communicate(timeout=60)
        except subprocess.TimeoutExpired:
            _terminate_process_tree(process)
            return None, "conversion smoke timed out after 60 seconds"
        if process.returncode:
            detail = (stdout or stderr).strip().splitlines()
            return None, detail[0] if detail else f"exit={process.returncode}"
        if not output.is_file() or output.read_bytes()[:5] != b"%PDF-":
            return None, "conversion smoke did not produce a valid PDF"
    return "conversion-smoke-passed", None


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
    version_results = {
        "libreoffice": libreoffice_smoke(tools["libreoffice"]),
        "pdftoppm": version(tools["pdftoppm"], ["-v"]),
        "mermaid_cli": version(tools["mermaid_cli"], ["--version"]),
        "node": version(tools["node"], ["--version"]),
        "pnpm": version(tools["pnpm"], ["--version"]),
    }
    report = {
        "platform": platform.platform(),
        "tools": tools,
        "versions": {
            "python": platform.python_version(),
            **{name: result[0] for name, result in version_results.items()},
        },
        "probe_failures": {name: result[1] for name, result in version_results.items() if result[1]},
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
    missing.extend(name for name in ("libreoffice", "pdftoppm") if version_results[name][1])
    if args.require_mermaid:
        missing.extend(name for name in ("mermaid_cli", "chrome", "node", "pnpm") if not tools[name])
    report["missing"] = sorted(set(missing))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["missing"] or not report["output_writable"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
