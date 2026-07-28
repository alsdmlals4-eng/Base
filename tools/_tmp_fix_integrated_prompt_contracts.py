from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(relative: str, old: str, new: str) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{relative}: expected one occurrence, found {count}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def main() -> None:
    replace_once(
        "docs/knowledge/vertical-slice/SKILL_ORCHESTRATION_AND_EVIDENCE.md",
        "→ Demo-First Slice 계약·품질·파이프라인",
        "→ DEMO_FIRST_VERTICAL_SLICE 계약·품질·파이프라인",
    )
    replace_once(
        "docs/knowledge/vertical-slice/ASSET_MASCOT_AND_TUNING.md",
        "→ Godot 기본 기능·공식 Asset Store·공식 GitHub·신뢰 가능한 마켓 조사",
        "→ Godot 기본 기능·공식 Asset Store(에셋스토어)·공식 GitHub·신뢰 가능한 마켓 조사",
    )
    replace_once(
        "docs/knowledge/VERTICAL_SLICE_V6_REQUIREMENT_COVERAGE.md",
        "## 허용된 Legacy",
        "## ALLOWED_LEGACY — 허용된 역사·호환 표현",
    )


if __name__ == "__main__":
    main()
