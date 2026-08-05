# Base 중복·공백·책임 경계 분석

- 기준 Repository: `alsdmlals4-eng/Base`
- 기준 Commit: `c7e678c928d08e736694319184f090ee87009efc`
- 분석일: `2026-08-06`
- 분석 상태: 문서·Registry·Skill 책임 대조 `COMPLETE`; 구현·Pilot·모델 행동 `NOT_RUN`

## 1. 현재 권한 지도

| 현재 책임 | Base owner | 외부 도구와 겹침 |
|---|---|---|
| 의도·질문·실행 계약·Grill Me | `managing-project-intake-and-work-contract` | Superpowers, Spec Kit clarify, BMAD Analysis |
| 기획·책임 원본·Decision | `managing-design-documents` | Spec Kit spec/constitution, BMAD PRD |
| 작업 분해·순서 | intake `decompose-and-sequence` | Spec Kit tasks, BMAD stories |
| 공격·비판 검증·회귀 | `running-adversarial-review-and-refinement` | BMAD role review, Spec Kit analyze |
| 변경 증거·완료 판정 | `reviewing-and-validating-project-changes` | Spec Kit analyze/implement validation |
| UX/UI·디자인 시스템·Godot | `auditing-and-refining-ui-art` | DESIGN.md, taste-skill, shadcn |
| Skill 통합 경계 | `evolving-project-discipline-skills` | Superpowers Skill ecosystem |

## 2. 중복 판정

### Superpowers 전체 복제

`REJECTED_DUPLICATE`

Base가 이미 사용자 승인 전 구현 금지, 설계·계획, TDD·검증·적대 검토를 운영한다. 외부 Skill 이름과 파일을 다시 등록하면 자동 routing과 owner가 중복된다.

### Spec Kit 전체 설치

`REJECTED_DUPLICATE_WITH_TOOL_RISK`

constitution/spec/plan/tasks/implement는 Base의 AGENTS·책임 원본·계약·작업 분해·BUILD와 중복된다. CLI·slash command·shell 실행 경로는 Base 권한 Gate 밖의 자동 행동을 추가할 수 있다.

### BMAD Named Agent 설치

`REJECTED_AUTHORITY_FRAGMENTATION`

동일 Decision이 PM·Architect·UX·Developer 문서에 분산될 수 있고 주 책임 Skill 하나와 단일 정본을 약화한다.

### taste-skill 원문 설치

`REJECTED_WEB_AND_TASTE_BIAS`

실제 frontend 생산에는 유용할 수 있으나 Base 공용 게임 UI 규칙으로는 특정 stack·font·icon·미감 편향이 강하다.

## 3. 확인된 공백

### GAP-01 명세 산출물 추적성

현재 Base에는 Decision·Issue·Plan·정본·검증이 있으나 다음 연결을 공통 ID Packet으로 강제하는 얇은 표준이 명확하지 않다.

```text
Requirement
→ Acceptance
→ Task
→ Implementation
→ Verification
```

판정: `SHOULD_ADD_AS_TEMPLATE_AND_EXISTING_MODES`

### GAP-02 교차 분야 공격 관점

현재 적대적 검토는 강하지만 제품·UX·아키텍처·구현·QA·문서 관점의 최소 Coverage를 재사용 가능한 Lens로 명시하면 다분야 누락 방지에 도움이 된다.

판정: `SHOULD_ADD_AS_REFERENCE`

### GAP-03 기계 판독 시각 token 정본

현재 UX/UI 계약은 경험·흐름·상태·접근성·Godot 책임이 강하지만 색·타이포그래피·spacing·radius·component token의 portable representation과 source version 계약은 상대적으로 약하다.

판정: `SHOULD_ADD_AS_OPTIONAL_PROJECT_TEMPLATE_AND_ADAPTER`

### GAP-04 외부 UI code 조달 Gate

Base에는 에셋·플러그인·권리 검토가 있으나 Web Registry·MCP가 실제 source file과 dependency·script·secret·overwrite를 프로젝트에 전달하는 경우의 전용 UI 조달 체크가 명시적이지 않다.

