# Learning Log

## 2026-08-19 · HTML builder에서 Notion human-facing projection owner로 재분류

- standalone HTML dashboard는 사용자 기본 작업면에서 제거한다.
- 그러나 “복잡한 프로젝트를 사람이 한 화면에서 이해하도록 구조화한다”는 책임 자체는 여전히 필요하다.
- 별도 Skill을 새로 만들기보다 기존 `building-project-visual-dashboards`의 목적을 Notion Project Home / Visual Map으로 재분류하는 편이 routing/consumer 안정성과 context 비용에서 더 강하다.
- QA Evidence Studio는 project-management dashboard가 아니라 specialist validation utility이므로 별도 유지한다.
- disposition: `RECLASSIFY + IMPROVE`.
- reuse_scope: `BASE_PROMOTION_CANDIDATE`.

## 2026-08-19 · Skill freshness companion은 같은 의미를 검증해야 한다

- Skill description/body가 바뀌었다고 해서 아무 Part 테스트나 `require_any_changed`를 만족시키도록 허용하면 freshness gate가 형식만 통과하고 실제 라우팅 의미를 검증하지 못한다.
- `building-project-visual-dashboards`의 Notion Home 재분류는 `tests/test_skill_routing_governance.py`에서 `notion-project-home` trigger, active `use_when`, standalone HTML 금지 경계를 직접 검증한다.
- `tests/test_p0[1-9]_*.py` 같은 광역 wildcard를 generic Skill companion으로 허용하는 대안은 기각한다. owner-local Part 테스트 지원이 필요하면 P08 후속에서 source owner와 test owner의 의미 일치를 검증하는 별도 계약으로 해결한다.
- reuse_scope: `BASE_PROMOTION_CANDIDATE`.
- revisit_condition: owner-local focused test가 반복적으로 canonical freshness에 막힐 때 semantic owner-aware companion resolution을 구현한다.
