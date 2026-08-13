# Capsule and Locks

## Entry Gate

```text
PLANNING_LOCKED
+ VISUAL_LOCKED 또는 PACKAGE_VISUAL_IMPACT_NONE
+ PROJECT_ADAPTER_VALIDATED
+ REQUIREMENT_COVERAGE_INITIALIZED
= AUTONOMOUS_IMPLEMENTATION_READY
```

## Project Execution Capsule

권장 프로젝트 경로는 `docs/operations/loop/`이며 Capsule, Planning Lock, Visual Lock, Adapter, Validation Profile, Active Run, immutable Runs, Implementation Packages, Coverage Ledgers를 둔다.

Capsule은 `project_id`, exact source SHA, Lock/Adapter 참조, Capability, 보호면, semantic resource domain, Autonomy, Runtime provider, context isolation을 선언한다. 완료 Run은 덮어쓰지 않고 `ACTIVE_LOOP_RUN.json`만 현재 실행을 가리킨다.

## Planning Lock

프로젝트 코어, 플레이어 경험, 승인 시스템·콘텐츠·기능, Acceptance Criteria, 보호 의미, 제외 범위, Decision ID와 책임 원본을 잠근다. 내부 클래스 구조·파일 분리·캐시·Signal·테스트 전략 같은 가역 HOW는 Agent가 선택할 수 있다. 기능 의미·범위 축소·주요 UX·경제·콘텐츠 의미·미승인 기능은 사용자 결정으로 반환한다.

## Visual Lock

시각 영향 Package에는 필수이며 Figma는 선택형 provider다.

```text
FIGMA_VISUAL_BIBLE
GITHUB_ART_BIBLE
IMMUTABLE_REFERENCE_SNAPSHOT
APPROVED_ASSET_MANIFEST
COMPOSITE
```

`Keep / Avoid / Do Not Drift`, 비율·실루엣·팔레트·재질·광원·카메라·UI 위계·아이콘/VFX·플랫폼·화면비를 잠근다. Figma 접근 불가 시 본 것으로 간주하지 않고 승인 Snapshot·Art Bible·Asset Manifest로 대체한다.

Package visual impact는 `NONE / EXISTING_LOCKED / NEW_VISUAL_REQUIRED`다. `NEW_VISUAL_REQUIRED`는 자동 구현을 중지한다.
