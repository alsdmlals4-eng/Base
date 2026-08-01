from __future__ import annotations

import os
import shutil
import signal
import subprocess
import tempfile
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path

try:
    import publication_v3 as pub
except ModuleNotFoundError:
    from tools import publication_v3 as pub


@dataclass(frozen=True)
class PublicationTools:
    libreoffice: str | None
    pdftoppm: str | None
    mermaid_cli: str | None
    chrome: str | None
    node: str | None
    pnpm: str | None
    font_regular: str | None
    font_bold: str | None


@dataclass(frozen=True)
class ReadinessReport:
    tools: PublicationTools
    versions: dict[str, str | None]
    probe_failures: dict[str, str]
    missing: tuple[str, ...]

    @property
    def ready(self) -> bool:
        return not self.missing and not self.probe_failures

    @property
    def skip_reason(self) -> str:
        unavailable = sorted(set(self.missing) | set(self.probe_failures))
        if not unavailable:
            return "publication runtime ready"
        return "publication runtime unavailable: " + ", ".join(unavailable)

    def as_dict(self) -> dict[str, object]:
        return {
            "tools": asdict(self.tools),
            "versions": self.versions,
            "probe_failures": self.probe_failures,
            "missing": list(self.missing),
            "ready": self.ready,
            "skip_reason": self.skip_reason,
        }


def _configured_path(environment_name: str) -> str | None:
    configured = os.environ.get(environment_name, "").strip()
    return str(Path(configured).expanduser().resolve()) if configured else None


def resolve_publication_tools(repository_root: Path) -> PublicationTools:
    regular, bold = pub.font_paths()
    return PublicationTools(
        libreoffice=_configured_path("BASE_LIBREOFFICE") or pub.libreoffice_path(),
        pdftoppm=_configured_path("BASE_PDFTOPPM") or pub.pdftoppm_path(),
        mermaid_cli=(
            _configured_path("BASE_MERMAID_CLI")
            or pub.mermaid_cli_path(repository_root)
        ),
        chrome=(
            _configured_path("PUPPETEER_EXECUTABLE_PATH") or pub.chrome_path()
        ),
        node=shutil.which("node"),
        pnpm=shutil.which("pnpm") or shutil.which("pnpm.cmd"),
        font_regular=_configured_path("BASE_FONT_REGULAR") or regular,
        font_bold=_configured_path("BASE_FONT_BOLD") or bold,
    )


def _terminate_process_tree(process: subprocess.Popen[str]) -> None:
    if os.name == "nt":
        try:
            subprocess.run(
                ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                capture_output=True,
                check=False,
                timeout=5,
            )
        except subprocess.TimeoutExpired:
            pass
    else:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    if process.poll() is None:
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


def _close_probe_pipes(process: subprocess.Popen[str]) -> None:
    for stream in (process.stdout, process.stderr):
        if stream is not None:
            stream.close()


def _run_probe(
    command: list[str],
    *,
    timeout: int,
) -> tuple[subprocess.Popen[str], str, str] | tuple[None, None, str]:
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            start_new_session=os.name != "nt",
            creationflags=(
                subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
            ),
        )
    except OSError as error:
        return None, None, str(error)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        _terminate_process_tree(process)
        try:
            process.communicate(timeout=min(1.0, max(0.1, float(timeout))))
        except subprocess.TimeoutExpired:
            _close_probe_pipes(process)
        return None, None, f"timed out after {timeout} seconds"
    return process, stdout, stderr


def _probe_command(command: str, arguments: list[str]) -> list[str]:
    return pub.safe_executable_command(
        command,
        arguments,
        trusted_wrapper_roots=(Path(command).resolve().parent,),
    )


def _command_version(
    command: str,
    arguments: list[str],
    *,
    timeout: int = 30,
) -> tuple[str | None, str | None]:
    try:
        probe_command = _probe_command(command, arguments)
    except ValueError as error:
        return None, str(error)
    process, stdout, stderr = _run_probe(
        probe_command,
        timeout=timeout,
    )
    if process is None:
        return None, stderr
    output = (stdout or stderr).strip().splitlines()
    first_line = output[0] if output else f"exit={process.returncode}"
    if process.returncode:
        return None, first_line
    return first_line, None


