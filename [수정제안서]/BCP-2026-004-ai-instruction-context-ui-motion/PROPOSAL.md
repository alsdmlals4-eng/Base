# BCP-2026-004 — 판단 중심 AI 지시·컨텍스트 큐레이션·UI 모션 원칙 통합

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base`
- 기준 커밋: `a82976a3a42450ea413cdc5d4aebf701678110d8`
- 제출일: `2026-08-01`
- 상태: `SUBMITTED`
- 지식 상태: `패턴`
- Decision ID: `DEC-2026-08-01-001`

## 관찰과 증거

사용자가 제공한 UI Skill 소개와 AI 지시문 간소화 자료에서 다음 반복 문제가 확인됐다.

1. 모든 판단을 강한 규칙으로 고정하면 최신 모델의 상황 판단을 방해한다.
2. 예시를 정답처럼 붙이면 모델이 예시 범위를 벗어나지 못하고 새로운 입력에 과적합한다.
3. 긴 지시문·반복 규칙·수동 Memory 복제는 컨텍스트 비용과 정본 drift를 늘린다.
4. 관련 없는 자료를 대량 투입하면 AI가 다루는 정보량과 충돌이 늘어난다.
5. UI를 기능적으로 만들 수 있어도 간격·계층·상태·모션·중단·반복 피로에서 완성도가 떨어질 수 있다.
6. 설명만으로 원하는 결과를 전달하는 것보다 실제 화면 계약·Schema·Fixture·전후 Artifact가 더 정확한 입력이 된다.

Base main에는 이미 자동 Trigger 라우팅, 점진적 공개, `RECOMMENDED_DEFAULT / USER_DECISION_REQUIRED`, Context Pack, Evidence 계층, UI 폴리싱, Reduced Motion, 반복·중단 검증이 존재한다. 따라서 외부 `ui-skills` 패키지를 도입하거나 새 독립 Skill을 추가하는 방식은 중복 책임을 만든다.

확인한 주요 책임 원본:

- `docs/OPERATING_MODEL.md`
- `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- `docs/CONFIRMED_DECISION_SYNC_POLICY.md`
- `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md`
- `docs/AI_SKILL_ADOPTION_GUIDE.md`
- `docs/knowledge/game-development/AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md`
- `skills/managing-project-intake-and-work-contract/SKILL.md`
- `skills/simplifying-skill-bodies/SKILL.md`
- `skills/auditing-and-refining-ui-art/SKILL.md`
- `skills/running-adversarial-review-and-refinement/SKILL.md`

## 일반화 후보

### 1. 지시 권위 예산

지시를 다음 세 단계로 분류한다.

```yaml
HARD_CONSTRAINT:
  applies_to:
    - security_and_privacy
    - permission_and_trust_boundary
    - data_integrity
    - irreversible_change
    - save_and_schema_compatibility
    - legal_and_license_boundary
  behavior: 반드시 준수하며 판단 공간으로 완화하지 않는다.

RECOMMENDED_DEFAULT:
  applies_to:
    - 기술 구조
    - 파일·명명
    - 초기 시험값
    - 일반적인 오류 처리와 테스트
  behavior: 반례나 프로젝트 정본 충돌이 없으면 사용하고 조정 조건을 남긴다.

JUDGMENT_SPACE:
  applies_to:
    - 표현 방식
    - 정보 배치
    - 대안 구성
    - 비파괴적 초안 선택
  behavior: 정본·근거·현재 상황 안에서 AI가 판단한다.
```

강한 금지·의무 규칙을 추가하거나 유지할 때는 실제 실패를 막는지, 더 낮은 권위의 기본값이나 검증으로 대체할 수 없는지 먼저 검사한다.

### 2. Interface-first Prompt

예시보다 먼저 다음을 정의한다.

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

예시는 정본이나 구현 범위를 제한하는 권위가 아니라 정상·실패·경계·회귀를 검증하는 Fixture 또는 Golden Set으로 취급한다.

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

자료는 많은 순서가 아니라 현재 바꿀 결정과 필요한 권위 순서로 선별한다. 반대 근거·실패 사례·보호 규칙을 관련 없다는 이유로 제거하지 않는다.

### 4. Artifact-first 전달

작업 유형에 맞는 검증 가능한 결과를 우선한다.

- UI: 화면 계약·와이어프레임·대표 상태·전후 렌더
- 데이터: Schema·표·정상/실패 Fixture
- 작업 순서: 의존성·Gate·롤백이 있는 Plan
- Prompt: 입출력 계약·Eval Fixture
- 게임 기획: 대표 상황·Vertical Slice·플레이테스트 계약

Artifact는 실제 런타임·사람 이해·접근성·성능을 자동으로 증명하지 않으며, 증거 상한을 명시한다.

### 5. 게임 UI 모션·상호작용 원칙

모션은 장식이 아니라 상태 변화·원인·공간 관계·입력 접수·결과를 설명해야 한다.

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

디즈니 애니메이션 12원칙이나 웹/SaaS 패턴을 기계적으로 복제하지 않고 Godot 게임 UI와 플레이어 중심 질문에 맞게 변환한다.

## 프로젝트 전용으로 남길 내용

