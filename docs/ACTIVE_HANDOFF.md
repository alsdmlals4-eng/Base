# UX/UI 공용 체계 확산 Active Handoff

> 갱신: 2026-07-29 20:57 KST  
> Mode: `session-handoff`  
> 상태: `DOCUMENTATION_AND_VALIDATION_CONTRACTS_MERGED / HUMAN_VALIDATION_PENDING`  
> Base UX/UI 기준 커밋: `0fd95f4513343e77fd664af2763a01b02f52545b`

이 문서는 UX/UI 공용 체계의 프로젝트 확산 작업을 다음 채팅이나 작업자가 즉시 재개하도록 연결하는 압축 라우터다. 프로젝트별 규칙·수치·구현 상태를 복제하지 않으며, 상세 내용은 각 저장소의 책임 원본·계획·Issue가 소유한다.

## 현재 상태

| 저장소 | main 기준점 | UX/UI 상태 | 추적 Issue | 다음 진입 조건 |
|---|---|---|---|---|
| `Base` | UX/UI baseline `0fd95f4513343e77fd664af2763a01b02f52545b` | 공용 Skill·reference·template·검증 계약 병합 | 이 문서 | 프로젝트 증거에서 공용 승격 후보가 생길 때만 갱신 |
| `Blacksmith` | `0b3c1bcdd1d1f47f44c379473e7846756e24d231` | 계획·검증 계약 병합, 제품 검증 차단 | `#69` | 상위 재기획 `#60`, 새 코어·Vertical Slice·사용자 검수 완료 |
| `GRIMOIRE-` | `ce1f24f43b41d29deff006bfaadc2595bb123124` | 입력·인식·설계 오류 검증 계약 병합 | `#9` | `ART-STYLE-01`, Art Bible, 실행 프로필 승인 |
| `omenward` | `7f8dc279039c6f6cdc7903341405885709847da5` | V2 3라인·릴·배치 검증 계약 병합 | `#105` | 상위 제품 Issue `#69`, v6 승인, `PRODUCT_CODE_AUTHORIZED: YES` |
| `Ten-Paces-Hidden-Moves` | `380128c48cab3c9cf76e758bfb1293c42c37b8b8` | 적 의도·3/3/4·합 STEP 14 계약 병합 | `#54` | 최신 기획·16권 절초 승인, 런타임 금지 해제 |
| `urban-legend` | `70bf04105895ab5ce855d9682c9c85b9e6eee579` | CORE-MVP-001 실제 검증 패킷 준비 완료 | `#105` | 즉시 Phase 1·2 실행 가능, 사람 검증은 참가자 필요 |

작업 제외 저장소:

- `MylittleBoat`
- `ninja-survival-godot`
- `Coc-Fiction`
- Unity 보관 저장소

## 이번 작업 결과

- Base `auditing-and-refining-ui-art`에 UX 계약·정보 구조·패턴·Godot UI 경계·접근성·플레이테스트 Mode를 통합했다.
- 다섯 프로젝트에 `docs/UX_UI_SYSTEM.md` 책임 원본을 두고 Base 최종 UX/UI 기준 SHA를 동기화했다.
- 다섯 프로젝트에 `docs/superpowers/plans/2026-07-29-ux-ui-validation-plan.md`를 병합했다.
- 프로젝트별 UX 검증 Issue를 생성하고 현재 기획 Gate와 제품 변경 금지 조건을 기록했다.
- Urban Legend에 다음 검증 문서를 병합했다.
  - `docs/validation/URBAN_LEGEND_UX_UI_VALIDATION_PACKET.md`
  - `docs/validation/URBAN_LEGEND_UX_UI_VALIDATION_RESULTS.md`
- 제품 코드·Scene·data·asset은 변경하지 않았다.
- HTML 기획 대시보드는 범위에서 제외했다.

## 확정·구현·검증·미확정

### 확정

- Base 공용 UX/UI 방법과 프로젝트별 책임 분리
- UI가 도메인 규칙·피해·보상·저장·분기 결과를 재계산하지 않는 Godot 경계
- 자동·렌더·사람·접근성 증거의 독립 상태 관리
- 프로젝트별 검증 과제·fixture·통과 기준·차단 Gate

### 구현

- 문서·Skill·Adapter·Issue·검증 패킷만 구현됨
- 제품 Godot UX/UI 구현은 이번 작업 범위가 아님

### 검증

- Base와 자동 Workflow가 있는 프로젝트의 문서·계약 CI는 병합 전 성공함
- GRIMOIRE는 자동 Workflow가 없어 파일 범위·문서 구조를 수동 검토함
- Urban Legend 검증 패킷의 Documentation Contracts는 성공함

### 미검증

- Urban Legend 최신 main 기준 Godot import·parse와 신규 렌더 artifact
- Urban Legend 신규 플레이어 6명, 45분 사용성, 음향 OFF·모션 감소·입력 폴백
- 실제 장애 사용자 접근성 검증
- Blacksmith Android 실기기 검증
- GRIMOIRE, OMENWARD, 십보강호 런타임 검증

미실행 항목은 `NOT_RUN` 또는 `HUMAN_NOT_RUN`을 유지한다.

## 다음 작업과 선행 조건

### 우선순위 1 — Urban Legend Issue #105 Phase 1·2

첫 행동:

