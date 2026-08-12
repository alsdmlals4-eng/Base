"""Application use cases and fail-closed run lifecycle."""

from dataclasses import dataclass, field
from pathlib import Path
from uuid import uuid4

from .curation import CurationState, save_curation
from .engine import EngineContractError, EngineResult, SpriteEngine
from .exporter import ExportResult, export_run
from .lineage import write_lineage
from .models import SpriteAnimationRequest
from .paths import RunPaths, resolve_project_path, create_run_paths


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
    frame_count: int = 0
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
        }


class SpriteAnimationService:
    def __init__(self, project_root: Path, engine: SpriteEngine) -> None:
        self._project_root = project_root.resolve()
        self._engine = engine
        self._runs: dict[str, RunRecord] = {}

    def create_run(self, request: SpriteAnimationRequest) -> RunRecord:
        anchor_path = resolve_project_path(self._project_root, request.anchor.source_path)
        if not anchor_path.is_file():
            raise ValueError("approved anchor source_path must point to an existing project file")
        resolve_project_path(self._project_root, request.output_root)

        run_id = uuid4().hex
        paths = create_run_paths(self._project_root, request.asset_id, request.action.name, run_id, request.output_root)
        lineage = write_lineage(request, anchor_path.read_bytes(), paths.run_dir)
        record = RunRecord(run_id=run_id, request=request, paths=paths, lineage=lineage, status="blocked")
        self._runs[run_id] = record
        try:
            result = self._engine.generate(request, paths.run_dir)
        except EngineContractError as error:
            record.warnings.append(str(error))
            return record
        record.status = "generated"
        record.frame_count = len(result.frames)
        return record

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
        if not frame.is_file():
            raise RunBlockedError("candidate frame file is unavailable")
        return frame

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
        if len(curation.selected) != record.request.action.frame_count:
            record.status = "blocked"
            record.warnings.append("all requested frames must be selected before export")
            raise RunBlockedError("all requested frames must be selected before export")
        record.export = export_run(record.paths.run_dir, record.request, curation)
        record.curation = curation
        record.status = "exported"
        return record
