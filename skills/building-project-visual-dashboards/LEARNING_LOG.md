# Learning Log

## 2026-08-21 · 행동 평가는 현재 Project Home 실행 단계를 이름으로 추적한다

- 2026-08-19의 HTML → Notion Project Home 재분류 뒤에도 `SBE-031`은 단일 HTML과 구형 `frame → map-sources → build → bind-status → validate`를 계속 요구해 current Skill과 충돌했다.
- 구형 HTML 경로를 부활시키지 않고 `frame-project-home → map-canonical-sources → build-project-home → bind-evidence-status → verify-destination-readback`을 current Skill Mode로 명시했다.
- 행동 평가는 self-contained Notion Home, 선택적 Visual Map, repository/runtime owner locator, evidence status와 exact destination readback을 요구한다.
- 정적 fixture·routing 계약 통과는 실제 Notion write/readback이나 사람 이해도 검증이 아니다. model behavior run과 실제 Project 적용은 계속 `NOT_RUN`이다.
- revisit_condition: Project Home의 실행 단계가 다시 바뀌거나 model behavior run이 mode 혼동·HTML 회귀·destination overclaim을 검출할 때 fixture와 Skill을 함께 재검토한다.

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

## 2026-08-19 · Workspace retirement는 기존 consumer contract를 보존하며 바꾼다

- Google Sheets active authority 제거와 Notion Home 재분류 과정에서 기존 GPO 테스트가 보호하던 `하위 시스템 checkpoint`, Skill package reference link, `Output contract`, `Quality gate` 같은 유효 소비 계약을 함께 잃으면 retirement 자체가 맞더라도 회귀다.
- 정책 변경 시 제거 대상 literal과 보존해야 할 capability를 분리하고, stale assertion은 current authority로 갱신하되 실제 유효 capability는 Registry·Skill body·reference에서 계속 소비되게 한다.
- frozen Base v9 Sheet artifact는 역사 증거로 보존하고 current migration-only authority는 별도 current decision/Workspace/Planning owner가 소유한다.
- reuse_scope: `BASE_PROMOTION_CANDIDATE`.
- revisit_condition: legacy retirement가 다시 unrelated capability 삭제나 historical artifact rewrite를 유발할 때 이 분리 계약을 재적용한다.
