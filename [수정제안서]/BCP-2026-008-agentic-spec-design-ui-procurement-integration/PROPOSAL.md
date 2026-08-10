# BCP-2026-008 — 에이전트 명세·디자인·외부 UI 조달 책임의 선택적 통합

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base`
- 원 제안 기준 커밋: `c7e678c928d08e736694319184f090ee87009efc`
- 원 제출일: `2026-08-06`
- 상태: `IMPLEMENTED`
- 기록 유형: `HISTORICAL_RECONCILIATION`
- 원 제안 PR: [#190](https://github.com/alsdmlals4-eng/Base/pull/190)
- 구현 PR: [#192](https://github.com/alsdmlals4-eng/Base/pull/192)

## 관찰과 증거

BCP-008은 원래 PR #190의 Draft proposal로 제출됐다. PR #190은 Draft로 종료되어 병합되지 않았다. 그러나 해당 PR의 승인 comment를 근거로 별도 구현 PR #192가 병합됐고, 그 구현물과 적대적 검토 기록은 현재 `main`에 남아 있다.

- 승인 근거: `docs/evidence/external-ui-procurement/BCP008_APPROVAL_REF.md`
- 구현·적대적 검토: `docs/evidence/external-ui-procurement/BCP008_ADVERSARIAL_REVIEW.md`
- 구현 PR 병합 커밋: `b96d9dfe09ef33a18e9b31113eb480ad7a919b1f`
- 현재 결과: `FEATURE_SPEC_TRACEABILITY_PACKET`, 교차 분야 검토 Lens, 선택형 `DESIGN.md` Adapter, 외부 UI 조달·anti-generic Gate

## 일반화 후보

L2 이상 작업은 기존 책임 원본을 대체하지 않는 Traceability Packet으로 Decision·Requirement·Acceptance·Implementation·Verification 연결을 확인한다. 다분야 공격은 기존 적대적 검토의 Lens로 수행하며, 프로젝트 시각 토큰과 외부 UI 조달은 기존 UI 책임 안에서 출처·라이선스·보안·접근성·실제 렌더 Gate를 거친다.

## 적용 조건과 비사용 조건

- 적용: L2 이상 기능의 추적성, 다분야 검토, 선택형 프로젝트 `DESIGN.md`, 외부 UI Registry·MCP·코드 조달을 검토할 때
- 비사용: L0/L1 기계 수정, 외부 UI 검색 성공을 설치·채택·품질 통과로 오인하는 경우, 기존 owner를 대체하는 새 ACTIVE Skill을 만드는 경우

## 반례와 위험

- PR #190의 미병합 상태를 구현 미실행으로 해석하면 PR #192 병합과 현재 구현물을 놓친다.
- PR #192 병합만 보고 원 proposal lifecycle이 `main` Registry에 없던 사실을 숨기면 BCP-001~019 전수 감사가 불가능해진다.
- 역사 record를 새 제안으로 위장하면 proposal-only gate를 약화할 수 있다. 따라서 이 항목은 `historical_reconciliation: true`인 구현 완료 backfill로만 허용하며, 원 PR·승인 comment·구현 PR을 모두 보존한다.

## 영향 범위와 검증

- 영향: 기존 활성 Skill·Registry 라우팅·released lock은 바꾸지 않고 Proposal Registry와 canonical history record만 보강한다.
- 검증: 원 PR #190의 미병합 상태, PR #192의 병합 상태·merge SHA, Registry와 canonical Proposal의 링크·상태를 함께 대조한다.
- 롤백: 잘못된 역사 근거가 발견되면 Registry entry와 이 reconciliation record를 함께 되돌리되, PR #190/#192와 기존 evidence는 삭제하지 않는다.

## 승인과 구현

- 원 승인 참조: `https://github.com/alsdmlals4-eng/Base/pull/190#issuecomment-5198050799`
- 원 구현 PR: `https://github.com/alsdmlals4-eng/Base/pull/192`
- 구현 상태: PR #192는 병합됐고, 이 문서는 2026-08-10 BCP-001~019 repository-wide audit에서 발견한 Registry history 누락을 닫는다.
- closeout 병합 커밋: `b96d9dfe09ef33a18e9b31113eb480ad7a919b1f`
- 검증 한계: 실제 게임 프로젝트에 외부 UI를 설치·렌더·접근성·사람 품질 평가한 사실은 이 historical reconciliation이 증명하지 않는다.
