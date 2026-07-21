---
name: reviewing-and-validating-project-changes
description: Use when code, data, documents, assets, configuration, or external AI output must be checked against an approved work contract and verified with repository evidence before integration.
---

# Reviewing and Validating Project Changes

## Core principle

변경 주체가 사람이든 AI든 설명보다 실제 diff, 책임 원본, 실행 결과를 우선한다. 승인된 작업 계약과 관찰 가능한 증거가 일치하고, 변경된 정본이 모든 활성 소비자에 전파되기 전에는 완료로 판정하지 않는다.

## Modes

- `contract-check`: 승인 목표, 범위, 보호 대상과 실제 변경을 대조한다.
- `external-source-review`: 외부 AI·병렬 작업자의 초안과 주장을 독립 검수한다.
- `reference-freshness`: 변경된 정본·경로·ID·Schema가 활성 참조·템플릿·테스트·파생본에 전파됐는지 감사한다.
- `static-validation`: 코드·데이터·문서·자산·참조·Schema를 정적 검사한다.
- `runtime-validation`: 실행·빌드·렌더·저장·오류 경로를 실제 환경에서 확인한다.
- `regression`: 대표 정상·경계·반례·기존 기능 회귀를 확인한다.
- `evidence-report`: 통과·실패·미실행·위험·롤백을 증거와 함께 보고한다.

`reference-freshness`는 파일·경로·Skill ID·문서 ID·Schema·정책·생성기·공개 인터페이스가 추가·이동·통합·삭제·교체되었거나, 영향 파일 누락 가능성이 있는 모든 변경에서 실행한다. 전문 절차는 `auditing-canonical-reference-freshness`를 호출한다.

## Required inputs

```yaml
approved_work_contract:
baseline_branch_and_commit:
changed_files_or_diff:
current_responsibility_sources:
canonical_sources_and_consumers:
known_renames_aliases_and_replacements:
allowed_and_protected_scope:
acceptance_criteria:
validation_commands_and_tools:
runtime_or_capture_targets:
rollback_path:
change_producer:
```

## Review order

```text
작업 계약·범위
→ 현행 책임 원본
→ 실제 diff·참조 영향
→ 필요 시 reference-freshness
→ 데이터·저장·호환성
→ 정적 검사
→ 런타임·렌더·빌드
→ 대표·경계·반례·회귀
→ 증거 보고·최소 수정·롤백
```

## Process

### 1. Contract check

1. 요청한 문제·산출물·완료 기준을 재진술한다.
2. 변경 파일을 `필수 / 허용 / 범위 밖`으로 분류한다.
3. 사용자 기존 변경과 승인되지 않은 구조 변경을 찾는다.
4. 삭제·이동·이름 변경은 모든 참조와 대체 경로를 확인한다.

### 2. Source review

1. 새 책임 원본을 만들기 전에 같은 책임의 현행 원본이 있는지 찾는다.
2. 구현 사실, 외부 근거, 추정, 제안을 분리한다.
3. 외부 설명보다 실제 파일·diff·명령 결과를 우선한다.
4. 확인할 수 없는 경로·명령·함수·필드를 승인하지 않는다.

### 3. Reference freshness

다음 중 하나라도 해당하면 `auditing-canonical-reference-freshness`를 호출한다.

- 파일·폴더·Skill ID·문서 ID·Schema·명령·공개 인터페이스를 변경했다.
- Registry·Documentation Map·START_HERE·AGENTS·운영 모델·템플릿을 변경했다.
- 통합·삭제·마이그레이션·발행 정책·생성기 변경이 있다.
- 하나의 정본 변경이 여러 소비자·테스트·Workflow·파생본에 영향을 줄 수 있다.

검사 결과에서 활성 파일의 오래된 참조, untouched 소비자, 허용된 Legacy·Change Log·과거 case, 정책·상태 drift, PDF·Manifest·해시 불일치를 구분한다.

Base 자동 검사:

```text
python tools/check_canonical_reference_freshness.py \
  --config .github/reference-freshness.json \
  --base <base-sha> --head <head-sha>
```

### 4. Static validation

- 코드: 호출 관계, 타입, 오류 처리, 공개 인터페이스.
- 데이터: ID, Schema, 기본값, 마이그레이션, 저장 호환성.
- 문서: 책임 중복, 경로, 상태, 명령, 구현과의 일치.
- 자산: 참조 경로, import 설정, 형식, 승인 상태.
- 구성: 플랫폼별 경로, 환경 변수, 잠금 파일, CI와 로컬 차이.

