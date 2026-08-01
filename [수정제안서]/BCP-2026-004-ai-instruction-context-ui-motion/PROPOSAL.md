# BCP-2026-004 — 판단 중심 AI 지시·컨텍스트 큐레이션·UI 모션 원칙 통합

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base`
- 기준 커밋: `7978093e16577f1a4e2f60fbc85ebf25d906673b`
- 제출일: `2026-08-01`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 지식 상태: `패턴`
- Decision ID: `DEC-2026-08-01-001`
- 사용자 승인 근거: `https://github.com/alsdmlals4-eng/Base/issues/115`

## 관찰과 증거

사용자가 제공한 이미지·글은 `USER_SUPPLIED_SOURCE`이며 공식 제품 사실의 정본이 아니다. Base main의 운영 정본·활성 Skill·Reference·Template과 대조한 결과 다음 반복 문제가 일반화 후보로 남았다.

1. 모든 판단을 강한 규칙으로 고정하면 상황별 선택과 새 입력 대응을 방해한다.
2. 예시를 정답처럼 사용하면 예시 범위에 과적합한다.
3. 반복 규칙·장문 지시·수동 Memory 복제는 컨텍스트 비용과 정본 drift를 늘린다.
4. 현재 결정과 무관한 자료의 대량 투입은 충돌과 오판 가능성을 높인다.
5. UI 기능은 동작해도 계층·상태·간격·모션·중단·반복 피로가 설계되지 않으면 완성도가 낮다.
6. 설명만 전달하는 것보다 화면 계약·Schema·Fixture·전후 Artifact가 더 정확한 입력이 되는 작업이 있다.

Base에는 이미 자동 Trigger 라우팅, 점진적 공개, `RECOMMENDED_DEFAULT / USER_DECISION_REQUIRED`, Context Pack, Evidence 계층, UI 폴리싱, Reduced Motion, 반복·중단 검증이 존재한다. 따라서 외부 `ui-skills` 패키지를 설치하거나 새 독립 Skill을 추가하지 않고 기존 책임에 통합한다.

## 일반화 후보

### 1. 지시 권위 예산

```yaml
HARD_CONSTRAINT:
  applies_to:
    - security_and_privacy
    - permission_and_trust_boundary
    - data_integrity
    - irreversible_change
    - save_and_schema_compatibility
    - legal_and_license_boundary
  behavior: 반드시 준수하며 AI 판단 공간으로 완화하지 않는다.

RECOMMENDED_DEFAULT:
  applies_to:
    - 기술 구조
    - 파일·명명
    - 초기 시험값
    - 일반 오류 처리와 테스트
  behavior: 반례나 프로젝트 정본 충돌이 없으면 적용하고 조정 조건을 기록한다.

JUDGMENT_SPACE:
  applies_to:
    - 표현 방식
    - 정보 배치
    - 대안 구성
    - 비파괴적 초안 선택
  behavior: 정본·근거·현재 상황의 경계 안에서 AI가 판단한다.
```

강한 금지·의무 규칙을 추가하거나 유지할 때는 실제 실패를 막는지, 더 낮은 권위의 기본값과 검증으로 대체할 수 없는지 검사한다.

### 2. Interface-first Prompt

```yaml
problem:
player_or_user_value:
inputs:
required_fields:
optional_fields:
authority_and_source:
output_contract:
invariants:
failure_conditions:
validation:
```

예시는 정본이나 구현 범위를 제한하는 권위가 아니라 정상·실패·경계·회귀를 검증하는 Fixture 또는 Golden Set으로 보존한다.

### 3. 결정 질문 중심 Context 큐레이션

```yaml
decision_question:
include_criteria:
exclude_criteria:
authority_level:
freshness:
representation:
deduplication:
known_conflicts:
context_budget:
progressive_load_trigger:
refresh_trigger:
```

자료는 양이 아니라 현재 바꿀 결정과 필요한 권위 순서로 선별한다. 반대 근거·실패 사례·보호 규칙을 단순히 제거하지 않고 제외 이유와 재조회 조건을 남긴다.

### 4. Artifact-first 전달

- UI: 화면 계약·와이어프레임·대표 상태·전후 렌더
- 데이터: Schema·표·정상/실패 Fixture
- 작업 순서: 의존성·Gate·롤백이 있는 Plan
- Prompt: 입출력 계약·Eval Fixture
- 게임 기획: 대표 상황·Vertical Slice·플레이테스트 계약

Artifact는 실제 런타임·사람 이해·접근성·성능을 자동으로 증명하지 않으며 주장 상한과 `NOT_RUN`을 명시한다.

### 5. 게임 UI 모션·상호작용 원칙

```text
목적과 상태 변화
→ 첫 시선·staging
→ anticipation
→ timing·easing
→ 공간적 연속성
→ follow-through
→ 입력 즉시성
→ 중단·즉시 완료
→ 빠른 반복·재진입
→ reduced motion·mute·haptic-off
→ 성능·도메인 상태 권위 검증
```

애니메이션 원칙과 웹/SaaS 패턴을 기계적으로 복제하지 않고 Godot 게임 UI의 중심 질문·입력·상태 소유권에 맞게 변환한다.

