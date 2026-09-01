# Base 활성 작업면 정리·프로젝트 시작 게이트 실행 계획

> 기준: 781dfe8faf0da26c04abb437ae68f94db2cb106b
> 승인: 현재 사용자 요청의 범위 내 교정·archive·보완 권한 재사용

## 목표

활성 Base 라우팅과 project adapter의 실제 연결을 유지하면서, 현재 소비되지 않는 schema-v3 역사 감사를 기본 작업면에서 제거하고, 프로젝트 L1+ 작업이 receipt 검증을 건너뛰지 않도록 모든 시작 entrypoint를 하나의 exact-pin gate로 수렴한다. 적대적 검토에서 발견된 active engine policy의 V3 workspace authority 잔존 표현도 V4 repository-first로 교정한다.

## 단계

1. registry, shared route, generated artifact, canonical reference freshness와 baseline test를 fresh-read한다.
2. candidate별 consumer, compatibility, unique evidence, Git rollback을 조사해 KEEP/COMPATIBILITY/ARCHIVE/UNVERIFIED를 판정한다.
3. 회귀 검사를 먼저 RED로 만들어 archive lifecycle과 project receipt route 누락을 드러낸다.
4. project start template, AI workflow, current router, base project router, default Work→Codex starter와 adapter contract를 current checklist/validator에 연결한다.
5. 두 history audit을 Archive로 이동하고 Manifest, original link, current replacement, hash, rollback을 갱신한다.
6. receipt validator, targeted tests, reference freshness, generated checks, whole regression을 실행한다.
7. 다섯 번 이상의 적대적 재검토에서 실제 finding만 교정한다.
8. active engine policy와 소비 test가 V4 authority를 요구하도록 RED/GREEN으로 교정한다.
9. exact-head branch를 push, PR/required checks/review, squash merge, main readback 순서로 처리한다.

## 검증·롤백

- archive 대상은 원래 tracked path가 사라지고 archive original body hash가 Manifest와 일치해야 한다.
- reference-zero는 이동 후 active routes에서 다시 검색하며, unknown consumer가 발견되면 삭제 대신 Archive/COMPATIBILITY로 되돌린다.
- project route는 adapter pin이 확인되지 않거나 Base validator가 해석되지 않으면 실행하지 않는다.
- rollback은 이 branch의 commit revert이며, Archive 원문은 manifest rollback ref와 Git history에서 복구할 수 있다.

## 적대적 검토 결과

1. 활성 authority/Archive: 기존 두 audit의 default docs path가 사라지고, EVIDENCE_RETENTION Manifest record의 destination body SHA-256·rollback ref·비권위 상태가 일치함을 확인했다.
2. project receipt execution: 모든 project-start entrypoint와 intake/분해/계획 surface를 검색했다. 세 generic `python tools/validate_work_contract_receipt.py` 경로를 발견해, current Base 또는 project adapter pin의 resolved Base root 경로로 교정했다.
3. compatibility: v7/v8 prompt, v4.9 compatibility appendix, v1 adapter schema, Godot operation envelope은 current tests 또는 compatibility consumers가 있어 삭제하지 않았다.
4. scope/integrity: 변경 범위는 current routing, archive evidence, regression, plan/spec/receipt에 한정했다. unrelated open PR·project repository·runtime asset은 건드리지 않았다.
5. integration safety: fresh fetch 뒤 branch가 origin/main 781dfe8의 descendant임을 확인했고, 다른 열린 PR은 read-only로 유지했다.
6. independent review readback: active `ENGINE_BASELINE_AND_ADAPTER_POLICY.md`가 `NOTION_HUMAN_FACING_CANON`과 `DOMAIN_SPLIT_CANON`을 현재 workspace authority로 선언한 것을 발견했다. engine baseline/adapter 선택은 유지하고, policy와 direct test를 V4 `REPOSITORY_PRIMARY_CANON`·`HUMAN_GDD_PDF_DERIVED_VIEW`·exception-only boundary로 RED/GREEN 교정했다.
7. final independent review: default Work→Codex starter가 receipt gate를 우회하고 Intake Skill의 receipt 예시가 validator root schema와 혼동될 수 있음을 발견했다. starter를 same pin/receipt/nonzero `BLOCKED_UNVERIFIED` gate로 보완하고, Intake Skill에 executable root JSON example을 추가한 뒤 이 example과 모든 entrypoint를 regression으로 검증했다.

유효한 finding은 2번, 6번, 7번이었고 같은 승인 범위 안에서 교정했다. 나머지는 no finding 또는 보존 판정이다.

## 검증 결과

- receipt validator: PASS
- focused archive/project route/V4 engine authority regression: PASS
- final review correction (starter gate + Intake root receipt example): 20 tests PASS
- selected governance/skill/reference suite: 66 tests PASS
- canonical reference freshness, generated Base artifacts, Skill implementation evidence, required-gate topology: PASS
- independent review before PR: PASS (Critical/Important findings: 0)
- PR CI correction: `local-skill-contract-learning-test-sync`가 요구하는 기존 운영체계 회귀검사를 추가해, 모든 L1+ 프로젝트 시작점의 same-pin receipt gate를 다시 고정했다.
- final local full regression after the CI-coupling correction: 2,430 tests PASS, 54 skipped, exit 0
- PR #822 exact-head CI: required `ci-gate`와 모든 필수 validation job PASS
- post-merge `main` readback: Squash merge commit `d060ffabdc827b929f66c4a6a1ad329a866885ac`에서 Game Project Operating System의 Windows publication smoke·core regression·`ci-gate`를 포함한 모든 job PASS
