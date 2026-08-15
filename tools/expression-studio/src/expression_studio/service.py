"""Fail-closed lifecycle for character-expression candidate review."""

from dataclasses import dataclass, field
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import re
from uuid import uuid4

from PIL import Image, UnidentifiedImageError
from base_tool_contracts import (
    AnchorEvidenceError,
    ApprovedAnchorRegistry,
    SubscriptionHandoffPacket,
    build_subscription_handoff_packet,
    confined_staging_read_bytes,
    render_chatgpt_pro_prompt,
    safe_staging_write_bytes,
)
from base_tool_contracts.trusted_files import (
    TrustedFileError,
    read_regular_nofollow,
    read_regular_portable_nofollow,
)

from .catalog import ResolvedExpression, resolve_expression
from .delivery import DeliveryBlockedError, FigmaDeliveryPacket, ProjectFigmaRegistry
from .engine import EngineContractError, EnginePolicy, EngineResult, ExpressionEngine, generation_instruction, trusted_engine_policy
from .exporter import ExportResult, export_selected_candidate
from .imports import DeclaredSource, ImportedImage, discard_import_bytes, import_metadata, revalidate_imported_image
from .lineage import write_lineage
from .models import ExpressionRequest
from .paths import RunPaths, create_run_paths, resolve_project_path, revalidate_run_paths, stable_run_tree


class RunNotFoundError(KeyError):
    pass


class RunBlockedError(RuntimeError):
    pass


_MAX_ANCHOR_BYTES = 25 * 1024 * 1024
_MAX_ANCHOR_DIMENSION = 4096
_ALLOWED_ANCHOR_FORMATS = {"PNG", "JPEG", "WEBP"}
_HANDOFF_REVIEW_CHECKLIST = (
    "same approved character identity",
    "requested edit is visible and limited to the requested scope",
    "no unrequested composition, style, or character change",
    "compare all candidates before confirming one result",
)


def _import_engine_policy() -> EnginePolicy:
    config = b"expression.import.v1|subscription_handoff_import|INCLUDED_OR_LOCAL_HANDOFF|provider_call_made=false"
    return EnginePolicy(
        adapter_id="expression.import.v1",
        provenance="subscription_handoff_import",
        delivery_eligible=True,
        config_sha256=hashlib.sha256(config).hexdigest(),
    )


def _read_project_image(
    project_root: Path,
    source_path: str,
    *,
    expected_sha256: str | None = None,
) -> bytes:
    """Read one bounded project image without following path links."""
    relative = Path(source_path)
    if relative.is_absolute() or not relative.parts or any(part in {"", ".", ".."} for part in relative.parts):
        raise ValueError("approved anchor source_path must be a confined project image")
    reader = (
        read_regular_nofollow
        if getattr(os, "O_NOFOLLOW", 0) and os.name != "nt"
        else read_regular_portable_nofollow
    )
    try:
        data, _ = reader(project_root / relative, max_bytes=_MAX_ANCHOR_BYTES)
    except TrustedFileError as error:
        raise ValueError("approved anchor source must be a readable regular file without links") from error
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


@dataclass(frozen=True)
class PendingHandoff:
    run_id: str
    request: ExpressionRequest
    resolved: ResolvedExpression
    anchor_sha256: str
    anchor_evidence: dict[str, str]
    packet: SubscriptionHandoffPacket
    prompt: str


