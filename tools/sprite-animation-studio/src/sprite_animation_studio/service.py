"""Application use cases and fail-closed run lifecycle."""

from dataclasses import dataclass, field
import hashlib
import json
import os
import re
import stat
from io import BytesIO
from pathlib import Path
from uuid import uuid4

from .curation import CurationState, save_curation
from .delivery import DeliveryBlockedError, FigmaDeliveryPacket, ProjectFigmaRegistry
from .engine import EngineContractError, EnginePolicy, EngineResult, SpriteEngine, trusted_engine_policy
from PIL import Image, UnidentifiedImageError
from base_tool_contracts import AnchorEvidenceError, ApprovedAnchorRegistry
from base_tool_contracts import confined_staging_read_bytes, safe_staging_write_bytes
from .exporter import ExportResult, export_run
from .imports import DeclaredSource, ImportedImage, discard_import_bytes, import_metadata, revalidate_imported_image
from .lineage import write_lineage
from .models import SpriteAnimationRequest
from .paths import RunPaths, resolve_project_path, create_run_paths, revalidate_run_paths, stable_run_tree


class RunNotFoundError(KeyError):
    pass


class RunBlockedError(RuntimeError):
    pass


_MAX_ANCHOR_BYTES = 25 * 1024 * 1024
_MAX_ANCHOR_DIMENSION = 4096
_ALLOWED_ANCHOR_FORMATS = {"PNG", "JPEG", "WEBP"}


