"""Fail-closed lifecycle for character-expression candidate review."""

from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
import re
from uuid import uuid4

from PIL import Image, UnidentifiedImageError
from base_tool_contracts import AnchorEvidenceError, ApprovedAnchorRegistry
from base_tool_contracts import safe_staging_write_bytes

from .catalog import ResolvedExpression, resolve_expression
from .delivery import DeliveryBlockedError, FigmaDeliveryPacket, ProjectFigmaRegistry
from .engine import EngineContractError, EnginePolicy, EngineResult, ExpressionEngine, trusted_engine_policy
from .exporter import ExportResult, export_selected_candidate
from .lineage import write_lineage
from .models import ExpressionRequest
from .paths import RunPaths, create_run_paths, resolve_project_path, revalidate_run_paths, stable_run_tree


class RunNotFoundError(KeyError):
    pass


class RunBlockedError(RuntimeError):
    pass


@dataclass
class RunRecord:
    run_id: str
    request: ExpressionRequest
    resolved: ResolvedExpression
    paths: RunPaths
    lineage: Path
    anchor_bytes: bytes
    engine_policy: EnginePolicy
    anchor_verification: str
    anchor_evidence: dict[str, str]
    status: str
    result: EngineResult | None = None
    generation_output_sha256: tuple[str, ...] = ()
    export_output_sha256: dict[str, str] = field(default_factory=dict)
    selected_candidate: int | None = None
    export: ExportResult | None = None
    warnings: list[str] = field(default_factory=list)

    def public_view(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "status": self.status,
            "candidate_count": len(self.result.candidates) if self.result else 0,
            "selected_candidate": self.selected_candidate,
            "warnings": self.warnings,
            "lineage": {
                "file": self.lineage.name,
                "figma_node_url": str(self.request.anchor.figma_node_url),
                "anchor_sha256": hashlib.sha256(self.anchor_bytes).hexdigest(),
            },
            "anchor_verification": self.anchor_verification,
            "resolved_expression": {
                "controls": [control.model_dump(mode="json") for control in self.resolved.controls],
                "movement_phrases": list(self.resolved.movement_phrases),
                "gaze_phrase": self.resolved.gaze_phrase,
                "head_pose_phrase": self.resolved.head_pose_phrase,
                "preset": self.resolved.preset,
            },
            "generation_instruction": self.result.generation_instruction if self.result else None,
            "engine": {
                "provenance": self.engine_policy.provenance,
                "delivery_eligible": self.engine_policy.delivery_eligible and self.anchor_verification == "ANCHOR_EVIDENCE_VERIFIED",
                "adapter_id": self.engine_policy.adapter_id,
                "config_sha256": self.engine_policy.config_sha256,
            },
        }