## 프로젝트 전용으로 남길 내용

- 세계관·장르·플랫폼·세션 구조
- 실제 화면 구성·색·간격·폰트·모션 시간·easing 값
- Godot Scene·Node·Resource 경로와 구현 상태
- 프로젝트 고유 Prompt·Context Pack 전문
- 승인 아트·UI 이미지·브랜드 표현
- 저장 Schema·게임 데이터·수치·난이도·경제
- 프로젝트별 적용 Decision·Commit·검증 결과

## 적용 조건과 비사용 조건

### 적용

- L1 이상 Prompt에 반복 규칙과 예시 고착이 있다.
- Context Pack에 무관한 문서·과거 대화·중복 정본이 누적된다.
- UI 구조가 안정됐으나 모션·상태·중단·반복 계약이 부족하다.
- Schema·화면·Fixture가 설명보다 정확한 전달 수단이다.

### 비사용

- 보안·권한·개인정보·데이터 무결성·저장 호환성 경계를 느슨하게 만드는 경우
- 프로젝트 코어·중요 기획을 AI 판단 공간으로 넘기는 경우
- 검증된 Example·Golden Set을 단순 삭제하는 경우
- 외부 UI 패키지나 Tailwind/SaaS 패턴을 그대로 설치·복제하는 경우
- 실제 화면·렌더·런타임 없이 UI 완료를 주장하는 경우

## 반례와 위험

1. 규칙 과소화 → `HARD_CONSTRAINT` 완화 금지
2. 예시 제거 회귀 → Fixture로 보존
3. 큐레이션 편향 → 제외 이유·충돌·재조회 조건 필수
4. Artifact 과신 → 증거 상한과 `NOT_RUN`
5. 모션 과잉 → P0→P1→P2 후 P3, 피드백 예산과 반복 피로
6. 책임 중복 → 새 Skill 금지, Method·Reference 통합
7. BCP-2026-003 충돌 → 하나의 v9.4 후보 PR에서 독립 Task·Commit·Test로 집계

## 영향 범위와 검증

### 예상 영향

- `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`
- `skills/auditing-and-refining-ui-art/references/ui-motion-and-interaction-principles.md`
- intake·simplifying·UI audit Skill
- AI 활용 Guide·planning sequence
- Documentation Map·프로젝트 AI Workflow·UX/UI Template·UI Review Checklist
- Skill Registry·Learning Log·Changelog·generated views
- focused contract test·Skill coverage·reference freshness·Base integrity·full Python suite·`git diff --check`

### 필수 적대적 검토

- 강제 규칙이 판단 영역으로 잘못 이동했는가
- 기획 결정을 AI 기본값으로 숨겼는가
- Golden Set과 경계 사례가 사라졌는가
- 큐레이션이 반대 근거를 제거하는가
- 웹/SaaS 패턴이 Godot 공용 규칙으로 유입됐는가
- 모션 완료가 도메인 결과의 권위 시점이 됐는가
- 새 파일의 Registry·Map·Template·Test 소비자가 untouched인가
- BCP-2026-003의 모델·비용·캐싱 책임을 침범했는가

## 필요한 도구·파일·권한

- GitHub Branch·PR·Actions와 Python 검증 환경
- 현재 로컬 저장소 복제·Python 실행: 네트워크 차단으로 `NOT_RUN`
- 실제 자동 검증 근거: GitHub Actions와 PR HEAD
- 최소 권한: Base contents·issues·pull requests 쓰기

## 승인과 구현

- 제안 상태: `SUBMITTED` — 신규 제안은 제안 PR에서 이 상태로 시작한다.
- 사용자 승인 근거는 존재하지만 기계 상태 전환은 별도 구현 PR에서 수행한다.
- 구현 PR: `없음 — 제안 PR과 분리 예정`
- 구현 순서: BCP-2026-003과 BCP-2026-004를 하나의 Base v9.4 후보 구현 PR에서 독립 Task·Commit·Test로 적용하고, 그 PR에서 `APPROVED_FOR_IMPLEMENTATION`과 `approval_ref`를 기록한 뒤 evidence PR과 pin-finalization PR을 진행한다.
- 책임 경계: 모델 라우팅·비용·캐싱과 지시·컨텍스트·UI 모션의 입력·출력·검증을 합치지 않는다.
- 프로젝트 적용: Base v9.4가 검증·릴리스된 뒤 각 프로젝트의 로컬 Base 사본과 정본에 맞춰 별도 PR로 적용한다.
- 롤백: 제안 PR을 닫거나 제출 상태를 보존한 채 구현하지 않는다. 활성 Base 파일은 이 제안 PR에서 변경하지 않는다.

## Base v9.4 구현 연결

- approval_ref: `https://github.com/alsdmlals4-eng/Base/issues/115`
- implementation_pr: `https://github.com/alsdmlals4-eng/Base/pull/118`
- 상태 전환 위치: 제안 PR이 아니라 승인된 별도 Base v9.4 구현 PR
- BCP-2026-003과 BCP-2026-004는 같은 후보 PR을 사용하지만 Skill·Method·Reference·Test 책임을 분리한다.
