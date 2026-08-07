# Maintaining Project Context and Handoff Learning Log

## 2026-08-08 — On-demand Codex handoff and inherited merge authority

### Context

최근 확정된 실제 작업 방식은 GPT에서 기획·조사·구조 설계와 필요한 Godot POC·사전 구현을 오래 진행하고, 사용자가 Codex 전환을 요청하는 시점에만 실행 명세를 만들어 실제 저장소·프로젝트·Godot 상태를 다시 확인시키는 구조다.

### Finding

- 모든 Codex Build 전에 별도 읽기 전용 Codex Plan을 강제하면 명확한 저위험 작업에서도 비용·지연이 증가한다.
- GPT를 비-Godot 작업으로만 제한하면 현재 도구·POC·사전 제작 활용 방식과 충돌한다.
- GPT가 만든 명세는 의도 전달 계약이지 실제 구현 사실의 정본이 아니므로, Codex는 현재 GitHub 저장소·프로젝트 파일·Godot 상태를 직접 재검증해야 한다.
- 사용자가 이미 명시적으로 승인한 동일 범위에 병합 승인까지 반복 요청하면 승인 생명주기가 중복된다. 다만 새 범위·새 기획 결정·`USER_REVIEW_REQUIRED`·`CHANGE_PROPOSAL`·P0/P1은 기존 승인으로 덮으면 안 된다.

### Decision

- 새 광역 Skill을 만들지 않고 기존 `maintaining-project-context-and-handoff`에 `on-demand-codex-handoff` mode를 추가한다.
- `implementation-package-handoff`는 L2 이상·다중 의존성·고위험 작업의 패키지 인계 책임을 유지한다.
- Codex Plan은 `CODEX_PREFLIGHT_OPTIONAL`로 바꾸고 위험·불확실성·사용자 요청에 따라 선택한다.
- `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`를 적용해 동일 승인 범위의 PR은 새 차단 finding이 없으면 추가 확인·재승인·병합 승인 요청 없이 검증 후 병합한다.

### Validation evidence

- TDD test-only RED: `32078a5afb886d71245a324529bf90cf33479ea2`
- RED에서 새 on-demand/merge-authority 계약 부재로 required validation failure를 확인했다.
- GREEN 구현은 Draft PR `#215`에서 진행 중이며 exact-head contract, reference freshness, adversarial, Required Check를 다시 검증한다.

### Reuse boundary

새 Skill은 독립 입력·산출물·승인 권한이 생기고 기존 Handoff 책임에 넣을 때 경계가 무너지는 경우에만 검토한다. 현재는 같은 인계 생명주기의 mode 차이이므로 기존 Skill 흡수가 더 적합하다.
