# One-Click Play Handoff Design

Status: USER_APPROVED_DESIGN · IMPLEMENTATION_AUTHORIZED

## Goal

게임 프로젝트의 대표 Vertical Slice·Demo를 최종 인계할 때 사용자가 저장소를 갱신하고 엔진의 기본 **Project Play**만 실행하면 실제 플레이 흐름을 확인할 수 있게 한다. 별도 Scene 선택, 편집기 수동 설정, 숨은 feature flag, 파일 교체를 사용자에게 요구하지 않는다.

## Scope

이 공용 계약은 게임 엔진 프로젝트의 대표 플레이 빌드·Vertical Slice·Demo 인계에 적용한다. 프로젝트 고유 validation harness, 테스트 Scene, 플랫폼별 export override는 유지할 수 있지만 일반 사용자 검수의 기본 진입점과 혼동시키지 않는다.

## Architecture

기존 책임 원본에 분산 반영한다.

1. `designing-vertical-slices`
   - 대표 구간은 기본 Project Play에서 진입 가능해야 한다.
   - 타이틀 또는 시작 화면에서 실제 대표 플레이의 성공·실패·복귀 흐름까지 연결한다.
2. `reviewing-and-validating-project-changes`
   - 사용자 시작점에서 기본 실행을 검증한다.
   - 별도 Scene 선택·수동 editor 설정이 필요하면 완료가 아니다.
3. `synchronizing-local-and-github-state`
   - 작업자는 승인 Branch에 commit·push한다.
   - 사용자는 `Fetch origin → Pull origin`으로 같은 Branch·Commit을 받는다.
   - Fetch만 수행한 상태를 적용 완료로 간주하지 않는다.
4. `maintaining-project-context-and-handoff`
   - repository, branch, commit SHA, 갱신 절차, 기본 실행 동작, 기대 첫 화면, 남은 수동 gate를 인계한다.
5. `templates/project-operations/AI_WORKFLOW.md`
   - 프로젝트 운영 템플릿의 완료·Handoff Gate에 같은 공용 계약을 노출한다.

새 Skill은 만들지 않는다. 기존 책임 경계를 강화한다.

## Runtime contract

```text
작업자 구현·검증
→ 승인 Branch에 commit·push
→ 사용자 GitHub Desktop에서 올바른 저장소·Branch 선택
→ Fetch origin
→ Pull origin
→ 엔진 프로젝트 다시 열기
→ Project Play
→ 대표 Demo의 첫 화면
→ 실제 플레이 성공·실패·복귀 흐름
```

- `Fetch origin`은 원격 상태 확인이며 로컬 파일 적용이 아니다.
- `Pull origin` 또는 동등한 fast-forward 갱신 뒤 로컬 HEAD가 전달 Commit과 일치해야 한다.
- 프로젝트의 기본 실행은 대표 플레이 UI·입력 표면을 표시해야 한다.
- debug·validation 전용 진입점은 별도 명령·feature override로 유지한다.

## Evidence and status

자동 테스트는 다음을 최소 증명한다.

- 기본 main scene 또는 entrypoint가 존재한다.
- 기본 실행이 대표 Demo root를 생성한다.
- 첫 화면과 실제 gameplay surface로 전환할 수 있다.
- 핵심 HUD·도구·입력 표면이 표시된다.
- 대표 성공·실패 경로와 복귀가 회귀 테스트로 연결된다.

실제 로컬·Windows·device 조작을 실행하지 않았다면 `NOT_RUN`이다. 사용자가 실행했으나 HUD·입력·흐름이 동작하지 않으면 `FAIL · RETEST_REQUIRED`로 기록하고 완료·Ready·Production PASS를 주장하지 않는다.

## Completion gate

다음 중 하나라도 필요하면 인계 완료가 아니다.

- 사용자가 Scene을 직접 찾아 F6로 실행해야 함
- Project Settings에서 main scene을 수동 지정해야 함
- 입력 모드·플러그인·feature flag를 사용자에게 수동 설정하게 함
- Fetch만 안내하고 Pull 또는 로컬 HEAD 확인을 생략함
- 자동 boot·flow 테스트 없이 “실행될 것”으로 추정함
- 실제 플레이 실패를 패키징 PASS로 덮음

## Rollback

기본 실행 전환이 validation harness 또는 플랫폼 export를 훼손하면 제품 bootstrap 변경을 되돌리고 별도 feature override를 복구한다. 사용자 작업 유실을 막기 위해 force push·hard reset을 기본 절차로 사용하지 않는다.
