from __future__ import annotations
from dataclasses import asdict, dataclass

@dataclass(frozen=True)
class Finding:
    code: str
    message: str
    path: str = ""

    def to_dict(self) -> dict[str, str]:
        return asdict(self)
