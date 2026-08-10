# BCP - 괴이기록국(urban-legend)

## 출처와 상태

- Proposal ID: `BCP-2026-014-handoff-machine-consumer-compatibility-closeout`
- 출처 프로젝트: `alsdmlals4-eng/urban-legend`
- 출처 프로젝트 기준 Handoff head: `2b424906c4ecaa4a027719383d3400486b03c72e`
- 관련 프로젝트 PR: `urban-legend #187`
- 관련 Base Proposal: `BCP-2026-013-post-merge-continuation-state-reconciliation`
- 제출일: `2026-08-10`
- 상태: `SUBMITTED`
- 지식 상태: `관찰`
- Existing Solution Verdict: `ABSORB`
- 사용자 표시명 규칙: `BCP - 프로젝트 이름`

이 파일은 사용자 지정 명명 규칙에 따라 `bcp-괴이기록국(urban-legend)` 경로를 canonical proposal surface로 사용한다. 기계 추적용 Proposal ID는 기존 `BCP-2026-014-handoff-machine-consumer-compatibility-closeout`를 유지한다.

## 관찰과 증거

`urban-legend`의 `docs/CURRENT_HANDOFF.md`를 최신 상태 중심으로 압축했을 때, 사람이 읽는 현재 상태는 더 정확해졌지만 기존 테스트·validator가 과거 호환 토큰을 machine-consumed contract로 사용하고 있어 exact-head CI가 실패했다.

최종 복구에서는 현재 상태와 historical compatibility를 분리한 뒤 exact-head workflow 5개가 모두 PASS했다. 전체 원본 제안 본문과 상세 증거는 다음 파일에 그대로 보존한다.

- `evidence/ORIGINAL_BCP_2026_014_DETAIL.md`
- `evidence/URBAN_LEGEND_HANDOFF_COMPATIBILITY_EVIDENCE.md`

## 일반화 후보

Handoff/Active Context를 큰 폭으로 갱신하거나 closeout할 때는 사람용 현재 상태만 갱신하지 않고 다음을 함께 수행한다.

```text
runtime/repository truth 확인
→ machine consumer inventory
→ CURRENT_AUTHORITY / HISTORICAL_COMPATIBILITY_ONLY / STALE_REMOVE 분류
→ current-state 압축
→ exact-head contract validation
→ 실패 원인 귀속
→ compatibility 보존 또는 consumer migration
→ exact-head GREEN
→ closeout
```

새 광역 Skill을 만들기보다 기존 `maintaining-project-context-and-handoff`와 `auditing-canonical-reference-freshness`에 흡수하는 후보로 유지한다.

## 프로젝트 전용으로 남길 내용

Base 공용 규칙으로 복사하지 않는다.

- `urban-legend`의 PR·commit·Decision ID
- `Ver 4.2` / `Ver 4.3` 자체
- `CORE-VALIDATION-001`, `UX-PD-001 2A`, `mvp-039`, `POC_PASSED: NOT_DECLARED` 자체
- 프로젝트 Google Sheet 주소·셀 범위
- Godot runtime blocker와 게임 고유 상태

## 적용 조건과 비사용 조건

적용:
- Handoff/Active Context를 대폭 교체한다.
- 테스트·workflow·validator·parser가 해당 문서를 소비한다.
- 현재 상태와 과거 호환 문자열이 혼동될 위험이 있다.

비사용:
- machine consumer가 없는 단순 메모/오탈자다.
- 폐기된 consumer 자체를 같은 승인 범위에서 안전하게 migration할 수 있다.
- 프로젝트 전용 값만 존재하고 공용 lifecycle gap이 없다.

## 반례와 위험

- 오래된 테스트 하나만 폐기된 요구를 소비한다면 영구 compatibility token을 추가하지 말고 consumer migration이 더 적절하다.
- 날짜가 붙은 historical snapshot은 현재 상태로 rewrite하지 않는다.
- compatibility 영역이 쓰레기통이 되지 않도록 각 토큰에 실제 consumer 근거를 요구한다.

## 영향 범위와 검증

제안 단계에서는 Base 활성 Skill·Method·Template·Tool·Schema·Test·Workflow를 수정하지 않는다.

승인될 경우 후보 범위:
- `skills/maintaining-project-context-and-handoff/SKILL.md`
- `skills/auditing-canonical-reference-freshness/SKILL.md`
- 관련 기존 regression test / learning log

검증 기준:
- current truth와 historical compatibility가 명확히 분리된다.
- machine consumer 누락 시 closeout을 GREEN으로 주장하지 않는다.
- exact-head validation을 통과해야 한다.

## 필요한 도구·파일·권한

- 필요 항목: GitHub 저장소 read/write, Actions 결과 read, Proposal Registry read/write
- 필요한 이유: proposal/evidence/registry 정합성과 exact-head 검증을 확인하기 위해서다.
- 설치·적용 방법: Base proposal lifecycle을 사용한다.
- 설치 후 확인 명령: Base proposal validator 및 관련 CI
- 최소 권한: proposal-only `[수정제안서]/**` write; 활성 Base 구현 권한은 별도 승인 필요

## 승인과 구현

- 사용자 승인 근거: 본 proposal storage 및 프로젝트명 기반 명명 규칙 적용 승인
- 제안 상태: `SUBMITTED`
- 활성 Base 구현 승인: `미승인`
- 구현 PR: `없음`
- 롤백: 이 canonical proposal path와 Registry entry를 이전 상태로 되돌리면 되며 활성 Base 동작에는 영향이 없다.
