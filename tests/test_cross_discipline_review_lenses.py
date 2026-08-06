from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_review_lenses_preserve_single_owner_and_selective_use() -> None:
    reference = read(
        "skills/running-adversarial-review-and-refinement/references/"
        "cross-discipline-review-lenses.md"
    )
    for lens in (
        "제품·플레이어 가치",
        "UX·접근성",
        "아키텍처·상태 소유권",
        "구현·성능·플랫폼",
        "QA·회귀·출시",
        "문서·추적성·인수인계",
    ):
        assert lens in reference
    assert "결정을 소유하지 않는다" in reference
    assert "L2 이상" in reference
    assert "NOT_APPLICABLE" in reference
    for token in (
        "lens",
        "evidence",
        "affected_requirement",
        "severity",
        "owner_skill",
        "status",
    ):
        assert token in reference


def test_main_adversarial_skill_routes_lenses_without_named_agent_authority() -> None:
    skill = read("skills/running-adversarial-review-and-refinement/SKILL.md")
    assert "cross-discipline-review-lenses.md" in skill
    assert "L2 이상" in skill
    assert "주 책임" in skill
