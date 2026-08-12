"""Application use cases and fail-closed run lifecycle."""

from dataclasses import dataclass, field
import hashlib
import json
import re
from io import BytesIO
from pathlib import Path
from uuid import uuid4

from .curation import CurationState, save_curation
from .delivery import DeliveryBlockedError, FigmaDeliveryPacket, ProjectFigmaRegistry
from .engine import EngineContractError, EnginePolicy, EngineResult, SpriteEngine, trusted_engine_policy
from PIL import Image, UnidentifiedImageError
from base_tool_contracts import AnchorEvidenceError, ApprovedAnchorRegistry
from .exporter import ExportResult, export_run
from .lineage import write_lineage
from .models import SpriteAnimationRequest
from .paths import RunPaths, resolve_project_path, create_run_paths, revalidate_run_paths, stable_run_path


class RunNotFoundError(KeyError):
    pass


class RunBlockedError(RuntimeError):
    pass


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

    def public_view(self) -> dict[str, object]:
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
        }


class SpriteAnimationService:
    def __init__(self, project_root: Path, engine: SpriteEngine, registry: ProjectFigmaRegistry | None = None, project_id: str | None = None, anchor_registry: ApprovedAnchorRegistry | None = None) -> None:
        if project_id is None or re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", project_id) is None:
            raise ValueError("a canonical project_id is required for every Sprite Animation Studio instance")
        self._project_root = project_root.resolve()
        self._engine = engine
        self._engine_policy = trusted_engine_policy(engine)
        self._registry = registry
        self._project_id = project_id
        self._anchor_registry = anchor_registry
        if self._anchor_registry is not None:
            self._anchor_registry.assert_project_owned(self._project_root)
        self._runs: dict[str, RunRecord] = {}

    def create_run(self, request: SpriteAnimationRequest) -> RunRecord:
        if self._project_id is not None and request.project_id != self._project_id:
            raise ValueError(f"request project_id must match configured project_id {self._project_id!r}")
        if self._registry is not None:
            try:
                self._registry.validate_anchor_url(request.project_id, str(request.anchor.figma_node_url))
            except DeliveryBlockedError as error:
                raise ValueError(str(error)) from error
        anchor_path = resolve_project_path(self._project_root, request.anchor.source_path)
        if not anchor_path.is_file():
            raise ValueError("approved anchor source_path must point to an existing project file")
        run_id = uuid4().hex
        paths = create_run_paths(self._project_root, request.asset_id, request.action.name, run_id)
        revalidate_run_paths(self._project_root, paths)
        anchor_bytes = anchor_path.read_bytes()
        anchor_verification = "ANCHOR_ROUTE_SYNTAX_VALID" if self._registry is not None else "ANCHOR_UNVERIFIED"
        anchor_evidence: dict[str, str] = {}
        if self._anchor_registry is not None:
            try:
                anchor_evidence = self._anchor_registry.evidence(project_id=request.project_id, source_path=request.anchor.source_path, figma_node_url=str(request.anchor.figma_node_url), source_bytes=anchor_bytes)
                anchor_verification = anchor_evidence["verification_state"]
            except AnchorEvidenceError as error:
                raise ValueError(str(error)) from error
        try:
            with stable_run_path(self._project_root, paths) as stable_run:
                engine_anchor = stable_run / f"anchor{anchor_path.suffix.lower() or '.png'}"
                engine_anchor.write_bytes(anchor_bytes)
                engine_request = request.model_copy(update={"anchor": request.anchor.model_copy(update={"source_path": str(engine_anchor)})})
                lineage = write_lineage(request, anchor_bytes, stable_run, engine={"validation_state": "NOT_RUN"}, anchor_verification=anchor_verification, anchor_evidence=anchor_evidence).resolve()
                record = RunRecord(run_id=run_id, request=request, paths=paths, lineage=lineage, status="blocked", anchor_bytes=anchor_bytes, engine_policy=self._engine_policy, anchor_verification=anchor_verification, anchor_evidence=anchor_evidence)
                self._runs[run_id] = record
                generated = self._engine.generate(engine_request, stable_run)
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
            anchor_unchanged = anchor_path.read_bytes() == anchor_bytes
        except OSError:
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
        record.generation_output_sha256 = tuple(hashlib.sha256(path.read_bytes()).hexdigest() for path in result.frames)
        record.result = result
        with stable_run_path(self._project_root, paths) as stable_run:
            record.lineage = write_lineage(request, anchor_bytes, stable_run, engine=self._engine_evidence(record.generation_output_sha256), anchor_verification=anchor_verification, anchor_evidence=anchor_evidence).resolve()
        record.status = "generated"
        record.frame_count = len(result.frames)
        return record

    def config(self) -> dict[str, object]:
        routing_state = "NOT_CONFIGURED"
        if self._registry is not None and self._project_id is not None:
            routing_state = self._registry.routing_state(self._project_id)
        return {
            "project_id": self._project_id,
            "engine_provenance": self._engine_policy.provenance,
            "engine_adapter_id": self._engine_policy.adapter_id,
            "engine_config_sha256": self._engine_policy.config_sha256,
            "engine_delivery_eligible": self._engine_policy.delivery_eligible,
            "delivery_eligible": self._engine_policy.delivery_eligible and self._anchor_registry is not None and self._registry is not None,
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
        save_curation(record.paths.run_dir, curation)
        record.curation = curation
        record.status = "curated"
        return record

    def candidate_frame(self, run_id: str, frame_index: int) -> Path:
        record = self.get_run(run_id)
        if frame_index < 0 or frame_index >= record.frame_count:
            raise ValueError("candidate frame index is outside generated frames")
        frame = record.paths.frames_dir / f"frame-{frame_index:03d}.png"
        resolved = frame.resolve()
        if record.paths.frames_dir.resolve() not in resolved.parents or not resolved.is_file():
            raise RunBlockedError("candidate frame file is unavailable")
        return resolved

    def approved_anchor(self, run_id: str) -> Path:
        record = self.get_run(run_id)
        anchor = resolve_project_path(self._project_root, record.request.anchor.source_path)
        if not anchor.is_file():
            raise RunBlockedError("approved anchor file is unavailable")
        return anchor

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
        with stable_run_path(self._project_root, record.paths) as stable_run:
            exported = export_run(stable_run, record.request, curation, engine=self._engine_evidence(record.generation_output_sha256), anchor_sha256=hashlib.sha256(record.anchor_bytes).hexdigest(), anchor_verification=record.anchor_verification, anchor_evidence=record.anchor_evidence)
            record.export = ExportResult(exported.frames_dir.resolve(), exported.atlas.resolve(), exported.contact_sheet.resolve(), exported.gif.resolve(), exported.manifest.resolve(), exported.godot_handoff.resolve())
            record.lineage = write_lineage(record.request, record.anchor_bytes, stable_run, engine=self._engine_evidence(record.generation_output_sha256), anchor_verification=record.anchor_verification, anchor_evidence=record.anchor_evidence).resolve()
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
        for frame in sorted(record.export.frames_dir.glob("*.png")):
            deliverables.append(self._deliverable("selected_frame", self._project_relative(frame), frame))
        return FigmaDeliveryPacket(
            run_id=record.run_id,
            project_id=record.request.project_id,
            mode=record.request.mode,
            anchor_figma_node_url=str(record.request.anchor.figma_node_url),
            target=target,
            engine=self._engine_evidence(record.generation_output_sha256),
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
            manifest = json.loads(record.export.manifest.read_text(encoding="utf-8"))
            selected = sorted(record.export.frames_dir.glob("*.png"))
            selected_hashes = [hashlib.sha256(path.read_bytes()).hexdigest() for path in selected]
            visual_hashes = {
                "atlas_sha256": hashlib.sha256(record.export.atlas.read_bytes()).hexdigest(),
                "contact_sheet_sha256": hashlib.sha256(record.export.contact_sheet.read_bytes()).hexdigest(),
                "preview_gif_sha256": hashlib.sha256(record.export.gif.read_bytes()).hexdigest(),
                "godot_handoff_sha256": hashlib.sha256(record.export.godot_handoff.read_bytes()).hexdigest(),
            }
        except (OSError, json.JSONDecodeError) as error:
            raise RunBlockedError("export provenance manifest is unavailable or invalid") from error
        if manifest.get("anchor_verification") != "ANCHOR_EVIDENCE_VERIFIED":
            raise RunBlockedError("export manifest has no verified anchor evidence")
        engine = manifest.get("engine", {})
        if engine.get("config_sha256") != self._engine_policy.config_sha256 or not engine.get("delivery_eligible"):
            raise RunBlockedError("export manifest engine provenance does not match the configured adapter")
        if manifest.get("selected_sha256") != selected_hashes:
            raise RunBlockedError("export frame hashes do not match the manifest")
        if any(manifest.get(key) != value for key, value in visual_hashes.items()):
            raise RunBlockedError("export visual deliverable hashes do not match the manifest")
        if manifest.get("anchor_evidence") != record.anchor_evidence:
            raise RunBlockedError("export manifest anchor evidence does not match the verified run")
        if self._current_export_hashes(record) != record.export_output_sha256:
            raise RunBlockedError("an exported sprite deliverable changed after export")

    def _engine_evidence(self, output_sha256: tuple[str, ...]) -> dict[str, object]:
        return {
            "adapter_id": self._engine_policy.adapter_id,
            "provenance": self._engine_policy.provenance,
            "delivery_eligible": self._engine_policy.delivery_eligible,
            "config_sha256": self._engine_policy.config_sha256,
            "validation_state": "SERVICE_POLICY_VERIFIED",
            "output_sha256": list(output_sha256),
        }

    def _revalidate_runtime(self, record: RunRecord) -> None:
        try:
            revalidate_run_paths(self._project_root, record.paths)
        except ValueError as error:
            raise RunBlockedError(str(error)) from error
        try:
            current_policy = trusted_engine_policy(self._engine)
        except EngineContractError as error:
            raise RunBlockedError(str(error)) from error
        if current_policy != record.engine_policy or not current_policy.delivery_eligible:
            raise RunBlockedError("configured engine policy changed or is not delivery eligible")
        anchor = resolve_project_path(self._project_root, record.request.anchor.source_path)
        try:
            current_bytes = anchor.read_bytes()
        except OSError as error:
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
        current_hashes = tuple(hashlib.sha256(path.read_bytes()).hexdigest() for path in record.result.frames) if record.result else ()
        if current_hashes != record.generation_output_sha256:
            raise RunBlockedError("generated sprite frames changed after generation")

    @staticmethod
    def _current_export_hashes(record: RunRecord) -> dict[str, str]:
        assert record.export is not None
        hashes = {
            "atlas": hashlib.sha256(record.export.atlas.read_bytes()).hexdigest(),
            "contact_sheet": hashlib.sha256(record.export.contact_sheet.read_bytes()).hexdigest(),
            "preview_gif": hashlib.sha256(record.export.gif.read_bytes()).hexdigest(),
            "lineage": hashlib.sha256(record.lineage.read_bytes()).hexdigest(),
            "manifest": hashlib.sha256(record.export.manifest.read_bytes()).hexdigest(),
            "godot_handoff": hashlib.sha256(record.export.godot_handoff.read_bytes()).hexdigest(),
        }
        for frame in sorted(record.export.frames_dir.glob("*.png")):
            hashes[f"frame:{frame.name}"] = hashlib.sha256(frame.read_bytes()).hexdigest()
        return hashes

    @staticmethod
    def _deliverable(kind: str, path: str, absolute: Path) -> dict[str, str]:
        return {"kind": kind, "project_relative_path": path, "sha256": hashlib.sha256(absolute.read_bytes()).hexdigest()}

    def _validate_engine_result(self, result: EngineResult, expected_count: int, frames_dir: Path, anchor_bytes: bytes) -> None:
        if len(result.frames) != expected_count:
            raise EngineContractError(f"engine returned {len(result.frames)} frames; expected {expected_count}")
        root = frames_dir.resolve()
        seen: set[Path] = set()
        visual_hashes: list[str] = []
        for frame in result.frames:
            resolved = frame.resolve()
            if root not in resolved.parents or resolved.suffix.lower() != ".png" or not resolved.is_file():
                raise EngineContractError("engine frame must be a PNG inside the run frame directory")
            if resolved in seen:
                raise EngineContractError("engine returned the same frame path more than once")
            seen.add(resolved)
            try:
                with Image.open(resolved) as image:
                    rgba = image.convert("RGBA")
                    visual_hashes.append(hashlib.sha256(rgba.tobytes()).hexdigest())
                    if self._engine_policy.delivery_eligible and rgba.getbbox() is None:
                        raise EngineContractError("engine frame must not be fully transparent")
            except (OSError, UnidentifiedImageError) as error:
                raise EngineContractError("engine frame must be a readable PNG") from error
        if self._engine_policy.delivery_eligible:
            with Image.open(BytesIO(anchor_bytes)) as image:
                anchor_visual = hashlib.sha256(image.convert("RGBA").tobytes()).hexdigest()
            if all(value == anchor_visual for value in visual_hashes):
                raise EngineContractError("delivery-eligible sprite frames must visibly differ from the anchor")