1. `urban-legend` 최신 `main`과 Issue `#105`를 연다.
2. 아래 책임 원본을 순서대로 읽는다.
3. 실제 실행 commit SHA를 `URBAN_LEGEND_UX_UI_VALIDATION_RESULTS.md`에 고정한다.
4. 기존 자동·렌더 경로를 같은 commit에서 재실행한다.
5. run URL·artifact ID·1280×720·1920×1080 판정을 기록한다.
6. 자동·렌더 기준선이 안정된 뒤에만 신규 플레이어 6명 테스트로 넘어간다.

읽기 순서:

```text
urban-legend/AGENTS.md
→ urban-legend/docs/CURRENT_STATUS.md
→ urban-legend/docs/UX_UI_SYSTEM.md
→ urban-legend/docs/superpowers/plans/2026-07-29-ux-ui-validation-plan.md
→ urban-legend/docs/validation/URBAN_LEGEND_UX_UI_VALIDATION_PACKET.md
→ urban-legend/docs/validation/URBAN_LEGEND_UX_UI_VALIDATION_RESULTS.md
→ urban-legend Issue #105
→ 실제 Scene·data·tests
```

자동·렌더 대상:

- `tests/test_core_mvp_001_data_contract.py`
- `tests/test_core_mvp_001_static_contract.py`
- `tests/core_mvp_001_scene_test.gd`
- `tests/test_mvp039_manual_ux_validation.gd`
- `tests/ui_visual_capture.gd`
- `scenes/poc/core_mvp_001/core_mvp_001_scene.tscn`
- `data/poc/core_mvp_001/afterlife_station_poc.json`

### 우선순위 2 — 기획 Gate가 열린 프로젝트만 진행

- Blacksmith: `#60` 승인 후 `#69`의 fixture·Android 검증 계약을 재확인한다.
- GRIMOIRE: `ART-STYLE-01`·Art Bible 승인 후 `#9`에서 작성 오버레이 최소 구현 계약을 만든다.
- OMENWARD: v6·제품 코드 승인 뒤 `#105`에서 V2 Scene·View Data·Signal 소유자를 읽기 전용 조사한다.
- 십보강호: 최신 기획·16권 절초 승인 뒤 `#54`에서 STEP 14 구현·사람 검증 Issue를 분리한다.

Gate가 닫힌 프로젝트에서 Codex Build나 제품 파일 변경을 시작하지 않는다.

## 보호 범위

- 프로젝트 최신 사용자 결정과 Active Context가 Base 공용안보다 우선한다.
- 제품 코드·Scene·data·asset은 승인된 별도 구현 Issue 전까지 변경하지 않는다.
- UX 개선 명목으로 전투·경제·괴이·마법 문법·3/3/4·분기·저장 규칙을 변경하지 않는다.
- 자동 테스트를 사람 이해도 증거로 대체하지 않는다.
- 사람 테스트 전 `POC_PASSED`, `CORE_LOOP_PROVEN`, `MVP_COMPLETE`를 선언하지 않는다.
- 제외 저장소에 이번 체계를 자동 확산하지 않는다.
- HTML 기획 대시보드를 다시 도입하지 않는다.

## 먼저 읽을 책임 원본

1. `AGENTS.md`
2. `docs/DOCUMENTATION_MAP.md`
3. `docs/ACTIVE_HANDOFF.md`
4. 대상 프로젝트의 `ACTIVE_CONTEXT` 또는 `CURRENT_STATUS`
5. 대상 프로젝트 `docs/UX_UI_SYSTEM.md`
6. 대상 프로젝트 UX/UI 검증 계획
7. 대상 프로젝트 추적 Issue와 실제 파일·테스트

## 호출 Skill

- 재개·상태 대조: `maintaining-project-context-and-handoff` / `resume`
- 새 UX 설계가 필요한 경우: `brainstorming` 후 `auditing-and-refining-ui-art`
- 런타임 UI 감사: `auditing-and-refining-ui-art` / `runtime-ui-audit`
- 사람 검증 계약: `auditing-and-refining-ui-art` / `playtest-contract`
- 공격적 검토: `running-adversarial-review-and-refinement`
- 변경·CI·증거 검수: `reviewing-and-validating-project-changes`
- 구현 계획: 승인 Gate 후 `writing-plans`
- 완료 주장 전: `verification-before-completion`

## 검증·미검증·롤백

### 확인된 문서 PR

- Blacksmith: `#68`, Base SHA 동기화 `#71`
- GRIMOIRE: `#8`, Base SHA 동기화 `#11`
- OMENWARD: `#104`, Base SHA 동기화 `#107`
- Ten Paces: `#53`, Base SHA 동기화 `#56`
- Urban Legend: 검증 계획 `#104`, 검증 패킷 `#107`, Base SHA 동기화 `#108`

### 롤백

이번 작업은 제품 파일을 변경하지 않았다. 문제가 생기면 해당 저장소의 위 문서 PR merge commit을 revert하고, 제품 코드·데이터·Scene에는 별도 롤백을 수행하지 않는다.

### 다음 세션 시작 문장

> `Base/docs/ACTIVE_HANDOFF.md와 대상 프로젝트의 UX-VALIDATION Issue를 읽고, 현재 Gate와 실제 main을 대조한 뒤 다음 미완료 단계부터 이어가줘. 제품 파일은 승인된 구현 Gate 전까지 수정하지 마.`