### 5. Runtime validation

- 가능한 경우 사용자가 실제로 겪는 시작점에서 증상을 재현한다.
- 빌드·실행·렌더·저장·불러오기·오류 경로를 확인한다.
- UI 전문 감사가 필요하면 `auditing-and-refining-ui-art`를 별도 호출한다.
- 필요한 실행 환경이 없으면 통과 처리하지 않고 미실행 사유와 확인 방법을 기록한다.

### 6. Regression

1. 대표 정상 경로.
2. 최소·최대·빈 값·누락 입력 같은 경계 경로.
3. 원래 실패를 재현하는 반례.
4. 변경과 인접한 기존 기능.
5. 실패 후 복구·롤백 경로.
6. 최신 정본과 이전 참조가 다시 공존하지 않는지 확인한다.

### 7. Decision

- `ACCEPT`: 계약과 검증을 충족하고 참조 최신성 누락이 없다.
- `ACCEPT_WITH_FOLLOWUP`: 핵심 기준은 통과했지만 비차단 후속 작업이 있다.
- `REVISE`: 수정 뒤 같은 검증을 다시 실행해야 한다.
- `REJECT`: 범위·사실·호환성·정본 계약 위반으로 폐기한다.
- `UNVERIFIED`: 필요한 환경·입력이 없어 완료 판정할 수 없다.

## Output contract

```md
# 프로젝트 변경 검증
## 판정
## 승인된 목표·범위와 실제 diff
## 확인한 책임 원본·파일
## 정본·참조 최신성·변경 전파
## 정적 검사
## 런타임·렌더·빌드 검증
## 대표·경계·반례·회귀 결과
## 외부 산출물 독립 검수
## 실패·미실행·남은 위험
## 필요한 최소 수정
## 롤백·복구
## 증거 경로·명령·캡처
```

## Definition of Done

- 승인된 계약과 실제 변경 범위를 대조했다.
- 변경된 책임과 참조 경로를 확인했다.
- 정본·경로·ID·Schema 변경이 있으면 영향 지도와 reference freshness 결과가 있다.
- 변경됐어야 하지만 untouched인 파일의 갱신 필요 여부를 판정했다.
- 가능한 정적·런타임·회귀 검증을 실제 실행했다.
- 실행하지 못한 검증을 성공으로 표시하지 않았다.
- 판정과 증거, 남은 위험, 롤백을 연결했다.
- 외부 산출물은 독립 검수 없이 정본에 반영하지 않았다.

## Failure conditions

- 실제 파일을 읽지 않고 완료를 주장한다.
- 원래 증상을 재현하지 못한 테스트만으로 수정 완료를 주장한다.
- 사용자 승인 없이 범위 밖 구조 변경·삭제·마이그레이션을 수행한다.
- 테스트 없이 저장 형식·공개 인터페이스를 바꾼다.
- 확인할 수 없는 경로·명령·함수·데이터 필드·실행 결과를 만든다.
- 기존 사용자 변경을 덮어쓴다.
- 새 정본 파일만 확인하고 이전 참조·untouched 소비자·파생본을 검사하지 않는다.
- Git 이력·Change Log·Alias의 역사 참조를 활성 stale reference와 구분하지 않는다.

## Related skills

- `auditing-canonical-reference-freshness`: 정본 영향 지도, 오래된 참조, content drift, 파생본 최신성과 변경 전파 누락을 전문 감사한다.
- `managing-design-documents`: 등록된 문서 정본과 정책별 발행·Manifest 검증을 담당한다.
- `managing-game-project-operating-system`: 시작 문서·Registry·Skill·자동화·콜드 스타트 전체 연결을 검증한다.
- `auditing-and-refining-ui-art`: 실제 Godot·Web UI 렌더의 전문 시각 감사를 담당한다.

## Legacy mode mapping

- `reviewing-external-ai-drafts` → `external-source-review`, `static-validation`, `regression`, `evidence-report`

Templates:

- `templates/quality/PROJECT_CHANGE_VALIDATION.md`
- `templates/quality/CANONICAL_REFERENCE_FRESHNESS_AUDIT.md`
- `templates/ai/EXTERNAL_AI_DRAFT_REVIEW.md` (legacy-compatible input)