def _read_project_image(project_root: Path, source_path: str, *, expected_sha256: str | None = None) -> bytes:
    """Read and decode one bounded project image without following path links."""
    relative = Path(source_path)
    if relative.is_absolute() or not relative.parts or any(part in {"", ".", ".."} for part in relative.parts):
        raise ValueError("approved anchor source_path must be a confined project image")
    directory_descriptor = -1
    descriptor = -1
    try:
        directory_descriptor = os.open(
            project_root,
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0),
        )
        directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
        for component in relative.parts[:-1]:
            next_descriptor = os.open(component, directory_flags, dir_fd=directory_descriptor)
            os.close(directory_descriptor)
            directory_descriptor = next_descriptor
        descriptor = os.open(
            relative.parts[-1],
            os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=directory_descriptor,
        )
        attributes = os.fstat(descriptor)
        if not stat.S_ISREG(attributes.st_mode):
            raise ValueError("approved anchor source must be a regular file, not a link")
        if attributes.st_size > _MAX_ANCHOR_BYTES:
            raise ValueError("approved anchor image exceeds the 25 MiB safety limit")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(1024 * 1024, _MAX_ANCHOR_BYTES + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > _MAX_ANCHOR_BYTES:
                raise ValueError("approved anchor image exceeds the 25 MiB safety limit")
        data = b"".join(chunks)
    except OSError as error:
        raise ValueError("approved anchor source must be a readable regular file without links") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if directory_descriptor >= 0:
            os.close(directory_descriptor)
    if expected_sha256 is not None and hashlib.sha256(data).hexdigest() != expected_sha256:
        raise ValueError("approved anchor source SHA-256 does not match project-owned evidence")
    try:
        with Image.open(BytesIO(data)) as image:
            if image.format not in _ALLOWED_ANCHOR_FORMATS:
                raise ValueError("approved anchor must be a supported PNG, JPEG, or WebP image")
            if max(image.size) > _MAX_ANCHOR_DIMENSION or min(image.size) < 1:
                raise ValueError("approved anchor image dimensions are outside the supported range")
            image.load()
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as error:
        raise ValueError("approved anchor must be a supported PNG, JPEG, or WebP image") from error
    return data


def _read_staged_file(project_root: Path, path: Path, *, expected_sha256: str | None = None) -> bytes:
    return confined_staging_read_bytes(project_root, path, expected_sha256=expected_sha256)


def _import_engine_policy() -> EnginePolicy:
    config = b"sprite.import.v1|subscription_handoff_import|INCLUDED_OR_LOCAL_HANDOFF|provider_call_made=false"
    return EnginePolicy("sprite.import.v1", "subscription_handoff_import", True, hashlib.sha256(config).hexdigest())


@dataclass
class RunRecord:
    run_id: str
    request: SpriteAnimationRequest
    paths: RunPaths
    lineage: Path
    status: str
    anchor_bytes: bytes
    engine_policy: EnginePolicy
    anchor_verification: str
    anchor_evidence: dict[str, str]
    frame_count: int = 0
    result: EngineResult | None = None
    generation_output_sha256: tuple[str, ...] = ()
    export_output_sha256: dict[str, str] = field(default_factory=dict)
    curation: CurationState | None = None
    export: ExportResult | None = None
    warnings: list[str] = field(default_factory=list)
    run_mode: str = "simulated"
    imported_images: tuple[ImportedImage, ...] = ()
    provider_call_made: bool = False

    def public_view(self) -> dict[str, object]:
        imported_files = [
            {
                "index": image.order,
                "sha256": image.sha256,
                "format": image.detected_format,
                "width": image.width,
                "height": image.height,
                "has_alpha": image.has_alpha,
            }
            for image in self.imported_images
        ]
        cost_route = "INCLUDED_OR_LOCAL_HANDOFF" if self.run_mode == "subscription_handoff_import" else "EXPLICIT_ENGINE_ROUTE"
        return {
            "run_id": self.run_id,
            "status": self.status,
            "frame_count": self.frame_count,
            "selected": self.curation.selected if self.curation else [],
            "warnings": self.warnings,
            "lineage": {"file": self.lineage.name, "figma_node_url": str(self.request.anchor.figma_node_url)},
            "anchor_verification": self.anchor_verification,
            "engine": {
                "provenance": self.engine_policy.provenance,
                "delivery_eligible": self.engine_policy.delivery_eligible and self.anchor_verification == "ANCHOR_EVIDENCE_VERIFIED",
                "adapter_id": self.engine_policy.adapter_id,
                "config_sha256": self.engine_policy.config_sha256,
            },
            "cost": {
                "cost_route": cost_route,
                "provider_call_made": self.provider_call_made,
            },
            "cost_route": cost_route,
            "provider_call_made": self.provider_call_made,
            "declared_source": self.imported_images[0].declared_source if self.imported_images else None,
            "imported_files": imported_files,
            "run_mode": self.run_mode,
            "imports": [import_metadata(image) for image in self.imported_images],
        }


class SpriteAnimationService:
    def __init__(self, project_root: Path, engine: SpriteEngine, registry: ProjectFigmaRegistry | None = None, project_id: str | None = None, anchor_registry: ApprovedAnchorRegistry | None = None, run_mode: str = "subscription_handoff_import") -> None:
        if project_id is None or re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", project_id) is None:
            raise ValueError("a canonical project_id is required for every Sprite Animation Studio instance")
        self._project_root = project_root.resolve()
        self._engine = engine
        self._engine_policy = trusted_engine_policy(engine)
        self._registry = registry
        self._project_id = project_id
        self._anchor_registry = anchor_registry
        if run_mode not in {"subscription_handoff_import", "simulated", "pinned_sprite_gen"}:
            raise ValueError("unsupported Sprite Animation Studio run mode")
        expected_provenance = {"simulated": "simulated", "pinned_sprite_gen": "pinned_sprite_gen"}.get(run_mode)
        if (
            expected_provenance is not None
            and self._engine_policy.provenance in {"simulated", "pinned_sprite_gen"}
            and self._engine_policy.provenance != expected_provenance
        ):
            raise ValueError("Sprite Animation Studio run mode does not match the configured engine")
        self._run_mode = run_mode
        if self._anchor_registry is not None:
            self._anchor_registry.assert_project_owned(self._project_root)
        self._runs: dict[str, RunRecord] = {}

    def create_run(self, request: SpriteAnimationRequest) -> RunRecord:
        if self._run_mode == "subscription_handoff_import":
            raise RunBlockedError("MODE_NOT_AVAILABLE")
        if self._project_id is not None and request.project_id != self._project_id:
            raise ValueError(f"request project_id must match configured project_id {self._project_id!r}")
        if self._registry is not None:
            try:
                self._registry.validate_anchor_url(request.project_id, str(request.anchor.figma_node_url))
            except DeliveryBlockedError as error:
                raise ValueError(str(error)) from error
        anchor_path = resolve_project_path(self._project_root, request.anchor.source_path)
        run_id = uuid4().hex
        paths = create_run_paths(self._project_root, request.asset_id, request.action.name, run_id)
        revalidate_run_paths(self._project_root, paths)
        anchor_bytes = _read_project_image(self._project_root, request.anchor.source_path)
        anchor_verification = "ANCHOR_ROUTE_SYNTAX_VALID" if self._registry is not None else "ANCHOR_UNVERIFIED"
        anchor_evidence: dict[str, str] = {}
        if self._anchor_registry is not None:
            try:
                anchor_evidence = self._anchor_registry.evidence(project_id=request.project_id, source_path=request.anchor.source_path, figma_node_url=str(request.anchor.figma_node_url), source_bytes=anchor_bytes)
                anchor_verification = anchor_evidence["verification_state"]
            except AnchorEvidenceError as error:
                raise ValueError(str(error)) from error
        try:
            with stable_run_tree(self._project_root, paths) as stable:
                stable_run = stable.run_dir
                stable_frames = stable.open_directory("frames", expected_identity=paths.frames_identity)
                stable_engine_run = stable.open_directory("sprite-gen-run", create=True)
                engine_anchor = safe_staging_write_bytes(stable_run, f"anchor{anchor_path.suffix.lower() or '.png'}", anchor_bytes)
                engine_request = request.model_copy(update={"anchor": request.anchor.model_copy(update={"source_path": str(engine_anchor)})})
                lineage = write_lineage(request, anchor_bytes, stable_run, engine={"validation_state": "NOT_RUN"}, anchor_verification=anchor_verification, anchor_evidence=anchor_evidence).resolve()
                record = RunRecord(run_id=run_id, request=request, paths=paths, lineage=lineage, status="blocked", anchor_bytes=anchor_bytes, engine_policy=self._engine_policy, anchor_verification=anchor_verification, anchor_evidence=anchor_evidence, run_mode=self._run_mode)
                self._runs[run_id] = record
                generated = self._engine.generate(engine_request, stable_frames, stable_engine_run)
                record.provider_call_made = self._run_mode == "pinned_sprite_gen"
                result = EngineResult(frames=tuple(path.resolve() for path in generated.frames), provenance=generated.provenance, delivery_eligible=generated.delivery_eligible, stdout=generated.stdout, stderr=generated.stderr)
        except (EngineContractError, ValueError) as error:
            record = self._runs.get(run_id)
            if record is None:
                raise ValueError(str(error)) from error
            record.warnings.append(str(error))
            return record
        try:
            revalidate_run_paths(self._project_root, paths)
        except ValueError as error:
            record.warnings.append(str(error))
            return record
        try:
            anchor_unchanged = _read_project_image(
                self._project_root,
                request.anchor.source_path,
                expected_sha256=hashlib.sha256(anchor_bytes).hexdigest(),
            ) == anchor_bytes
        except ValueError:
            anchor_unchanged = False
        if not anchor_unchanged:
            record.warnings.append("approved anchor changed during generation; the run was blocked without overwriting the source")
            return record
        if result.provenance != self._engine_policy.provenance or result.delivery_eligible != self._engine_policy.delivery_eligible:
            record.warnings.append("engine result provenance or delivery eligibility does not match the configured adapter policy")
            return record
        try:
            self._validate_engine_result(result, request.action.frame_count, paths.frames_dir, anchor_bytes)
        except EngineContractError as error:
            record.warnings.append(str(error))
            return record
        record.generation_output_sha256 = tuple(hashlib.sha256(_read_staged_file(self._project_root, path)).hexdigest() for path in result.frames)
        record.result = result
        with stable_run_tree(self._project_root, paths) as stable:
            record.lineage = write_lineage(request, anchor_bytes, stable.run_dir, engine=self._engine_evidence(record.generation_output_sha256), anchor_verification=anchor_verification, anchor_evidence=anchor_evidence).resolve()
        record.status = "generated"
        record.frame_count = len(result.frames)
        return record

    def create_import_run(self, request: SpriteAnimationRequest, frames: tuple[ImportedImage, ...], declared_source: DeclaredSource) -> RunRecord:
        if self._run_mode != "subscription_handoff_import":
            raise RunBlockedError("MODE_NOT_AVAILABLE")
        if request.project_id != self._project_id:
            raise ValueError(f"request project_id must match configured project_id {self._project_id!r}")
        if len(frames) != request.action.frame_count:
            raise ValueError(f"import returned {len(frames)} frames; expected {request.action.frame_count}")
        if any(image.declared_source != declared_source or image.order != index for index, image in enumerate(frames)):
            raise ValueError("import frame metadata does not match declared source or upload order")
        frames = tuple(revalidate_imported_image(frame) for frame in frames)
        dimensions = {(image.width, image.height) for image in frames}
        if len(dimensions) != 1:
            raise ValueError("import sprite frame dimensions must match")
        visual_hashes: list[str] = []
        for frame in frames:
            with Image.open(BytesIO(frame.data)) as opened:
                rgba = opened.convert("RGBA")
                if rgba.getchannel("A").getbbox() is None:
                    raise ValueError("import sprite frame must not be fully transparent")
                visual_hashes.append(hashlib.sha256(rgba.tobytes()).hexdigest())
        if len(visual_hashes) != len(set(visual_hashes)):
            raise ValueError("import sprite frames must not be pixel-duplicates")
        if self._registry is not None:
            try:
                self._registry.validate_anchor_url(request.project_id, str(request.anchor.figma_node_url))
            except DeliveryBlockedError as error:
                raise ValueError(str(error)) from error
        anchor_path = resolve_project_path(self._project_root, request.anchor.source_path)
        anchor_bytes = _read_project_image(self._project_root, request.anchor.source_path)
        anchor_verification = "ANCHOR_ROUTE_SYNTAX_VALID" if self._registry is not None else "ANCHOR_UNVERIFIED"
        anchor_evidence: dict[str, str] = {}
        if self._anchor_registry is not None:
            try:
                anchor_evidence = self._anchor_registry.evidence(project_id=request.project_id, source_path=request.anchor.source_path, figma_node_url=str(request.anchor.figma_node_url), source_bytes=anchor_bytes)
                anchor_verification = anchor_evidence["verification_state"]
            except AnchorEvidenceError as error:
                raise ValueError(str(error)) from error
        run_id = uuid4().hex
        paths = create_run_paths(self._project_root, request.asset_id, request.action.name, run_id)
        revalidate_run_paths(self._project_root, paths)
        policy = _import_engine_policy()
        warnings: list[str] = []
        if request.mode == "effect_stages" and any(not frame.has_alpha for frame in frames):
            warnings.append("effect frame has no alpha channel; opaque backgrounds may require cleanup")
        with stable_run_tree(self._project_root, paths) as stable:
            stable_frames = stable.open_directory("frames", expected_identity=paths.frames_identity)
            safe_staging_write_bytes(stable.run_dir, f"anchor{anchor_path.suffix.lower() or '.png'}", anchor_bytes)
            frame_paths: list[Path] = []
            for frame in frames:
                with Image.open(BytesIO(frame.data)) as opened:
                    encoded = BytesIO()
                    opened.convert("RGBA").save(encoded, format="PNG")
                frame_paths.append(safe_staging_write_bytes(stable_frames, f"frame-{frame.order:03d}.png", encoded.getvalue()).resolve())
            result = EngineResult(frames=tuple(frame_paths), provenance=policy.provenance, delivery_eligible=True)
            output_sha256 = tuple(hashlib.sha256(_read_staged_file(self._project_root, path)).hexdigest() for path in frame_paths)
            lineage = write_lineage(request, anchor_bytes, stable.run_dir, engine=self._engine_evidence(output_sha256, policy=policy), anchor_verification=anchor_verification, anchor_evidence=anchor_evidence, imported_images=[import_metadata(frame) for frame in frames], run_mode=self._run_mode).resolve()
        record = RunRecord(run_id=run_id, request=request, paths=paths, lineage=lineage, status="generated", anchor_bytes=anchor_bytes, engine_policy=policy, anchor_verification=anchor_verification, anchor_evidence=anchor_evidence, frame_count=len(frames), result=result, generation_output_sha256=output_sha256, warnings=warnings, run_mode=self._run_mode, imported_images=tuple(discard_import_bytes(frame) for frame in frames))
        self._runs[run_id] = record
        return record

    def config(self) -> dict[str, object]:
        routing_state = "NOT_CONFIGURED"
        if self._registry is not None and self._project_id is not None:
            routing_state = self._registry.routing_state(self._project_id)
        policy = _import_engine_policy() if self._run_mode == "subscription_handoff_import" else self._engine_policy
        return {
            "project_id": self._project_id,
            "run_mode": self._run_mode,
            "engine_provenance": policy.provenance,
            "engine_adapter_id": policy.adapter_id,
            "engine_config_sha256": policy.config_sha256,
            "engine_delivery_eligible": policy.delivery_eligible,
            "delivery_eligible": policy.delivery_eligible and self._anchor_registry is not None and self._registry is not None,
            "cost_route": "INCLUDED_OR_LOCAL_HANDOFF" if self._run_mode == "subscription_handoff_import" else "EXPLICIT_ENGINE_ROUTE",
            "provider_call_made": False,
            "routing_state": routing_state,
            "anchor_evidence_state": "CONFIGURED" if self._anchor_registry is not None else "ANCHOR_EVIDENCE_REQUIRED",
        }

    def get_run(self, run_id: str) -> RunRecord:
        try:
            return self._runs[run_id]
        except KeyError as error:
            raise RunNotFoundError(run_id) from error

    def save_curation(self, run_id: str, curation: CurationState) -> RunRecord:
        record = self.get_run(run_id)
        if record.status == "blocked":
            raise RunBlockedError("blocked runs cannot be curated")
        with stable_run_tree(self._project_root, record.paths) as stable:
            save_curation(stable.run_dir, curation)
        revalidate_run_paths(self._project_root, record.paths)
        record.curation = curation
        record.status = "curated"
        return record

    def candidate_frame(self, run_id: str, frame_index: int) -> bytes:
        record = self.get_run(run_id)
        if frame_index < 0 or frame_index >= record.frame_count:
            raise ValueError("candidate frame index is outside generated frames")
        frame = record.paths.frames_dir / f"frame-{frame_index:03d}.png"
        resolved = frame.resolve()
        if record.paths.frames_dir.resolve() not in resolved.parents or not resolved.is_file():
            raise RunBlockedError("candidate frame file is unavailable")
        try:
            return _read_staged_file(self._project_root, resolved, expected_sha256=record.generation_output_sha256[frame_index])
        except ValueError as error:
            raise RunBlockedError("candidate frame is unavailable or changed") from error

    def approved_anchor(self, run_id: str) -> bytes:
        record = self.get_run(run_id)
        return record.anchor_bytes

    def export(self, run_id: str, curation: CurationState) -> RunRecord:
        record = self.get_run(run_id)
        if record.status == "blocked":
            raise RunBlockedError("blocked runs cannot be exported")
        if record.result is None or not record.engine_policy.delivery_eligible:
            provenance = record.engine_policy.provenance
            raise RunBlockedError(f"{provenance} engine output is not eligible for export or Figma delivery")
        self._revalidate_runtime(record)
        if record.anchor_verification != "ANCHOR_EVIDENCE_VERIFIED":
            raise RunBlockedError("project-owned approved-anchor evidence is required before export or Figma delivery")
        try:
            self._validate_engine_result(record.result, record.request.action.frame_count, record.paths.frames_dir, record.anchor_bytes)
        except EngineContractError as error:
            raise RunBlockedError(str(error)) from error
        if len(curation.selected) != record.request.action.frame_count:
            record.status = "blocked"
            record.warnings.append("all requested frames must be selected before export")
            raise RunBlockedError("all requested frames must be selected before export")
        with stable_run_tree(self._project_root, record.paths) as stable:
            stable_frames = stable.open_directory("frames", expected_identity=record.paths.frames_identity)
            stable_exports = stable.open_directory("exports", expected_identity=record.paths.exports_identity)
            stable_selected = stable.open_directory(f"exports/frames/{record.request.action.name}", create=True)
            stable_godot = stable.open_directory("exports/godot", create=True)
            exported = export_run(stable.run_dir, stable_frames, stable_exports, stable_selected, stable_godot, record.request, curation, frame_sha256=record.generation_output_sha256, engine=self._engine_evidence(record.generation_output_sha256, policy=record.engine_policy), anchor_sha256=hashlib.sha256(record.anchor_bytes).hexdigest(), anchor_verification=record.anchor_verification, anchor_evidence=record.anchor_evidence, imported_images=[import_metadata(image) for image in record.imported_images], run_mode=record.run_mode)
            record.export = ExportResult(exported.frames_dir.resolve(), exported.atlas.resolve(), exported.contact_sheet.resolve(), exported.gif.resolve(), exported.manifest.resolve(), exported.godot_handoff.resolve())
            record.lineage = write_lineage(record.request, record.anchor_bytes, stable.run_dir, engine=self._engine_evidence(record.generation_output_sha256, policy=record.engine_policy), anchor_verification=record.anchor_verification, anchor_evidence=record.anchor_evidence, imported_images=[import_metadata(image) for image in record.imported_images], run_mode=record.run_mode).resolve()
        try:
            revalidate_run_paths(self._project_root, record.paths)
        except ValueError as error:
            raise RunBlockedError(str(error)) from error
        record.curation = curation
        record.export_output_sha256 = self._current_export_hashes(record)
        record.status = "exported"
        return record

    def prepare_figma_delivery(self, run_id: str) -> FigmaDeliveryPacket:
        record = self.get_run(run_id)
        if record.status != "exported" or record.export is None or record.curation is None:
            raise RunBlockedError("curated export is required before Figma delivery can be prepared")
        if record.result is None or not record.engine_policy.delivery_eligible:
            provenance = record.engine_policy.provenance
            raise RunBlockedError(f"{provenance} engine output is not eligible for Figma delivery")
        if record.anchor_verification != "ANCHOR_EVIDENCE_VERIFIED":
            raise RunBlockedError("project-owned approved-anchor evidence is required before Figma delivery")
        if self._registry is None:
            raise RunBlockedError("Figma target registry is unavailable for this run")
        self._revalidate_runtime(record)
        self._registry.assert_unchanged()
        self._validate_export_evidence(record)
        target = self._registry.resolve_ready_target(record.request.project_id)
        if not record.curation.selected:
            raise RunBlockedError("selected frames are required before Figma delivery can be prepared")
        deliverables = [
            self._deliverable("atlas", self._project_relative(record.export.atlas), record.export.atlas),
            self._deliverable("contact_sheet", self._project_relative(record.export.contact_sheet), record.export.contact_sheet),
            self._deliverable("preview_gif", self._project_relative(record.export.gif), record.export.gif),
            self._deliverable("lineage", self._project_relative(record.lineage), record.lineage),
            self._deliverable("manifest", self._project_relative(record.export.manifest), record.export.manifest),
            self._deliverable("godot_handoff", self._project_relative(record.export.godot_handoff), record.export.godot_handoff),
        ]
        for frame in self._selected_export_frames(record):
            deliverables.append(self._deliverable("selected_frame", self._project_relative(frame), frame))
        return FigmaDeliveryPacket(
            run_id=record.run_id,
            project_id=record.request.project_id,
            mode=record.request.mode,
            anchor_figma_node_url=str(record.request.anchor.figma_node_url),
            target=target,
            engine=self._engine_evidence(record.generation_output_sha256, policy=record.engine_policy),
            anchor_verification=record.anchor_verification,
            anchor_evidence=record.anchor_evidence,
            visual_deliverables=deliverables,
        )

    def _project_relative(self, path: Path) -> str:
        try:
            return path.relative_to(self._project_root).as_posix()
        except ValueError as error:
            raise RunBlockedError("delivery output is outside the project workspace") from error

    def _validate_export_evidence(self, record: RunRecord) -> None:
        assert record.export is not None
        try:
            manifest = json.loads(_read_staged_file(self._project_root, record.export.manifest).decode("utf-8"))
            selected = self._selected_export_frames(record)
            selected_hashes = [hashlib.sha256(_read_staged_file(self._project_root, path)).hexdigest() for path in selected]
            visual_hashes = {
                "atlas_sha256": hashlib.sha256(_read_staged_file(self._project_root, record.export.atlas)).hexdigest(),
                "contact_sheet_sha256": hashlib.sha256(_read_staged_file(self._project_root, record.export.contact_sheet)).hexdigest(),
                "preview_gif_sha256": hashlib.sha256(_read_staged_file(self._project_root, record.export.gif)).hexdigest(),
                "godot_handoff_sha256": hashlib.sha256(_read_staged_file(self._project_root, record.export.godot_handoff)).hexdigest(),
            }
        except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
            raise RunBlockedError("export provenance manifest is unavailable or invalid") from error
        if manifest.get("anchor_verification") != "ANCHOR_EVIDENCE_VERIFIED":
            raise RunBlockedError("export manifest has no verified anchor evidence")
        engine = manifest.get("engine", {})
        if engine.get("config_sha256") != record.engine_policy.config_sha256 or not engine.get("delivery_eligible"):
            raise RunBlockedError("export manifest engine provenance does not match the configured adapter")
        if manifest.get("selected_sha256") != selected_hashes:
            raise RunBlockedError("export frame hashes do not match the manifest")
        if any(manifest.get(key) != value for key, value in visual_hashes.items()):
            raise RunBlockedError("export visual deliverable hashes do not match the manifest")
        if manifest.get("anchor_evidence") != record.anchor_evidence:
            raise RunBlockedError("export manifest anchor evidence does not match the verified run")
        if self._current_export_hashes(record) != record.export_output_sha256:
            raise RunBlockedError("an exported sprite deliverable changed after export")

    def _engine_evidence(self, output_sha256: tuple[str, ...], *, policy: EnginePolicy | None = None) -> dict[str, object]:
        selected_policy = policy or self._engine_policy
        return {
            "adapter_id": selected_policy.adapter_id,
            "provenance": selected_policy.provenance,
            "delivery_eligible": selected_policy.delivery_eligible,
            "config_sha256": selected_policy.config_sha256,
            "validation_state": "SERVICE_POLICY_VERIFIED",
            "output_sha256": list(output_sha256),
            "cost_route": "INCLUDED_OR_LOCAL_HANDOFF" if selected_policy.provenance == "subscription_handoff_import" else "EXPLICIT_ENGINE_ROUTE",
            "provider_call_made": selected_policy.provenance == "pinned_sprite_gen",
        }

    def _revalidate_runtime(self, record: RunRecord) -> None:
        try:
            revalidate_run_paths(self._project_root, record.paths)
        except ValueError as error:
            raise RunBlockedError(str(error)) from error
        if record.run_mode == "subscription_handoff_import":
            if record.engine_policy != _import_engine_policy():
                raise RunBlockedError("import policy changed after generation")
        else:
            try:
                current_policy = trusted_engine_policy(self._engine)
            except EngineContractError as error:
                raise RunBlockedError(str(error)) from error
            if current_policy != record.engine_policy or not current_policy.delivery_eligible:
                raise RunBlockedError("configured engine policy changed or is not delivery eligible")
        try:
            current_bytes = _read_project_image(
                self._project_root,
                record.request.anchor.source_path,
                expected_sha256=hashlib.sha256(record.anchor_bytes).hexdigest(),
            )
        except ValueError as error:
            raise RunBlockedError("approved anchor is unavailable during revalidation") from error
        if current_bytes != record.anchor_bytes or self._anchor_registry is None:
            raise RunBlockedError("approved anchor bytes or project-owned evidence changed after generation")
        try:
            self._anchor_registry.assert_unchanged()
            evidence = self._anchor_registry.evidence(project_id=record.request.project_id, source_path=record.request.anchor.source_path, figma_node_url=str(record.request.anchor.figma_node_url), source_bytes=current_bytes)
        except AnchorEvidenceError as error:
            raise RunBlockedError(str(error)) from error
        if evidence != record.anchor_evidence:
            raise RunBlockedError("approved-anchor evidence changed after generation")
        try:
            current_hashes = tuple(
                hashlib.sha256(_read_staged_file(self._project_root, path, expected_sha256=expected)).hexdigest()
                for path, expected in zip(record.result.frames, record.generation_output_sha256, strict=True)
            ) if record.result else ()
        except (ValueError, OSError) as error:
            raise RunBlockedError("generated sprite frames are unavailable or changed") from error
        if current_hashes != record.generation_output_sha256:
            raise RunBlockedError("generated sprite frames changed after generation")

    def _current_export_hashes(self, record: RunRecord) -> dict[str, str]:
        assert record.export is not None
        hashes = {
            "atlas": hashlib.sha256(_read_staged_file(self._project_root, record.export.atlas)).hexdigest(),
            "contact_sheet": hashlib.sha256(_read_staged_file(self._project_root, record.export.contact_sheet)).hexdigest(),
            "preview_gif": hashlib.sha256(_read_staged_file(self._project_root, record.export.gif)).hexdigest(),
            "lineage": hashlib.sha256(_read_staged_file(self._project_root, record.lineage)).hexdigest(),
            "manifest": hashlib.sha256(_read_staged_file(self._project_root, record.export.manifest)).hexdigest(),
            "godot_handoff": hashlib.sha256(_read_staged_file(self._project_root, record.export.godot_handoff)).hexdigest(),
        }
        for frame in self._selected_export_frames(record):
            hashes[f"frame:{frame.name}"] = hashlib.sha256(_read_staged_file(self._project_root, frame)).hexdigest()
        return hashes

    @staticmethod
    def _selected_export_frames(record: RunRecord) -> list[Path]:
        assert record.export is not None and record.curation is not None
        return [record.export.frames_dir / f"frame-{position:03d}.png" for position in range(len(record.curation.selected))]

    def _deliverable(self, kind: str, path: str, absolute: Path) -> dict[str, str]:
        return {"kind": kind, "project_relative_path": path, "sha256": hashlib.sha256(_read_staged_file(self._project_root, absolute)).hexdigest()}

    def _validate_engine_result(self, result: EngineResult, expected_count: int, frames_dir: Path, anchor_bytes: bytes) -> None:
        if len(result.frames) != expected_count:
            raise EngineContractError(f"engine returned {len(result.frames)} frames; expected {expected_count}")
        root = frames_dir.resolve()
        seen: set[Path] = set()
        visual_hashes: list[str] = []
        for frame in result.frames:
            resolved = frame.resolve()
            if root not in resolved.parents or resolved.suffix.lower() != ".png":
                raise EngineContractError("engine frame must be a PNG inside the run frame directory")
            if resolved in seen:
                raise EngineContractError("engine returned the same frame path more than once")
            seen.add(resolved)
            try:
                data = _read_staged_file(self._project_root, resolved)
                with Image.open(BytesIO(data)) as image:
                    rgba = image.convert("RGBA")
                    visual_hashes.append(hashlib.sha256(rgba.tobytes()).hexdigest())
                    if self._engine_policy.delivery_eligible and rgba.getbbox() is None:
                        raise EngineContractError("engine frame must not be fully transparent")
            except (OSError, ValueError, UnidentifiedImageError) as error:
                raise EngineContractError("engine frame must be a readable PNG") from error
        if self._engine_policy.delivery_eligible:
            with Image.open(BytesIO(anchor_bytes)) as image:
                anchor_visual = hashlib.sha256(image.convert("RGBA").tobytes()).hexdigest()
            if all(value == anchor_visual for value in visual_hashes):
                raise EngineContractError("delivery-eligible sprite frames must visibly differ from the anchor")