class ExpressionStudioService:
    def __init__(
        self,
        project_root: Path,
        engine: ExpressionEngine,
        registry: ProjectFigmaRegistry | None = None,
        project_id: str | None = None,
        anchor_registry: ApprovedAnchorRegistry | None = None,
    ) -> None:
        if project_id is None or re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", project_id) is None:
            raise ValueError("a canonical project_id is required for every Expression Studio instance")
        self._project_root = project_root.resolve()
        self._engine = engine
        self._engine_policy = trusted_engine_policy(engine)
        self._registry = registry
        self._project_id = project_id
        self._anchor_registry = anchor_registry
        if self._anchor_registry is not None:
            self._anchor_registry.assert_project_owned(self._project_root)
        self._runs: dict[str, RunRecord] = {}

    def create_run(self, request: ExpressionRequest) -> RunRecord:
        if self._project_id is not None and request.project_id != self._project_id:
            raise ValueError(f"request project_id must match configured project_id {self._project_id!r}")
        if self._registry is not None:
            try:
                self._registry.validate_anchor_url(request.project_id, str(request.anchor.figma_node_url))
            except DeliveryBlockedError as error:
                raise ValueError(str(error)) from error
        anchor = resolve_project_path(self._project_root, request.anchor.source_path)
        if not anchor.is_file():
            raise ValueError("approved anchor source_path must point to an existing project image")
        resolved = resolve_expression(request)
        run_id = uuid4().hex
        paths = create_run_paths(self._project_root, request.asset_id, run_id)
        revalidate_run_paths(self._project_root, paths)
        anchor_bytes = anchor.read_bytes()
        anchor_verification = "ANCHOR_ROUTE_SYNTAX_VALID" if self._registry is not None else "ANCHOR_UNVERIFIED"
        anchor_evidence: dict[str, str] = {}
        if self._anchor_registry is not None:
            try:
                anchor_evidence = self._anchor_registry.evidence(
                    project_id=request.project_id,
                    source_path=request.anchor.source_path,
                    figma_node_url=str(request.anchor.figma_node_url),
                    source_bytes=anchor_bytes,
                )
                anchor_verification = anchor_evidence["verification_state"]
            except AnchorEvidenceError as error:
                raise ValueError(str(error)) from error
        try:
            with stable_run_tree(self._project_root, paths) as stable:
                stable_run = stable.run_dir
                stable_candidates = stable.open_directory("candidates", expected_identity=paths.candidates_identity)
                engine_anchor = safe_staging_write_bytes(stable_run, f"approved-anchor{anchor.suffix.lower() or '.png'}", anchor_bytes)
                engine_request = request.model_copy(update={"anchor": request.anchor.model_copy(update={"source_path": str(engine_anchor)})})
                lineage = write_lineage(request, resolved, anchor_bytes, stable_run, anchor_verification=anchor_verification, anchor_evidence=anchor_evidence).resolve()
                record = RunRecord(run_id=run_id, request=request, resolved=resolved, paths=paths, lineage=lineage, anchor_bytes=anchor_bytes, engine_policy=self._engine_policy, anchor_verification=anchor_verification, anchor_evidence=anchor_evidence, status="blocked")
                self._runs[run_id] = record
                result = self._engine.generate(engine_request, resolved, stable_candidates)
                record.result = EngineResult(
                    candidates=[path.resolve() for path in result.candidates],
                    generation_instruction=result.generation_instruction,
                    provenance=getattr(result, "provenance", "unverified"),
                    delivery_eligible=bool(getattr(result, "delivery_eligible", False)),
                )
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
            record.result = None
            return record
        if (
            getattr(record.result, "provenance", "unverified") != self._engine_policy.provenance
            or bool(getattr(record.result, "delivery_eligible", False)) != self._engine_policy.delivery_eligible
        ):
            record.warnings.append("engine result provenance or delivery eligibility does not match the configured adapter policy")
            record.result = None
            return record
        try:
            anchor_unchanged = anchor.read_bytes() == anchor_bytes
        except OSError:
            anchor_unchanged = False
        if not anchor_unchanged:
            record.warnings.append("approved anchor changed during generation; the run was blocked without overwriting the source")
            record.result = None
            return record
        try:
            self._validate_engine_result(
                record.result,
                request.candidate_count,
                paths.candidates_dir,
                anchor_bytes,
                delivery_eligible=self._engine_policy.delivery_eligible,
            )
        except EngineContractError as error:
            record.warnings.append(str(error))
            record.result = None
            return record
        record.generation_output_sha256 = tuple(hashlib.sha256(path.read_bytes()).hexdigest() for path in record.result.candidates)
        with stable_run_tree(self._project_root, paths) as stable:
            record.lineage = write_lineage(request, resolved, anchor_bytes, stable.run_dir, generation_instruction=record.result.generation_instruction, engine=self._engine_evidence(record.generation_output_sha256), anchor_verification=record.anchor_verification, anchor_evidence=record.anchor_evidence).resolve()
        record.status = "generated"
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

    def candidate(self, run_id: str, candidate_index: int) -> Path:
        record = self.get_run(run_id)
        if record.result is None or candidate_index < 0 or candidate_index >= len(record.result.candidates):
            raise RunBlockedError("candidate is outside generated candidates")
        candidate = record.result.candidates[candidate_index]
        resolved = candidate.resolve()
        if record.paths.candidates_dir.resolve() not in resolved.parents or not resolved.is_file():
            raise RunBlockedError("candidate image is unavailable")
        return resolved

    def approved_anchor(self, run_id: str) -> Path:
        record = self.get_run(run_id)
        anchor = resolve_project_path(self._project_root, record.request.anchor.source_path)
        if not anchor.is_file():
            raise RunBlockedError("approved anchor image is unavailable")
        return anchor

    def export(self, run_id: str, selected_candidate: int) -> RunRecord:
        record = self.get_run(run_id)
        if record.status != "generated" or record.result is None:
            raise RunBlockedError("a generated run with a selected candidate is required before export")
        if not record.engine_policy.delivery_eligible:
            raise RunBlockedError(
                f"{record.engine_policy.provenance} engine output is not eligible for export or Figma delivery"
            )
        self._revalidate_runtime(record)
        if record.anchor_verification != "ANCHOR_EVIDENCE_VERIFIED":
            raise RunBlockedError("project-owned approved-anchor evidence is required before export or Figma delivery")
        try:
            self._validate_engine_result(record.result, record.request.candidate_count, record.paths.candidates_dir, record.anchor_bytes, delivery_eligible=True)
        except EngineContractError as error:
            raise RunBlockedError(str(error)) from error
        self.candidate(run_id, selected_candidate)
        with stable_run_tree(self._project_root, record.paths) as stable:
            stable_candidates_dir = stable.open_directory("candidates", expected_identity=record.paths.candidates_identity)
            stable_exports = stable.open_directory("exports", expected_identity=record.paths.exports_identity)
            stable_candidates = [stable_candidates_dir / path.name for path in record.result.candidates]
            exported = export_selected_candidate(stable_exports, stable_candidates, selected_candidate, record.result.generation_instruction, candidate_sha256=record.generation_output_sha256, engine=self._engine_evidence(record.generation_output_sha256), anchor_sha256=hashlib.sha256(record.anchor_bytes).hexdigest(), anchor_verification=record.anchor_verification, anchor_evidence=record.anchor_evidence)
            record.export = ExportResult(exported.selected.resolve(), exported.contact_sheet.resolve(), exported.manifest.resolve())
            record.selected_candidate = selected_candidate
            record.lineage = write_lineage(record.request, record.resolved, record.anchor_bytes, stable.run_dir, generation_instruction=record.result.generation_instruction, selected_candidate=selected_candidate, engine=self._engine_evidence(record.generation_output_sha256), anchor_verification=record.anchor_verification, anchor_evidence=record.anchor_evidence).resolve()
        try:
            revalidate_run_paths(self._project_root, record.paths)
        except ValueError as error:
            raise RunBlockedError(str(error)) from error
        record.export_output_sha256 = self._current_export_hashes(record)
        record.status = "exported"
        return record

    def prepare_figma_delivery(self, run_id: str) -> FigmaDeliveryPacket:
        record = self.get_run(run_id)
        if record.status != "exported" or record.export is None or record.selected_candidate is None:
            raise RunBlockedError("an exported run with a selected candidate is required before Figma delivery")
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
        return FigmaDeliveryPacket(
            run_id=record.run_id,
            project_id=record.request.project_id,
            anchor_figma_node_url=str(record.request.anchor.figma_node_url),
            target=target,
            engine=self._engine_evidence(record.generation_output_sha256),
            anchor_verification=record.anchor_verification,
            anchor_evidence=record.anchor_evidence,
            visual_deliverables=[
                self._deliverable("selected_expression", self._project_relative(record.export.selected), record.export.selected),
                self._deliverable("contact_sheet", self._project_relative(record.export.contact_sheet), record.export.contact_sheet),
                self._deliverable("lineage", self._project_relative(record.lineage), record.lineage),
                self._deliverable("manifest", self._project_relative(record.export.manifest), record.export.manifest),
            ],
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
            selected_hash = hashlib.sha256(record.export.selected.read_bytes()).hexdigest()
            contact_sheet_hash = hashlib.sha256(record.export.contact_sheet.read_bytes()).hexdigest()
        except (OSError, json.JSONDecodeError) as error:
            raise RunBlockedError("export provenance manifest is unavailable or invalid") from error
        if manifest.get("anchor_verification") != "ANCHOR_EVIDENCE_VERIFIED":
            raise RunBlockedError("export manifest has no verified anchor evidence")
        engine = manifest.get("engine", {})
        if engine.get("config_sha256") != self._engine_policy.config_sha256 or not engine.get("delivery_eligible"):
            raise RunBlockedError("export manifest engine provenance does not match the configured adapter")
        if manifest.get("selected_sha256") != selected_hash:
            raise RunBlockedError("export selected image hash does not match its manifest")
        if manifest.get("contact_sheet_sha256") != contact_sheet_hash:
            raise RunBlockedError("export contact sheet hash does not match its manifest")
        if manifest.get("anchor_evidence") != record.anchor_evidence:
            raise RunBlockedError("export manifest anchor evidence does not match the verified run")
        if self._current_export_hashes(record) != record.export_output_sha256:
            raise RunBlockedError("an exported expression deliverable changed after export")

    def _engine_evidence(self, output_sha256: tuple[str, ...] = ()) -> dict[str, object]:
        evidence: dict[str, object] = {
            "adapter_id": self._engine_policy.adapter_id,
            "provenance": self._engine_policy.provenance,
            "delivery_eligible": self._engine_policy.delivery_eligible,
            "config_sha256": self._engine_policy.config_sha256,
            "validation_state": "SERVICE_POLICY_VERIFIED",
        }
        if output_sha256:
            evidence["output_sha256"] = list(output_sha256)
        return evidence

    def _revalidate_runtime(self, record: RunRecord) -> None:
        try:
            revalidate_run_paths(self._project_root, record.paths)
        except ValueError as error:
            raise RunBlockedError(str(error)) from error
        current_policy = trusted_engine_policy(self._engine)
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
            evidence = self._anchor_registry.evidence(
                project_id=record.request.project_id,
                source_path=record.request.anchor.source_path,
                figma_node_url=str(record.request.anchor.figma_node_url),
                source_bytes=current_bytes,
            )
        except AnchorEvidenceError as error:
            raise RunBlockedError(str(error)) from error
        if evidence != record.anchor_evidence:
            raise RunBlockedError("approved-anchor evidence changed after generation")
        current_hashes = tuple(hashlib.sha256(path.read_bytes()).hexdigest() for path in record.result.candidates) if record.result else ()
        if current_hashes != record.generation_output_sha256:
            raise RunBlockedError("generated expression candidates changed after generation")

    @staticmethod
    def _current_export_hashes(record: RunRecord) -> dict[str, str]:
        assert record.export is not None
        return {
            "selected": hashlib.sha256(record.export.selected.read_bytes()).hexdigest(),
            "contact_sheet": hashlib.sha256(record.export.contact_sheet.read_bytes()).hexdigest(),
            "lineage": hashlib.sha256(record.lineage.read_bytes()).hexdigest(),
            "manifest": hashlib.sha256(record.export.manifest.read_bytes()).hexdigest(),
        }

    @staticmethod
    def _deliverable(kind: str, path: str, absolute: Path) -> dict[str, str]:
        return {"kind": kind, "project_relative_path": path, "sha256": hashlib.sha256(absolute.read_bytes()).hexdigest()}

    @staticmethod
    def _validate_engine_result(result: EngineResult, expected_count: int, candidates_dir: Path, anchor_bytes: bytes, *, delivery_eligible: bool) -> None:
        if len(result.candidates) != expected_count:
            raise EngineContractError(f"engine returned {len(result.candidates)} candidates; expected {expected_count}")
        root = candidates_dir.resolve()
        resolved_candidates: list[Path] = []
        for candidate in result.candidates:
            resolved = candidate.resolve()
            if root not in resolved.parents or resolved.suffix.lower() != ".png":
                raise EngineContractError("engine candidate must be a PNG inside the run candidate directory")
            if not resolved.is_file():
                raise EngineContractError("engine candidate image is unavailable")
            try:
                with Image.open(resolved) as image:
                    rgba = image.convert("RGBA")
                    if rgba.getbbox() is None:
                        raise EngineContractError("engine candidate must not be fully transparent")
            except (OSError, UnidentifiedImageError) as error:
                raise EngineContractError("engine candidate must be a readable PNG image") from error
            resolved_candidates.append(resolved)
        if len(resolved_candidates) != len(set(resolved_candidates)):
            raise EngineContractError("engine returned the same candidate path more than once")
        if delivery_eligible:
            try:
                from io import BytesIO
                with Image.open(BytesIO(anchor_bytes)) as anchor_image:
                    anchor_visual = hashlib.sha256(anchor_image.convert("RGBA").tobytes()).hexdigest()
                candidate_visuals = []
                for candidate in resolved_candidates:
                    with Image.open(candidate) as image:
                        candidate_visuals.append(hashlib.sha256(image.convert("RGBA").tobytes()).hexdigest())
            except (OSError, UnidentifiedImageError) as error:
                raise EngineContractError("engine output visual hashes could not be verified") from error
            if all(value == anchor_visual for value in candidate_visuals):
                raise EngineContractError("delivery-eligible expression candidates must visibly differ from the anchor")
