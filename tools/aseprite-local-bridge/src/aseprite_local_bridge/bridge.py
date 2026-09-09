from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from typing import Callable, Mapping, Sequence
import uuid

from ._core import (
    ASSET_ID_PATTERN,
    EVIDENCE_CEILING,
    PNG_SIGNATURE,
    WINDOWS_RESERVED_NAMES,
    BridgeConfig,
    BridgeError,
    _is_within,
    _read_json,
    _reject_link_traversal,
    _relative_posix,
    _sha256,
)


Runner = Callable[..., subprocess.CompletedProcess[str]]


class AsepriteBridge:
    def __init__(
        self,
        config: BridgeConfig,
        executable: Path | str | None = None,
        runner: Runner | None = None,
        environ: Mapping[str, str] | None = None,
    ) -> None:
        self.config = config
        self._runner = runner or subprocess.run
        self._environ = dict(os.environ if environ is None else environ)
        self.executable = self._discover_executable(executable)

    def _discover_executable(self, explicit: Path | str | None) -> Path:
        if explicit is not None:
            candidate = Path(explicit).expanduser().resolve()
            if not candidate.is_file():
                raise BridgeError("ASEPRITE_UNAVAILABLE", f"explicit path not found: {candidate}")
            return candidate

        env_value = self._environ.get("ASEPRITE_PATH", "").strip()
        if env_value:
            candidate = Path(env_value).expanduser().resolve()
            if not candidate.is_file():
                raise BridgeError("ASEPRITE_UNAVAILABLE", "ASEPRITE_PATH does not point to a file")
            return candidate

        for name in ("aseprite", "Aseprite"):
            found = shutil.which(name, path=self._environ.get("PATH"))
            if found:
                candidate = Path(found).resolve()
                if candidate.is_file():
                    return candidate

        for candidate in self._common_install_paths():
            if candidate.is_file():
                return candidate.resolve()

        raise BridgeError(
            "ASEPRITE_UNAVAILABLE",
            "set --aseprite or ASEPRITE_PATH to a licensed Aseprite executable",
        )

    def _common_install_paths(self) -> tuple[Path, ...]:
        home = Path.home()
        values: list[Path] = []
        if os.name == "nt":
            program_files = self._environ.get("ProgramFiles", r"C:\Program Files")
            program_files_x86 = self._environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
            local_app_data = self._environ.get("LOCALAPPDATA", "")
            values.extend(
                [
                    Path(program_files) / "Aseprite" / "Aseprite.exe",
                    Path(program_files_x86) / "Aseprite" / "Aseprite.exe",
                    Path(program_files_x86)
                    / "Steam"
                    / "steamapps"
                    / "common"
                    / "Aseprite"
                    / "Aseprite.exe",
                ]
            )
            if local_app_data:
                values.append(Path(local_app_data) / "Programs" / "Aseprite" / "Aseprite.exe")
        elif sys_platform() == "darwin":
            values.extend(
                [
                    Path("/Applications/Aseprite.app/Contents/MacOS/aseprite"),
                    home
                    / "Library"
                    / "Application Support"
                    / "Steam"
                    / "steamapps"
                    / "common"
                    / "Aseprite"
                    / "Aseprite.app"
                    / "Contents"
                    / "MacOS"
                    / "aseprite",
                ]
            )
        else:
            values.extend(
                [
                    Path("/usr/bin/aseprite"),
                    Path("/usr/local/bin/aseprite"),
                    home / ".local" / "bin" / "aseprite",
                    home
                    / ".steam"
                    / "debian-installation"
                    / "steamapps"
                    / "common"
                    / "Aseprite"
                    / "aseprite",
                    home
                    / ".steam"
                    / "steam"
                    / "steamapps"
                    / "common"
                    / "Aseprite"
                    / "aseprite",
                ]
            )
        return tuple(values)

    def _run(self, arguments: Sequence[str]) -> subprocess.CompletedProcess[str]:
        command = [str(self.executable), *map(str, arguments)]
        try:
            result = self._runner(
                command,
                cwd=str(self.config.project_root),
                capture_output=True,
                text=True,
                timeout=self.config.timeout_seconds,
                check=False,
                shell=False,
            )
        except subprocess.TimeoutExpired as error:
            raise BridgeError(
                "ASEPRITE_TIMEOUT",
                f"command exceeded {self.config.timeout_seconds} seconds",
            ) from error
        except OSError as error:
            raise BridgeError("ASEPRITE_UNAVAILABLE", str(error)) from error
        if result.returncode != 0:
            detail = (result.stderr or result.stdout or f"exit {result.returncode}").strip()
            if len(detail) > 2000:
                detail = detail[:2000] + "…"
            raise BridgeError("ASEPRITE_COMMAND_FAILED", detail)
        return result

    def _base_batch_arguments(self) -> list[str]:
        args = ["-b"]
        if self.config.use_noinapp:
            args.append("--noinapp")
        return args

    def _version(self) -> str:
        result = self._run(["--version"])
        version = result.stdout.strip()
        if not version:
            raise BridgeError("ASEPRITE_COMMAND_FAILED", "--version returned empty output")
        return version.splitlines()[0].strip()

    def _resolve_source(self, source: str) -> Path:
        raw = Path(source)
        if raw.is_absolute():
            raise BridgeError("PATH_OUTSIDE_PROJECT", "source must be project-relative")
        _reject_link_traversal(
            self.config.project_root,
            raw,
            "SOURCE_SYMLINK_FORBIDDEN",
        )
        path = (self.config.project_root / raw).resolve()
        if not _is_within(path, self.config.project_root):
            raise BridgeError("PATH_OUTSIDE_PROJECT", source)
        if not path.exists() or not path.is_file():
            raise BridgeError("SOURCE_NOT_FOUND", source)
        if path.suffix.lower() not in self.config.allowed_source_extensions:
            raise BridgeError("UNSUPPORTED_SOURCE_EXTENSION", path.suffix.lower())
        if not any(_is_within(path, root) for root in self.config.source_roots):
            raise BridgeError("SOURCE_OUTSIDE_ALLOWED_ROOTS", source)
        return path

    @staticmethod
    def _validate_asset_id(asset_id: str) -> str:
        if not ASSET_ID_PATTERN.fullmatch(asset_id):
            raise BridgeError(
                "INVALID_ASSET_ID",
                "use 1-64 uppercase letters, digits, '_' or '-', starting with a letter/digit",
            )
        if asset_id.upper() in WINDOWS_RESERVED_NAMES:
            raise BridgeError(
                "INVALID_ASSET_ID",
                f"{asset_id} is a reserved Windows device name",
            )
        return asset_id

    @staticmethod
    def _lines(stdout: str) -> list[str]:
        return [line.strip() for line in stdout.splitlines() if line.strip()]

    def doctor(self) -> dict[str, object]:
        return {
            "status": "PASS",
            "operation": "doctor",
            "project_root": str(self.config.project_root),
            "config": _relative_posix(self.config.config_path, self.config.project_root),
            "aseprite_executable": str(self.executable),
            "aseprite_version": self._version(),
            "candidate_output_root": _relative_posix(
                self.config.candidate_output_root,
                self.config.project_root,
            ),
            "evidence_ceiling": "ASEPRITE_CALLABLE_ONLY_NO_ASSET_EXPORT_NO_GODOT_RUNTIME",
        }

    def inspect(self, source: str) -> dict[str, object]:
        path = self._resolve_source(source)
        base = self._base_batch_arguments()
        layers = self._run([*base, "--list-layer-hierarchy", str(path)])
        tags = self._run([*base, "--list-tags", str(path)])
        slices = self._run([*base, "--list-slices", str(path)])
        return {
            "status": "PASS",
            "operation": "inspect",
            "source": {
                "path": _relative_posix(path, self.config.project_root),
                "sha256": _sha256(path),
                "bytes": path.stat().st_size,
            },
            "layers": self._lines(layers.stdout),
            "tags": self._lines(tags.stdout),
            "slices": self._lines(slices.stdout),
            "evidence_ceiling": "ASEPRITE_METADATA_READBACK_ONLY_NO_ASSET_EXPORT_NO_GODOT_RUNTIME",
        }

    def _validate_export_files(self, png_path: Path, json_path: Path) -> dict[str, object]:
        try:
            png_size = png_path.stat().st_size
            with png_path.open("rb") as handle:
                png_header = handle.read(len(PNG_SIGNATURE))
        except OSError as error:
            raise BridgeError("EXPORT_OUTPUT_MISSING", png_path.name) from error
        if png_size <= len(PNG_SIGNATURE) or png_header != PNG_SIGNATURE:
            raise BridgeError("INVALID_PNG", png_path.name)

        data = _read_json(json_path, "INVALID_ASEPRITE_JSON")
        if not isinstance(data, dict):
            raise BridgeError("INVALID_ASEPRITE_JSON", "root must be an object")
        frames = data.get("frames")
        if not isinstance(frames, (list, dict)) or not frames:
            raise BridgeError("INVALID_ASEPRITE_JSON", "frames must be non-empty")
        meta = data.get("meta")
        if meta is not None and not isinstance(meta, dict):
            raise BridgeError("INVALID_ASEPRITE_JSON", "meta must be an object when present")
        return data

    def _receipt(
        self,
        source: Path,
        asset_id: str,
        png_path: Path,
        json_path: Path,
        aseprite_version: str,
    ) -> dict[str, object]:
        outputs = []
        for path in (png_path, json_path):
            outputs.append(
                {
                    "path": _relative_posix(path, self.config.project_root),
                    "sha256": _sha256(path),
                    "bytes": path.stat().st_size,
                }
            )
        return {
            "schema_version": 1,
            "status": "PASS",
            "operation": "export_candidate",
            "asset_id": asset_id,
            "source": {
                "path": _relative_posix(source, self.config.project_root),
                "sha256": _sha256(source),
                "bytes": source.stat().st_size,
            },
            "aseprite": {
                "version": aseprite_version,
                "executable_name": self.executable.name,
            },
            "export": {
                "sheet_type": self.config.sheet_type,
                "border_padding": self.config.border_padding,
                "shape_padding": self.config.shape_padding,
                "inner_padding": self.config.inner_padding,
            },
            "outputs": outputs,
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "evidence_ceiling": EVIDENCE_CEILING,
        }

    def _publish_stage(self, stage: Path, final: Path, replace_candidate: bool) -> None:
        if not final.exists():
            try:
                stage.replace(final)
            except OSError as error:
                raise BridgeError("ATOMIC_REPLACE_FAILED", str(error)) from error
            return
        if not replace_candidate:
            raise BridgeError("CANDIDATE_EXISTS", final.name)

        backup = final.parent / f".{final.name}-backup-{uuid.uuid4().hex}"
        try:
            final.replace(backup)
            stage.replace(final)
        except OSError as error:
            if backup.exists() and not final.exists():
                backup.replace(final)
            raise BridgeError("ATOMIC_REPLACE_FAILED", str(error)) from error
        try:
            shutil.rmtree(backup)
        except OSError as error:
            if final.exists():
                shutil.rmtree(final)
            backup.replace(final)
            raise BridgeError("ATOMIC_REPLACE_FAILED", f"backup cleanup failed: {error}") from error

    def export_candidate(
        self,
        source: str,
        asset_id: str,
        replace_candidate: bool = False,
    ) -> dict[str, object]:
        source_path = self._resolve_source(source)
        asset_id = self._validate_asset_id(asset_id)
        output_root = self.config.candidate_output_root
        final = output_root / asset_id
        if final.exists() and not replace_candidate:
            raise BridgeError("CANDIDATE_EXISTS", asset_id)
        output_root.mkdir(parents=True, exist_ok=True)
        if not _is_within(output_root.resolve(), self.config.project_root):
            raise BridgeError("PATH_OUTSIDE_PROJECT", str(output_root))

        stage = Path(tempfile.mkdtemp(prefix=f".{asset_id}-staging-", dir=output_root))
        stage_png = stage / f"{asset_id}.png"
        stage_json = stage / f"{asset_id}.json"
        stage_receipt = stage / f"{asset_id}.receipt.json"
        try:
            version = self._version()
            args = [
                *self._base_batch_arguments(),
                "--list-layer-hierarchy",
                "--list-tags",
                "--list-slices",
                str(source_path),
                "--sheet",
                str(stage_png),
                "--data",
                str(stage_json),
                "--format",
                "json-array",
                "--sheet-type",
                self.config.sheet_type,
                "--border-padding",
                str(self.config.border_padding),
                "--shape-padding",
                str(self.config.shape_padding),
                "--inner-padding",
                str(self.config.inner_padding),
            ]
            self._run(args)
            self._validate_export_files(stage_png, stage_json)
            receipt = self._receipt(
                source_path,
                asset_id,
                stage_png,
                stage_json,
                version,
            )
            # Convert stage-relative output paths to their final published paths.
            for output in receipt["outputs"]:  # type: ignore[index]
                name = Path(str(output["path"])).name
                output["path"] = _relative_posix(final / name, self.config.project_root)
            stage_receipt.write_text(
                json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            self._publish_stage(stage, final, replace_candidate)
            return {
                "status": "PASS",
                "operation": "export_candidate",
                "candidate_directory": _relative_posix(final, self.config.project_root),
                "receipt": receipt,
            }
        finally:
            if stage.exists():
                shutil.rmtree(stage)

    def validate_candidate(self, asset_id: str) -> dict[str, object]:
        asset_id = self._validate_asset_id(asset_id)
        root = self.config.candidate_output_root.resolve()
        candidate = (root / asset_id).resolve()
        if not _is_within(candidate, root):
            raise BridgeError("PATH_OUTSIDE_PROJECT", asset_id)
        if not candidate.is_dir():
            raise BridgeError("EXPORT_OUTPUT_MISSING", asset_id)

        png_path = candidate / f"{asset_id}.png"
        json_path = candidate / f"{asset_id}.json"
        receipt_path = candidate / f"{asset_id}.receipt.json"
        self._validate_export_files(png_path, json_path)
        receipt = _read_json(receipt_path, "RECEIPT_MISMATCH")
        if not isinstance(receipt, dict):
            raise BridgeError("RECEIPT_MISMATCH", "receipt root must be an object")
        if receipt.get("schema_version") != 1 or receipt.get("asset_id") != asset_id:
            raise BridgeError("RECEIPT_MISMATCH", "schema_version or asset_id differs")
        if receipt.get("evidence_ceiling") != EVIDENCE_CEILING:
            raise BridgeError("RECEIPT_MISMATCH", "evidence ceiling differs")

        source_record = receipt.get("source")
        if not isinstance(source_record, dict) or not isinstance(source_record.get("path"), str):
            raise BridgeError("RECEIPT_MISMATCH", "source record is invalid")
        source_path = self._resolve_source(source_record["path"])
        if source_record.get("sha256") != _sha256(source_path):
            raise BridgeError("RECEIPT_MISMATCH", "source sha256 differs")
        if source_record.get("bytes") != source_path.stat().st_size:
            raise BridgeError("RECEIPT_MISMATCH", "source byte count differs")

        output_records = receipt.get("outputs")
        if not isinstance(output_records, list) or len(output_records) != 2:
            raise BridgeError("RECEIPT_MISMATCH", "outputs must contain PNG and JSON")
        by_path: dict[str, Mapping[str, object]] = {}
        for record in output_records:
            if not isinstance(record, dict) or not isinstance(record.get("path"), str):
                raise BridgeError("RECEIPT_MISMATCH", "output record is invalid")
            raw_path = Path(record["path"])
            if raw_path.is_absolute():
                raise BridgeError("RECEIPT_MISMATCH", "output path must be relative")
            resolved = (self.config.project_root / raw_path).resolve()
            if not _is_within(resolved, candidate):
                raise BridgeError("RECEIPT_MISMATCH", "output path leaves candidate directory")
            by_path[record["path"]] = record

        for path in (png_path, json_path):
            key = _relative_posix(path, self.config.project_root)
            record = by_path.get(key)
            if record is None:
                raise BridgeError("RECEIPT_MISMATCH", f"missing output record: {key}")
            if record.get("sha256") != _sha256(path):
                raise BridgeError("RECEIPT_MISMATCH", f"sha256 differs: {path.name}")
            if record.get("bytes") != path.stat().st_size:
                raise BridgeError("RECEIPT_MISMATCH", f"byte count differs: {path.name}")

        return {
            "status": "PASS",
            "operation": "validate_candidate",
            "asset_id": asset_id,
            "candidate_directory": _relative_posix(candidate, self.config.project_root),
            "receipt": receipt,
            "evidence_ceiling": EVIDENCE_CEILING,
        }


def sys_platform() -> str:
    # Isolated for deterministic tests without mutating global sys.platform.
    import sys

    return sys.platform
