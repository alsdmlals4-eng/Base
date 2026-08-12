"""Expression-specific packet built on the shared Figma routing contract."""

from __future__ import annotations

from dataclasses import dataclass

from base_tool_contracts import DeliveryBlockedError, ProjectFigmaRegistry, ProjectFigmaTarget

__all__ = [
    "DeliveryBlockedError",
    "FigmaDeliveryPacket",
    "ProjectFigmaRegistry",
    "ProjectFigmaTarget",
]


@dataclass(frozen=True)
class FigmaDeliveryPacket:
    run_id: str
    project_id: str
    anchor_figma_node_url: str
    target: ProjectFigmaTarget
    visual_deliverables: list[dict[str, str]]
    engine: dict[str, object]
    anchor_verification: str
    anchor_evidence: dict[str, str]

    def public_view(self) -> dict[str, object]:
        return {
            "status": "ready_for_project_gpt",
            "run_id": self.run_id,
            "project_id": self.project_id,
            "anchor_figma_node_url": self.anchor_figma_node_url,
            "target": {
                "project_id": self.target.project_id,
                "display_name": self.target.display_name,
                "figma_file_key": self.target.figma_file_key,
                "figma_url": self.target.figma_url,
                "delivery_page": self.target.delivery_page,
                "generation_area": self.target.generation_area,
                "delivery_page_node_id": self.target.delivery_page_node_id,
                "generation_area_node_id": self.target.generation_area_node_id,
            },
            "visual_deliverables": self.visual_deliverables,
            "engine": self.engine,
            "anchor_verification": self.anchor_verification,
            "anchor_evidence": self.anchor_evidence,
            "delivery_instruction": "Use this packet only in the matching project GPT workspace with the Figma connector; Expression Studio has not uploaded anything.",
        }