class ExpressionStudioService:
    def __init__(
        self,
        project_root: Path,
        engine: ExpressionEngine,
        registry: ProjectFigmaRegistry | None = None,
        project_id: str | None = None,
        anchor_registry: ApprovedAnchorRegistry | None = None,
        run_mode: str = "subscription_handoff_import",
    ) -> None:
        if project_id is None or re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", project_id) is None:
            raise ValueError("a canonical project_id is required for every Expression Studio instance")
        self._project_root = project_root.resolve()
        self._engine = engine
        self._engine_policy = trusted_engine_policy(engine)
        self._registry = registry
        self._project_id = project_id
        self._anchor_registry = anchor_registry
        if run_mode not in {"subscription_handoff_import", "simulated", "openai"}:
            raise ValueError("unsupported Expression Studio run mode")
        expected_provenance = {"simulated": "simulated", "openai": "openai"}.get(run_mode)
        if (
            expected_provenance is not None
            and self._engine_policy.provenance in {"simulated", "openai"}
            and self._engine_policy.provenance != expected_provenance
        ):
            raise ValueError("Expression Studio run mode does not match the configured engine")
        self._run_mode = run_mode
        if self._anchor_registry is not None:
            self._anchor_registry.assert_project_owned(self._project_root)
        self._runs: dict[str, RunRecord] = {}
        self._pending_handoffs: dict[str, PendingHandoff] = {}

    def prepare_subscription_handoff(self, request: ExpressionRequest) -> PendingHandoff:
        if self._run_mode != "subscription_handoff_import":
            raise RunBlockedError("MODE_NOT_AVAILABLE")
        if request.project_id != self._project_id:
            raise ValueError(f"request project_id must match configured project_id {self._project_id!r}")
        if self._registry is None or self._anchor_registry is None:
            raise ValueError("ChatGPT Pro handoff requires configured Figma routing and project-owned approved-anchor evidence")
        try:
            self._registry.validate_anchor_url(request.project_id, str(request.anchor.figma_node_url))
            self._registry.assert_unchanged()
            self._anchor_registry.assert_unchanged()
            expected_anchor_sha256 = self._anchor_registry.expected_source_sha256(
                project_id=request.project_id,
                source_path=request.anchor.source_path,
                figma_node_url=str(request.anchor.figma_node_url),
            )
        except (DeliveryBlockedError, AnchorEvidenceError) as error:
            raise ValueError(str(error)) from error
        anchor_bytes = _read_project_image(
            self._project_root,
            request.anchor.source_path,
            expected_sha256=expected_anchor_sha256,
        )
        try:
            anchor_evidence = self._anchor_registry.evidence(
                project_id=request.project_id,
                source_path=request.anchor.source_path,
                figma_node_url=str(request.anchor.figma_node_url),
                source_bytes=anchor_bytes,
            )
        except AnchorEvidenceError as error:
            raise ValueError(str(error)) from error
        resolved = resolve_expression(request)
        run_id = uuid4().hex
        while run_id in self._runs or run_id in self._pending_handoffs:
            run_id = uuid4().hex
        instruction = generation_instruction(request, resolved)
        packet = build_subscription_handoff_packet(
            project_id=request.project_id,
            tool_id="expression-studio",
            run_id=run_id,
            workflow="character_edit",
            source_filename=Path(request.anchor.source_path).name,
            source_sha256=hashlib.sha256(anchor_bytes).hexdigest(),
            instruction=instruction,
            expected_png_count=request.candidate_count,
            min_dimension=16,
            max_dimension=4096,
            review_checklist=_HANDOFF_REVIEW_CHECKLIST,
        )
        pending = PendingHandoff(
            run_id=run_id,
            request=request,
            resolved=resolved,
            anchor_sha256=hashlib.sha256(anchor_bytes).hexdigest(),
            anchor_evidence=dict(anchor_evidence),
            packet=packet,
            prompt=render_chatgpt_pro_prompt(packet),
        )
        self._pending_handoffs[run_id] = pending
        return pending

    def get_pending_handoff(self, run_id: str) -> PendingHandoff:
        try:
            return self._pending_handoffs[run_id]
        except KeyError as error:
            raise RunNotFoundError(run_id) from error

    def import_subscription_handoff(
        self,
        run_id: str,
        candidates: tuple[ImportedImage, ...],
    ) -> RunRecord:
        pending = self.get_pending_handoff(run_id)
        if self._registry is None or self._anchor_registry is None:
            raise ValueError("ChatGPT Pro handoff evidence is unavailable during import")
        try:
            self._registry.assert_unchanged()
            self._registry.validate_anchor_url(
                pending.request.project_id,
                str(pending.request.anchor.figma_node_url),
            )
            self._anchor_registry.assert_unchanged()
            expected_anchor_sha256 = self._anchor_registry.expected_source_sha256(
                project_id=pending.request.project_id,
                source_path=pending.request.anchor.source_path,
                figma_node_url=str(pending.request.anchor.figma_node_url),
            )
        except (DeliveryBlockedError, AnchorEvidenceError) as error:
            raise ValueError(str(error)) from error
        anchor_bytes = _read_project_image(
            self._project_root,
            pending.request.anchor.source_path,
            expected_sha256=expected_anchor_sha256,
        )
        if hashlib.sha256(anchor_bytes).hexdigest() != pending.anchor_sha256:
            raise ValueError("approved anchor changed after ChatGPT Pro handoff preparation")
        try:
            evidence = self._anchor_registry.evidence(
                project_id=pending.request.project_id,
                source_path=pending.request.anchor.source_path,
                figma_node_url=str(pending.request.anchor.figma_node_url),
                source_bytes=anchor_bytes,
            )
        except AnchorEvidenceError as error:
            raise ValueError(str(error)) from error
        if evidence != pending.anchor_evidence:
            raise ValueError("approved-anchor evidence changed after ChatGPT Pro handoff preparation")
        record = self.create_import_run(
            pending.request,
            candidates,
            "CHATGPT_INCLUDED",
            reserved_run_id=run_id,
        )
        del self._pending_handoffs[run_id]
        return record

    def create_run(self, request: ExpressionRequest) -> RunRecord:
        if self._run_mode == "subscription_handoff_import":
            raise RunBlockedError("MODE_NOT_AVAILABLE")
        if self._project_id is not None and request.project_id != self._project_id:
            raise ValueError(f"request project_id must match configured project_id {self._project_id!r}")
        if self._registry is not None:
            try:
                self._registry.validate_anchor_url(request.project_id, str(request.anchor.figma_node_url))
            except DeliveryBlockedError as error:
                raise ValueError(str(error)) from error
        anchor = resolve_project_path(self._project_root, request.anchor.source_path)
        if self._engine_policy.delivery_eligible and self._anchor_registry is None:
            raise ValueError("OpenAI generation requires project-owned approved-anchor evidence")
        expected_anchor_sha256: str | None = None
        if self._anchor_registry is not None:
            try:
                expected_anchor_sha256 = self._anchor_registry.expected_source_sha256(
                    project_id=request.project_id,
                    source_path=request.anchor.source_path,
                    figma_node_url=str(request.anchor.figma_node_url),
                )
            except AnchorEvidenceError as error:
                raise ValueError(str(error)) from error
        anchor_bytes = _read_project_image(
            self._project_root,
            request.anchor.source_path,
            expected_sha256=expected_anchor_sha256,
        )
        resolved = resolve_expression(request)
        run_id = uuid4().hex
        paths = create_run_paths(self._project_root, request.asset_id, run_id)
        revalidate_run_paths(self._project_root, paths)
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
                anchor_sha256 = hashlib.sha256(anchor_bytes).hexdigest()
                engine_anchor = safe_staging_write_bytes(
                    stable_run,
                    f"approved-anchor-{anchor_sha256}{anchor.suffix.lower() or '.png'}",
                    anchor_bytes,
                )
                engine_request = request.model_copy(update={"anchor": request.anchor.model_copy(update={"source_path": str(engine_anchor)})})
                lineage = write_lineage(request, resolved, anchor_bytes, stable_run, anchor_verification=anchor_verification, anchor_evidence=anchor_evidence).resolve()
                record = RunRecord(run_id=run_id, request=request, resolved=resolved, paths=paths, lineage=lineage, anchor_bytes=anchor_bytes, engine_policy=self._engine_policy, anchor_verification=anchor_verification, anchor_evidence=anchor_evidence, status="blocked", run_mode=self._run_mode)
                self._runs[run_id] = record
                result = self._engine.generate(engine_request, resolved, stable_candidates)
                record.provider_call_made = bool(getattr(result, "provider_call_made", False))
                record.result = EngineResult(
                    candidates=[path.resolve() for path in result.candidates],
                    generation_instruction=result.generation_instruction,
                    provenance=getattr(result, "provenance", "unverified"),
                    delivery_eligible=bool(getattr(result, "delivery_eligible", False)),
                    provider_call_made=record.provider_call_made,
                )
        except (EngineContractError, ValueError) as error:
            record = self._runs.get(run_id)
            if record is None:
                raise ValueError(str(error)) from error
            record.provider_call_made = bool(getattr(error, "provider_call_made", False))
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
            anchor_unchanged = _read_project_image(
                self._project_root,
                request.anchor.source_path,
                expected_sha256=hashlib.sha256(anchor_bytes).hexdigest(),
            ) == anchor_bytes
        except ValueError:
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
                project_root=self._project_root,
            )
        except EngineContractError as error:
            record.warnings.append(str(error))
            record.result = None
            return record
        record.generation_output_sha256 = tuple(hashlib.sha256(_read_staged_file(self._project_root, path)).hexdigest() for path in record.result.candidates)
        with stable_run_tree(self._project_root, paths) as stable:
            record.lineage = write_lineage(request, resolved, anchor_bytes, stable.run_dir, generation_instruction=record.result.generation_instruction, engine=self._engine_evidence(record.generation_output_sha256), anchor_verification=record.anchor_verification, anchor_evidence=record.anchor_evidence).resolve()
        record.status = "generated"
        return record

    def create_import_run(
        self,
        request: ExpressionRequest,
        candidates: tuple[ImportedImage, ...],
        declared_source: DeclaredSource,
        *,
        reserved_run_id: str | None = None,
    ) -> RunRecord:
        if self._run_mode != "subscription_handoff_import":
            raise RunBlockedError("MODE_NOT_AVAILABLE")
        if request.project_id != self._project_id:
            raise ValueError(f"request project_id must match configured project_id {self._project_id!r}")
        if len(candidates) != request.candidate_count:
            raise ValueError(f"import returned {len(candidates)} candidates; expected {request.candidate_count}")
        if any(image.declared_source != declared_source or image.order != index for index, image in enumerate(candidates)):
            raise ValueError("import candidate metadata does not match declared source or upload order")
        candidates = tuple(revalidate_imported_image(image) for image in candidates)
        if self._registry is not None:
            try:
                self._registry.validate_anchor_url(request.project_id, str(request.anchor.figma_node_url))
            except DeliveryBlockedError as error:
                raise ValueError(str(error)) from error
        anchor = resolve_project_path(self._project_root, request.anchor.source_path)
        expected_anchor_sha256: str | None = None
        if self._anchor_registry is not None:
            try:
                expected_anchor_sha256 = self._anchor_registry.expected_source_sha256(
                    project_id=request.project_id,
                    source_path=request.anchor.source_path,
                    figma_node_url=str(request.anchor.figma_node_url),
                )
            except AnchorEvidenceError as error:
                raise ValueError(str(error)) from error
        anchor_bytes = _read_project_image(self._project_root, request.anchor.source_path, expected_sha256=expected_anchor_sha256)
        with Image.open(BytesIO(anchor_bytes)) as anchor_image:
            anchor_visual = hashlib.sha256(anchor_image.convert("RGBA").tobytes()).hexdigest()
        visual_hashes: list[str] = []
        for candidate in candidates:
            with Image.open(BytesIO(candidate.data)) as opened:
                rgba = opened.convert("RGBA")
                if rgba.getchannel("A").getbbox() is None:
                    raise ValueError("import candidate must not be fully transparent")
                visual_hashes.append(hashlib.sha256(rgba.tobytes()).hexdigest())
        if len(visual_hashes) != len(set(visual_hashes)):
            raise ValueError("import expression candidates must not be pixel-duplicates")
        if any(value == anchor_visual for value in visual_hashes):
            raise ValueError("import expression candidate must visibly differ from the anchor")
        resolved = resolve_expression(request)
        run_id = reserved_run_id or uuid4().hex
        if run_id in self._runs:
            raise RunBlockedError("run identity is already in use")
        paths = create_run_paths(self._project_root, request.asset_id, run_id)
        revalidate_run_paths(self._project_root, paths)
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
        policy = _import_engine_policy()
        instruction = generation_instruction(resolved)
        with stable_run_tree(self._project_root, paths) as stable:
            stable_candidates = stable.open_directory("candidates", expected_identity=paths.candidates_identity)
            anchor_sha256 = hashlib.sha256(anchor_bytes).hexdigest()
            safe_staging_write_bytes(stable.run_dir, f"approved-anchor-{anchor_sha256}{anchor.suffix.lower() or '.png'}", anchor_bytes)
            candidate_paths: list[Path] = []
            for image in candidates:
                with Image.open(BytesIO(image.data)) as opened:
                    encoded = BytesIO()
                    opened.convert("RGBA").save(encoded, format="PNG")
                candidate_paths.append(safe_staging_write_bytes(stable_candidates, f"candidate-{image.order:03d}.png", encoded.getvalue()).resolve())
            result = EngineResult(candidate_paths, instruction, provenance=policy.provenance, delivery_eligible=True)
            output_sha256 = tuple(hashlib.sha256(_read_staged_file(self._project_root, path)).hexdigest() for path in candidate_paths)
            lineage = write_lineage(
                request,
                resolved,
                anchor_bytes,
                stable.run_dir,
                generation_instruction=instruction,
                engine=self._engine_evidence(output_sha256, policy=policy),
                anchor_verification=anchor_verification,
                anchor_evidence=anchor_evidence,
                imported_images=[import_metadata(image) for image in candidates],
                run_mode=self._run_mode,
            ).resolve()
        record = RunRecord(
            run_id=run_id,
            request=request,
            resolved=resolved,
            paths=paths,
            lineage=lineage,
            anchor_bytes=anchor_bytes,
            engine_policy=policy,
            anchor_verification=anchor_verification,
            anchor_evidence=anchor_evidence,
            status="generated",
            result=result,
            generation_output_sha256=output_sha256,
            run_mode=self._run_mode,
            imported_images=tuple(discard_import_bytes(image) for image in candidates),
        )
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

    def candidate(self, run_id: str, candidate_index: int) -> bytes:
        record = self.get_run(run_id)
        if record.result is None or candidate_index < 0 or candidate_index >= len(record.result.candidates):
            raise RunBlockedError("candidate is outside generated candidates")
        candidate = record.result.candidates[candidate_index]
        resolved = candidate.resolve()
        if record.paths.candidates_dir.resolve() not in resolved.parents or not resolved.is_file():
            raise RunBlockedError("candidate image is unavailable")
        try:
            return _read_staged_file(self._project_root, resolved, expected_sha256=record.generation_output_sha256[candidate_index])
        except ValueError as error:
            raise RunBlockedError("candidate image is unavailable or changed") from error

    def approved_anchor(self, run_id: str) -> bytes:
        record = self.get_run(run_id)
        return record.anchor_bytes

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
            self._validate_engine_result(record.result, record.request.candidate_count, record.paths.candidates_dir, record.anchor_bytes, delivery_eligible=True, project_root=self._project_root)
        except EngineContractError as error:
            raise RunBlockedError(str(error)) from error
        self.candidate(run_id, selected_candidate)
        with stable_run_tree(self._project_root, record.paths) as stable:
            stable_candidates_dir = stable.open_directory("candidates", expected_identity=record.paths.candidates_identity)
            stable_exports = stable.open_directory("exports", expected_identity=record.paths.exports_identity)
            stable_candidates = [stable_candidates_dir / path.name for path in record.result.candidates]
            exported = export_selected_candidate(stable_exports, stable_candidates, selected_candidate, record.result.generation_instruction, candidate_sha256=record.generation_output_sha256, engine=self._engine_evidence(record.generation_output_sha256, policy=record.engine_policy), anchor_sha256=hashlib.sha256(record.anchor_bytes).hexdigest(), anchor_verification=record.anchor_verification, anchor_evidence=record.anchor_evidence, imported_images=[import_metadata(image) for image in record.imported_images], run_mode=record.run_mode)
            record.export = ExportResult(exported.selected.resolve(), exported.contact_sheet.resolve(), exported.manifest.resolve())
            record.selected_candidate = selected_candidate
            record.lineage = write_lineage(record.request, record.resolved, record.anchor_bytes, stable.run_dir, generation_instruction=record.result.generation_instruction, selected_candidate=selected_candidate, engine=self._engine_evidence(record.generation_output_sha256, policy=record.engine_policy), anchor_verification=record.anchor_verification, anchor_evidence=record.anchor_evidence, imported_images=[import_metadata(image) for image in record.imported_images], run_mode=record.run_mode).resolve()
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
            engine=self._engine_evidence(record.generation_output_sha256, policy=record.engine_policy),
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
            manifest = json.loads(_read_staged_file(self._project_root, record.export.manifest).decode("utf-8"))
            selected_hash = hashlib.sha256(_read_staged_file(self._project_root, record.export.selected)).hexdigest()
            contact_sheet_hash = hashlib.sha256(_read_staged_file(self._project_root, record.export.contact_sheet)).hexdigest()
        except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
            raise RunBlockedError("export provenance manifest is unavailable or invalid") from error
        if manifest.get("anchor_verification") != "ANCHOR_EVIDENCE_VERIFIED":
            raise RunBlockedError("export manifest has no verified anchor evidence")
        engine = manifest.get("engine", {})
        if engine.get("config_sha256") != record.engine_policy.config_sha256 or not engine.get("delivery_eligible"):
            raise RunBlockedError("export manifest engine provenance does not match the configured adapter")
        if manifest.get("selected_sha256") != selected_hash:
            raise RunBlockedError("export selected image hash does not match its manifest")
        if manifest.get("contact_sheet_sha256") != contact_sheet_hash:
            raise RunBlockedError("export contact sheet hash does not match its manifest")
        if manifest.get("anchor_evidence") != record.anchor_evidence:
            raise RunBlockedError("export manifest anchor evidence does not match the verified run")
        if self._current_export_hashes(record) != record.export_output_sha256:
            raise RunBlockedError("an exported expression deliverable changed after export")

    def _engine_evidence(self, output_sha256: tuple[str, ...] = (), *, policy: EnginePolicy | None = None) -> dict[str, object]:
        selected_policy = policy or self._engine_policy
        evidence: dict[str, object] = {
            "adapter_id": selected_policy.adapter_id,
            "provenance": selected_policy.provenance,
            "delivery_eligible": selected_policy.delivery_eligible,
            "config_sha256": selected_policy.config_sha256,
            "validation_state": "SERVICE_POLICY_VERIFIED",
            "cost_route": "INCLUDED_OR_LOCAL_HANDOFF" if selected_policy.provenance == "subscription_handoff_import" else "EXPLICIT_ENGINE_ROUTE",
            "provider_call_made": selected_policy.provenance == "openai",
        }
        if output_sha256:
            evidence["output_sha256"] = list(output_sha256)
        return evidence

    def _revalidate_runtime(self, record: RunRecord) -> None:
        try:
            revalidate_run_paths(self._project_root, record.paths)
        except ValueError as error:
            raise RunBlockedError(str(error)) from error
        if record.run_mode == "subscription_handoff_import":
            if record.engine_policy != _import_engine_policy():
                raise RunBlockedError("import policy changed after generation")
        else:
            current_policy = trusted_engine_policy(self._engine)
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
        try:
            current_hashes = tuple(
                hashlib.sha256(_read_staged_file(self._project_root, path, expected_sha256=expected)).hexdigest()
                for path, expected in zip(record.result.candidates, record.generation_output_sha256, strict=True)
            ) if record.result else ()
        except (ValueError, OSError) as error:
            raise RunBlockedError("generated expression candidates are unavailable or changed") from error
        if current_hashes != record.generation_output_sha256:
            raise RunBlockedError("generated expression candidates changed after generation")

    def _current_export_hashes(self, record: RunRecord) -> dict[str, str]:
        assert record.export is not None
        return {
            "selected": hashlib.sha256(_read_staged_file(self._project_root, record.export.selected)).hexdigest(),
            "contact_sheet": hashlib.sha256(_read_staged_file(self._project_root, record.export.contact_sheet)).hexdigest(),
            "lineage": hashlib.sha256(_read_staged_file(self._project_root, record.lineage)).hexdigest(),
            "manifest": hashlib.sha256(_read_staged_file(self._project_root, record.export.manifest)).hexdigest(),
        }

    def _deliverable(self, kind: str, path: str, absolute: Path) -> dict[str, str]:
        return {"kind": kind, "project_relative_path": path, "sha256": hashlib.sha256(_read_staged_file(self._project_root, absolute)).hexdigest()}

    @staticmethod
    def _validate_engine_result(result: EngineResult, expected_count: int, candidates_dir: Path, anchor_bytes: bytes, *, delivery_eligible: bool, project_root: Path) -> None:
        if len(result.candidates) != expected_count:
            raise EngineContractError(f"engine returned {len(result.candidates)} candidates; expected {expected_count}")
        root = candidates_dir.resolve()
        resolved_candidates: list[Path] = []
        candidate_bytes: list[bytes] = []
        for candidate in result.candidates:
            resolved = candidate.resolve()
            if root not in resolved.parents or resolved.suffix.lower() != ".png":
                raise EngineContractError("engine candidate must be a PNG inside the run candidate directory")
            try:
                data = _read_staged_file(project_root, resolved)
                with Image.open(BytesIO(data)) as image:
                    rgba = image.convert("RGBA")
                    if rgba.getbbox() is None:
                        raise EngineContractError("engine candidate must not be fully transparent")
            except (OSError, ValueError, UnidentifiedImageError) as error:
                raise EngineContractError("engine candidate must be a readable PNG image") from error
            resolved_candidates.append(resolved)
            candidate_bytes.append(data)
        if len(resolved_candidates) != len(set(resolved_candidates)):
            raise EngineContractError("engine returned the same candidate path more than once")
        if delivery_eligible:
            try:
                with Image.open(BytesIO(anchor_bytes)) as anchor_image:
                    anchor_visual = hashlib.sha256(anchor_image.convert("RGBA").tobytes()).hexdigest()
                candidate_visuals = []
                for data in candidate_bytes:
                    with Image.open(BytesIO(data)) as image:
                        candidate_visuals.append(hashlib.sha256(image.convert("RGBA").tobytes()).hexdigest())
            except (OSError, UnidentifiedImageError) as error:
                raise EngineContractError("engine output visual hashes could not be verified") from error
            if len(candidate_visuals) != len(set(candidate_visuals)):
                raise EngineContractError("delivery-eligible expression candidates must not be pixel-duplicates")
            if any(value == anchor_visual for value in candidate_visuals):
                raise EngineContractError("delivery-eligible expression candidates must each visibly differ from the anchor")