def _libreoffice_smoke(command: str) -> tuple[str | None, str | None]:
    with tempfile.TemporaryDirectory(prefix="base-libreoffice-probe-") as temporary:
        root = Path(temporary)
        profile = root / "profile"
        profile.mkdir()
        source = root / "probe.html"
        output = root / "probe.pdf"
        source.write_text(
            "<!doctype html><meta charset='utf-8'><title>Base probe</title><p>Base</p>",
            encoding="utf-8",
        )
        arguments = [
            f"-env:UserInstallation={profile.resolve().as_uri()}",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(root),
            str(source),
        ]
        try:
            probe_command = _probe_command(command, arguments)
        except ValueError as error:
            return None, str(error)
        process, stdout, stderr = _run_probe(
            probe_command,
            timeout=60,
        )
        if process is None:
            return None, stderr
        if process.returncode:
            detail = (stdout or stderr).strip().splitlines()
            return None, detail[0] if detail else f"exit={process.returncode}"
        if not output.is_file() or output.read_bytes()[:5] != b"%PDF-":
            return None, "conversion smoke did not produce a valid PDF"
    return "conversion-smoke-passed", None


def _missing_paths(tools: PublicationTools, required: tuple[str, ...]) -> list[str]:
    missing: list[str] = []
    for name in required:
        value = getattr(tools, name)
        if not value or not Path(value).is_file():
            missing.append(name)
    return missing


def probe_publication_readiness(
    tools: PublicationTools,
    *,
    require_mermaid: bool = False,
) -> ReadinessReport:
    basic = ("libreoffice", "pdftoppm", "font_regular", "font_bold")
    mermaid = ("mermaid_cli", "chrome", "node", "pnpm")
    required = basic + mermaid if require_mermaid else basic
    missing = _missing_paths(tools, required)
    versions: dict[str, str | None] = {
        "libreoffice": None,
        "pdftoppm": None,
        "mermaid_cli": None,
        "chrome": None,
        "node": None,
        "pnpm": None,
    }
    failures: dict[str, str] = {}

    if "libreoffice" not in missing:
        versions["libreoffice"], error = _libreoffice_smoke(tools.libreoffice or "")
        if error:
            failures["libreoffice"] = error
    if "pdftoppm" not in missing:
        versions["pdftoppm"], error = _command_version(
            tools.pdftoppm or "", ["-v"]
        )
        if error:
            failures["pdftoppm"] = error

    if require_mermaid:
        version_arguments = {
            "mermaid_cli": ["--version"],
            "chrome": ["--version"],
            "node": ["--version"],
            "pnpm": ["--version"],
        }
        for name, arguments in version_arguments.items():
            if name in missing:
                continue
            versions[name], error = _command_version(
                getattr(tools, name) or "", arguments
            )
            if error:
                failures[name] = error

    return ReadinessReport(
        tools=tools,
        versions=versions,
        probe_failures=failures,
        missing=tuple(sorted(missing)),
    )


def _publication_tools_state(tools: PublicationTools) -> tuple[tuple[object, ...], ...]:
    state: list[tuple[object, ...]] = []
    for name, value in asdict(tools).items():
        if not value:
            state.append((name, None))
            continue
        try:
            metadata = Path(value).stat()
        except OSError:
            state.append((name, value, None))
            continue
        state.append(
            (
                name,
                value,
                metadata.st_dev,
                metadata.st_ino,
                metadata.st_mode,
                metadata.st_size,
                metadata.st_mtime_ns,
            )
        )
    return tuple(state)


@lru_cache(maxsize=32)
def _publication_readiness_cached(
    tools: PublicationTools,
    require_mermaid: bool,
    tool_state: tuple[tuple[object, ...], ...],
) -> ReadinessReport:
    del tool_state
    return probe_publication_readiness(
        tools,
        require_mermaid=require_mermaid,
    )


def publication_readiness(
    repository_root: Path,
    *,
    require_mermaid: bool = False,
) -> ReadinessReport:
    tools = resolve_publication_tools(repository_root.resolve())
    return _publication_readiness_cached(
        tools,
        require_mermaid,
        _publication_tools_state(tools),
    )