판정: `SHOULD_ADD_AS_UI_REFERENCE`

### GAP-05 anti-generic 품질 판정

현재 polishing-pass가 P0~P3·실제 렌더·접근성·반복 피로를 다루지만, AI가 반복 생성하는 generic layout·불필요한 decorative pattern을 프로젝트 Design Read와 비교하는 진입 질문을 보강할 수 있다.

판정: `SHOULD_MERGE_INTO_EXISTING_POLISHING`

## 4. 책임 경계

| 산출물 | 단일 owner | 금지 |
|---|---|---|
| Requirement traceability Packet | intake·design docs가 생성, validation이 대조 | 상세 기획 정본으로 승격 |
| Cross-discipline Finding | adversarial review | 독립 Agent가 Decision 확정 |
| GAME_UX_UI_SYSTEM | UI 경험·행동 owner | 색 token만으로 축소 |
| 프로젝트 DESIGN.md | 시각 token owner | 게임 규칙·상태 소유권 포함 |
| 외부 code procurement record | UI audit + 기존 보안/라이선스 owner | MCP 자동 설치를 승인으로 간주 |
| anti-generic Finding | UI polishing/audit | 취향만으로 MUST_FIX 판정 |

## 5. 예상 구조 변화

```text
활성 Skill 수: 변화 없음
Skill Registry: 변화 없음 예상
새 Template: 2
새 Reference: 3
기존 Skill body: 필요한 routing·input/output·quality gate만 최소 수정
focused tests: 신규 또는 기존 suite 확장
```

## 6. 적대적 공격

### 공격 A — 새 Template이 또 다른 정본을 만든다

- 위험: Requirement Packet과 DESIGN.md가 기존 GDD·UX 문서를 복제
- 방어: Packet은 ID 연결만, DESIGN.md는 시각 token만 소유
- 판정: `VALID_CRITIQUE_MUST_GUARD`

### 공격 B — 새 Skill 0개 결정이 공백을 억지로 기존 owner에 넣는다

- 위험: 기존 Skill body가 비대해질 수 있음
- 방어: 본문에는 route와 output만 추가하고 상세 절차는 작은 Reference로 분리
- 재분리 조건: 독립 trigger·입력·산출물·검증·승인 경계가 두 개 이상의 Pilot에서 반복 증명
- 판정: `VALID_CRITIQUE_GUARDED`

### 공격 C — DESIGN.md가 Web 유행을 Godot에 강제한다

- 위험: px/rem·CSS component semantics를 Theme에 그대로 복제
- 방어: token 의미를 보존하되 Godot mapping과 Web mapping을 분리
- 판정: `VALID_CRITIQUE_MUST_GUARD`

### 공격 D — BMAD Lens가 형식적인 체크리스트가 된다

- 위험: 모든 작업에 6개 관점을 기계 적용해 비용만 증가
- 방어: L2 이상 다분야 작업에서만 관련 Lens를 선택하고 non-applicable 이유 기록
- 판정: `VALID_CRITIQUE_GUARDED`

### 공격 E — anti-generic 규칙이 창작 다양성을 억제한다

- 위험: 특정 패턴을 무조건 금지
- 방어: Design Read·플레이어 가치·접근성·실제 렌더와 비교하고 의도 있는 사용은 허용
- 판정: `VALID_CRITIQUE_MUST_GUARD`

### 공격 F — 외부 source 조사만으로 실제 유효성을 과장한다

- 위험: 문서상 장점을 Base 효과로 주장
- 방어: 현재 제안은 `패턴`; 실제 프로젝트 Pilot·모델 행동·사람 품질은 `NOT_RUN`
- 판정: `VALID_CRITIQUE_GUARDED`

## 7. 최종 판정

```yaml
recommendation: SELECTIVE_INTEGRATION
new_active_skill: 0
existing_owner_extension: true
proposal_only_pr: true
implementation_requires_new_approval: true
external_cli_or_mcp_installation: NOT_RUN
project_pilot: NOT_RUN
model_behavior_eval: NOT_RUN
human_ui_quality_eval: HUMAN_NOT_RUN
```