- 프로젝트별 세계관·장르·플랫폼·세션 구조
- 실제 화면 구성·색·간격·폰트·모션 시간·easing 값
- Godot Scene·Node·Resource 경로와 구현 상태
- 프로젝트 고유 Prompt 전문과 Context Pack 내용
- 승인 아트·UI 이미지·상징 캐릭터·브랜드 표현
- 저장 Schema·게임 데이터·수치·난이도·경제
- 각 프로젝트의 적용 Decision ID·Commit·검증 결과

## 적용 조건과 비사용 조건

### 적용 조건

- L1 이상 AI 작업 계약이나 Prompt가 과도하게 길고 반복 규칙이 많다.
- 예시가 입력·출력 계약보다 강한 권위로 사용된다.
- Context Pack에 관련 없는 문서·과거 대화·중복 정본이 누적된다.
- UI 정보 구조가 안정됐으나 모션·상태·중단·반복 완성도 계약이 부족하다.
- 설명만으로 정확한 결과 전달이 어렵고 Schema·화면·Fixture가 더 적합하다.

### 비사용 조건

- 보안·권한·개인정보·데이터 무결성·저장 호환성 같은 강제 경계를 느슨하게 만들려는 경우
- 프로젝트 코어·중요 기획을 AI 판단 공간으로 넘기려는 경우
- 기존 검증된 Example·Golden Set을 단순 삭제하려는 경우
- 외부 UI Skill 패키지나 Tailwind/SaaS 패턴을 그대로 설치·복제하려는 경우
- 실제 화면·렌더·런타임 없이 미감 완료를 주장하려는 경우

## 반례와 위험

1. **규칙 과소화**: 강한 규칙을 제거해 권한·데이터·호환성 사고가 발생할 수 있다.
   - 대응: `HARD_CONSTRAINT` allowlist와 완화 금지 Gate를 둔다.
2. **예시 제거 회귀**: 예시를 없애 경계 사례와 품질 기준이 사라질 수 있다.
   - 대응: 예시는 Fixture로 보존하고 인터페이스 뒤에 배치한다.
3. **큐레이션 편향**: 자료 선별이 반대 증거·실패 사례를 제거할 수 있다.
   - 대응: 제외 이유·알려진 충돌·재조회 조건을 필수화한다.
4. **Artifact 과신**: 이미지·Schema·문서가 실제 플레이를 증명한다고 오판할 수 있다.
   - 대응: 각 Artifact의 주장 상한과 `NOT_RUN`을 기록한다.
5. **모션 과잉**: 완성도를 이유로 모든 UI에 확대·흔들림·사운드가 추가될 수 있다.
   - 대응: P0→P1→P2 이후 P3, 피드백 예산, 반복 피로, Reduced Motion을 적용한다.
6. **책임 중복**: 새 Skill이 intake·simplification·UI Skill과 중복될 수 있다.
   - 대응: 새 활성 Skill을 만들지 않고 Method·Reference로 통합한다.
7. **열린 v9.4 작업 충돌**: Issue #113 / PR #114와 Registry·Release 계약이 충돌할 수 있다.
   - 대응: 제안 PR을 먼저 분리하고 구현은 최신 main에서 재기준화한다. 모델 라우팅·비용·caching 책임을 수정하지 않는다.

## 영향 범위와 검증

### 예상 영향

- 신규 Method: `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`
- 신규 UI Reference: `skills/auditing-and-refining-ui-art/references/ui-motion-and-interaction-principles.md`
- 기존 Skill: intake, simplifying, UI audit
- Guide·Policy: AI 활용 Guide, planning sequence
- 소비자: Documentation Map, 프로젝트 AI Workflow, UX/UI Template, UI Review Checklist
- 기계 권위·학습: Skill Registry, Learning Log, Changelog, generated views
- 검증: focused contract test, Skill coverage, reference freshness, Base integrity, full Python suite, `git diff --check`

### 필수 적대적 검토

- 강제 규칙이 판단 영역으로 잘못 이동했는가
- 프로젝트 기획 결정을 AI 기본값으로 숨겼는가
- 예시를 삭제해 Golden Set과 경계 사례가 사라졌는가
- Context 큐레이션이 반대 근거를 제거하는가
- 웹/SaaS 패턴이 Godot 게임 UI 공용 규칙으로 유입됐는가
- 모션이 도메인 결과의 권위 시점이 됐는가
- 새 파일은 존재하지만 Registry·Map·Template·Test 소비자가 untouched인가
- Issue #113 / PR #114의 활성 범위를 침범했는가

## 필요한 도구·파일·권한

- 필요 항목: GitHub 저장소 읽기·브랜치·파일·PR·Actions 권한
- 필요한 이유: 제안과 구현 PR 분리, 정본·Registry·Test 동기화, CI 검증
- 설치·적용 방법: GitHub 커넥터를 사용해 별도 Branch·PR에서 수행
- 설치 후 확인 명령: GitHub Actions의 필수 검사와 PR HEAD 상태 확인
- 최소 권한: Base 저장소의 branch push·PR create·review·merge 권한
- 로컬 저장소·Python 실행: 현재 환경의 네트워크 차단으로 `NOT_RUN`; GitHub Actions가 실행 증거를 소유한다.

## 승인과 구현

- 사용자 승인 근거: `https://github.com/alsdmlals4-eng/Base/issues/115`
- 승인 발화: `권장안대로 진행해`
- 구현 PR: `없음` — 제안 PR 병합 후 별도 생성
- 롤백: 제안 단계에서는 이 PR을 닫거나 revert하며 활성 Skill·Registry·Release 파일을 변경하지 않는다.
