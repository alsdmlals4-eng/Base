# 승인 결정 즉시 동기화 정책

이 문서는 Base와 Base를 적용한 프로젝트에서 기획·Grill Me·검수 중 확정된 결정을 누락 없이 복원하고, 같은 질문 반복·정본 drift·PR 누적을 막기 위한 공용 정본이다.

GitHub 객체의 생명주기는 `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md`, Work Mode와 Skill 라우팅은 `docs/WORK_MODE_AND_SKILL_ROUTING.md`, 문서 책임 원본과 발행은 `skills/managing-design-documents/SKILL.md`, 실제 변경 검증은 `skills/reviewing-and-validating-project-changes/SKILL.md`가 계속 책임진다. 프로젝트 workspace의 현재 권위는 `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`, 사람용 파생 PDF·legacy migration 경계는 `docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md`가 책임진다.

## 1. 목표

- 질문 전에 기존 승인 사항과 현재 구현을 확인해 같은 결정을 다시 묻지 않는다.
- 사용자에게는 프로젝트 코어·중요 기획·방향성·정본 충돌만 결정 요청한다.
- 승인된 결정은 같은 승인 단위에서 **repository primary canon**에 반영하고, 사람이 볼 필요가 있으면 exact-SHA PDF 파생본으로 발행한다.
- 장시간 인터뷰가 중단돼도 `CURRENT_CONFIRMED_DECISIONS.md`와 repository owner·파생 PDF 정보로 현재 승인 상태와 사람용 전체 그림을 복원한다.
- 구현 PR은 하나의 Goal에 하나만 유지하고 검증 완료 뒤 병합하거나, 병합 불가/폐기/참조 전용이면 이유를 기록하고 닫는다.
- 모든 병합 뒤 적대적 검토로 최근 승인 누락·정본 충돌·파생물 drift·회귀를 재검사한다.

## 2. 책임과 우선순위

### 2.1 V4 `REPOSITORY_PRIMARY_CANON`

```text
REPOSITORY_PRIMARY_CANON
→ Project Home에 해당하는 current planning / decision / visual / Flow Map / Storyboard / Asset catalog / Reference·Benchmark
→ Budget / Tier / Roster / Economy / Progression 등 현행 사람이 비교·학습·수정하는 표
→ Markdown / JSON / game data / code / scene / resource / config / tests

REPOSITORY_RUNTIME_TRUTH
→ 실제 구현·build·runtime·QA evidence

APPROVED_HUMAN_BLUEPRINT_PDF_CANON
→ exact source SHA와 evidence ceiling을 명시하고 사용자 승인·manifest 등록을 마친 불변 사람용 시각·검수 정본
```

repository는 기획·시각·구조화·구현 도메인의 현행 정본이며, 사람용 이해에는 정확한 source SHA의 PDF 또는 프로젝트가 정한 repository-native 문서를 사용한다. 파생 PDF와 static mockup은 runtime proof가 아니다.

Notion은 V4 exception 또는 legacy migration의 고유 자료 확인에만 쓴다. 그러한 source에서 얻은 내용이 규칙·데이터·구현 동작을 바꾸면 `PROPOSED_LEGACY_CHANGE`로 시작하고, `SYNC_BEFORE_IMPLEMENTATION`에 따라 repository owner를 동기화하기 전에는 구현·runtime 변경에 사용하지 않는다.

Google Sheets는 `COMPATIBILITY_ONLY` migration source다. 기존 unique material이 남은 프로젝트에서만 읽으며 새 기본 GDD workspace나 동기화 완료 조건으로 사용하지 않는다.

### 2.2 책임 surface

| Surface | 책임 | 정본 여부 |
|---|---|---|
| 최신 사용자 지시 | 현재 요청과 승인 원문 | 최우선 요구 권한 |
| GitHub Issue·PR 댓글 | 질문, 사용자 답변, 승인 시점, 검토 대화의 추적 증거 | 최종 정본 아님 |
| `CURRENT_CONFIRMED_DECISIONS.md` | 현재 승인 결정의 요약, 대체 관계, 반영 위치, 동기화 상태 | 승인 결정 복원 정본 |
| 등록된 repository 분야 문서·JSON·asset catalog | 시스템·서사·아트·UI·Flow/Wireframe 등 현행 상세 규칙과 예외 | `REPOSITORY_PRIMARY_CANON` |
| exact-SHA PDF | 사용자가 승인한 milestone 시각·검수 baseline | 승인·manifest 등록 후 `APPROVED_HUMAN_BLUEPRINT_PDF_CANON` |
| 프로젝트 Notion | 실제 V4 exception/legacy migration의 보조 source | 정본 아님 |
| `ACTIVE_CONTEXT.md` | 현재 단계·작업·위험·다음 행동 | 현재 상태 원본 |
| GitHub `main` | 반영된 structured 문서·코드·데이터·자산의 저장소 상태 | 통합 structured/runtime 상태 |
| Google Sheets | unique legacy material의 이관 입력 | `COMPATIBILITY_ONLY` |
| 과거 PR·Commit | 검토·변경·롤백 이력 | 과거 증거 |

`CURRENT_CONFIRMED_DECISIONS.md`는 상세 기획서를 장문 복제하지 않는다. 결정의 핵심, 보호 범위, 대체 관계, repository 상세 책임 원본과 파생 PDF/실제 exception 반영 위치를 기록한다.

### 2.3 충돌 우선순위

```text
최신 사용자 승인
→ 프로젝트 AGENTS·보안·엔진·데이터 규칙
→ CURRENT_CONFIRMED_DECISIONS.md의 현재 Decision
→ V4 repository active owner
   - 사람용 전체 그림·Visual·예산·Tier·Flow/Storyboard·Markdown·JSON·game data·code·scene·resource·test → repository
   - 사람용 milestone snapshot → exact-SHA PDF 파생본
→ ACTIVE_CONTEXT·승인된 작업 계약
→ 실제 repository runtime truth
→ 프로젝트에 동기화된 Base 기준
→ 외부 근거·과거 대화·추정
```

실제 구현과 승인 정본이 다르면 어느 한쪽을 자동으로 진실로 간주하지 않는다. 구현 누락인지 정본 미갱신인지 판정하고 `CANON_CONFLICT`로 보고한다.

## 3. 새 채팅·새 작업 시작 입력

가능하면 다음을 확인한다.

```text
Base repository URL
Project name and GitHub repository URL
필요한 exact-SHA PDF 또는 실제 V4 exception/migration source
현재 요청
```

링크가 이미 대화·Project Registry·프로젝트 정본에 있으면 다시 묻지 않는다. 연결된 GitHub/Notion으로 확인 가능한 정보도 사용자에게 되묻지 않는다.

Google Sheets는 compatibility migration이 실제 범위에 포함될 때만 추가 입력으로 본다.

## 4. 모든 L1 이상 작업의 사전 대조

새 질문·기획·검수·구현 계획 전에 다음 순서로 확인한다.

```text
프로젝트 GitHub main 최신 HEAD
→ 동일 Goal의 열린 Issue·PR·Branch
→ 최근 병합 PR과 후속·대체 링크
→ 프로젝트 AGENTS·START_HERE·ACTIVE_CONTEXT
→ CURRENT_CONFIRMED_DECISIONS.md
→ 관련 repository 분야 책임 원본 / 실제 code·data·Scene·Resource·test
→ repository 분야 owner와 필요한 exact-SHA PDF
→ 실제 V4 exception/migration source가 있으면 targeted readback
→ Decision ID·Commit SHA·publication/exception readback 비교
→ 필요 시 compatibility Sheet의 unique material만 확인
→ 중복·충돌·미반영·미검증 판정
→ 작업 시작
```

판정 상태:

```text
CANON_MATCH
CANON_CONFLICT
DERIVED_VIEW_OUTDATED
REPOSITORY_OUTDATED
OPEN_PR_EXISTS
DUPLICATE_WORK
DUPLICATE_QUESTION
MISSING_DECISION_SYNC
PROPOSED_LEGACY_CHANGE
BLOCKED_UNVERIFIED
```

`CANON_CONFLICT`, `DUPLICATE_WORK`, `DUPLICATE_QUESTION`, `MISSING_DECISION_SYNC`가 발견되면 새 질문이나 새 PR보다 기존 상태 복원을 먼저 수행한다.

## 5. 중복 질문 방지

질문 문구가 달라도 결정 대상과 결과가 같으면 중복 질문이다.

다음은 다시 묻지 않는다.

- 이미 `CURRENT`인 Decision과 동일한 방향 선택
- 이전 승인안을 표현만 바꾼 선택지
- `SUPERSEDED` 또는 `REJECTED`된 안을 새 안처럼 제시하는 질문
- repository와 Notion 중 한쪽 표시가 늦다는 이유로 같은 결정을 재질문하는 경우
- 현재 대화에 없다는 이유만으로 정본에 있는 결정을 재질문하는 경우
- 단계 이름만 달라지고 실제 프로젝트 영향이 같은 질문

기존 결정이 있으면 다음처럼 처리한다.

```text
기존 Decision ID 확인
→ 현재 전제가 유지되는지 검사
→ 유효하면 질문 없이 적용
→ 달라진 사실만 비교
→ 프로젝트 방향을 바꾸는 충돌일 때만 재결정 요청
```

재결정 질문에는 기존 Decision ID, 승인일, 기존 결정, 새 사실, 충돌, 유지·변경 영향, GPT 권장안을 포함한다.

## 6. 사용자 질문과 권장 기본값 분리

### 6.1 `RECOMMENDED_DEFAULT`

프로젝트 방향을 바꾸지 않고 최소 안전안이 정본·기술 표준·테스트로 결정되는 사항은 사용자에게 묻지 않는다.

예:

- 파일·폴더·함수·클래스 명명과 분리
- 일반적인 Godot 노드 구성과 내부 데이터 구조
- 오류 처리·로그·테스트 구성
- 임시 디버그 설정
- UI 여백·정렬의 초기값
- 입력 버퍼·전환 시간·쿨다운의 초기 시험값
- 플레이테스트 전 밸런스 초깃값
- 기존 정본을 그대로 구현하기 위한 기술 선택
- 명백한 참조 누락·테스트 실패·표준 위반 수정

기록 형식:

```yaml
classification: RECOMMENDED_DEFAULT
selected_value:
reason:
canonical_impact: NONE | TECHNICAL_ONLY
adjustment_condition:
validation:
```

### 6.2 `USER_DECISION_REQUIRED`

다음은 사용자와 논의한다.

- 프로젝트 코어·플레이어 판타지·Core Loop 변경
- 장르·플랫폼·타깃·세션 구조 변경
- 중요 시스템 추가·삭제·우선순위 변경
- 주요 UI·UX·아트 방향·서사 의미 변경
- 기존 승인 결정 폐기·대체
- 분야 책임 원본끼리의 기획 충돌
- 범위·비용·출시·사업 방향의 큰 변경
- 되돌리기 어렵거나 다른 시스템에 광범위한 영향을 주는 결정

수치도 난이도, 경제, 성장 속도, 세션 길이, 빌드 우열, 보상 체감, 선택 의미를 근본적으로 바꾸면 기획 결정이다.

## 7. 질문 기록

질문은 하나의 활성 GitHub 추적 surface에 댓글로 남긴다. 같은 인터뷰·Goal에서는 새 PR을 만들지 않고 기존 Issue 또는 PR conversation을 재사용한다. 활성 surface가 없다면 프로젝트 운영 규칙에 따라 계획 Issue 하나를 만든다.

```markdown
## 질문 — DEC-YYYY-MM-DD-NNN

- Work Mode:
- 분야:
- 기존 Decision ID:
- 확인한 repository 정본:
- 확인한 exact-SHA derived view 또는 실제 V4 exception/migration source:
- main HEAD:
- 관련 열린 PR:
- 최근 병합 PR:
- derived view / exception readback 상태:
- 질문:
- 선택지:
- GPT 권장안:
- 프로젝트 영향:
- 상태: AWAITING_USER_DECISION
```

질문은 한 번에 하나의 중요 결정만 포함한다.

## 8. 승인 즉시 동기화

사용자 답변 직후 다음을 같은 승인 단위에서 완료한다.

```text
사용자 답변 원문 보존
→ 기존 댓글 흐름에 승인 결과 기록
→ Decision 상태 판정
→ CURRENT_CONFIRMED_DECISIONS.md 갱신
→ 영향받는 repository 분야 책임 원본 / structured data / Flow·Wireframe 갱신
→ 필요한 ACTIVE_CONTEXT·작업 계약 갱신
→ 승인 PR exact-head 검토·required checks·squash merge
→ main Commit SHA 재조회
→ 사람이 봐야 하는 변화면 exact-SHA derived PDF 발행 또는 repository-native view 갱신
→ 실제 V4 exception/migration write가 있었다면 destination readback
→ Decision ID·Commit·approved PDF canon/exception 표현·대체 관계 비교
→ SYNCED 판정
→ 다음 질문
```

승인 결과 댓글:

```markdown
## 승인 결과 — DEC-YYYY-MM-DD-NNN

- 사용자 답변:
- 최종 결정:
- 상태: CONFIRMED | LATEST_OVERRIDE | SUPERSEDED | REJECTED | DEFERRED
- 대체되는 Decision:
- 영향받는 repository 책임 원본:
- human derived view 또는 V4 exception/migration 반영 위치:
- main Commit:
- derived view / exception last readback:
- 동기화 판정: SYNCED | PROPOSED_LEGACY_CHANGE | SYNC_FAILED | BLOCKED_UNVERIFIED
```

### 8.1 V4 exception 또는 legacy migration 처리

Notion은 새 프로젝트의 기본 workspace나 active decision-sync mirror가 아니다. 프로젝트 `AGENTS.md`가 실제 exception을 승인했거나 unique legacy material을 이관해야 할 때만 scoped source로 읽고 수정할 수 있다.

```text
PROPOSED_LEGACY_CHANGE
→ 기존 Decision·latest main·repository 분야 정본·실제 구현과 비교
→ 단순 presentation-only 변경인지 의미/규칙 변경인지 판정
→ 승인된 exception presentation-only면 Notion에서 반영·readback
→ 의미/규칙 변경이면 Decision 상태 갱신
→ repository primary owner 갱신
→ main Commit SHA 기록
→ 필요한 구현은 그 이후 별도 TDD/PR
→ exception readback과 repository cross-check
→ SYNCED
```

Notion의 표나 그림을 machine data로 직접 소비해 repository primary owner를 우회하지 않는다.

### 8.2 보호된 `main` 반영

보호된 `main`에서는 승인 기록을 포함해 direct push를 하지 않는다. 다음 변경도 branch → PR → exact-head checks/review → squash merge → main readback을 따른다.

- `CURRENT_CONFIRMED_DECISIONS.md`
- 승인된 기획 책임 원본의 해당 Section
- `ACTIVE_CONTEXT.md`의 현재 결정 요약
- Decision 상태·Registry의 해당 메타데이터

PR 안에서 승인 한 건당 논리 Commit 하나를 기본값으로 하되, `main`의 최종 이력은 repository rule이 요구하는 squash commit이다.

### 8.3 반드시 구현 PR을 사용하는 범위

- Godot·Web 런타임 코드
- Scene·Resource·게임 데이터 Schema
- 저장 호환성·마이그레이션
- GitHub Actions·Ruleset·자동화
- 대규모 파일 이동·삭제·재구조화
- Base 공용 정책·Skill·Template 변경
- 독립 검증·롤백이 필요한 자산 교체

승인 문서/파생물·exception 반영과 실제 구현 완료를 혼동하지 않는다.

## 9. Google Sheets compatibility migration

Google Sheets는 `COMPATIBILITY_ONLY`다.

- Base 저장소 자체는 Sheet 동기화 대상이 아니다.
- 새 프로젝트의 기본 GDD workspace로 요구하지 않는다.
- 기존 Sheet에 unique material이 남아 있는 경우에만 source ID·tab·row를 읽는다.
- `UNIQUE / DUPLICATE / OBSOLETE`를 분류해 repository의 올바른 destination으로 이관한다. Notion destination은 실제 V4 exception일 때만 추가한다.
- 이관 뒤 destination readback을 수행한다.
- Sheet-only 수정은 자동 canon 승격하지 않는다.
- 이관 완료 뒤 Sheet가 오래됐다는 이유만으로 프로젝트를 `SYNC_FAILED`로 만들지 않는다.

## 10. 동기화 상태

```text
QUESTION_RECORDED
AWAITING_USER_DECISION
APPROVED_PENDING_CANON
CANON_UPDATED
MAIN_UPDATED
DERIVED_VIEW_UPDATED
EXCEPTION_MIGRATION_UPDATED
PROPOSED_LEGACY_CHANGE
SYNCED
SYNC_FAILED
SUPERSEDED
BLOCKED_UNVERIFIED
```

`SHEET_UPDATED`와 `NOTION_UPDATED`는 과거 workspace 동기화의 **legacy compatibility audit token**이다. 현재 정상 상태 전이는 `DERIVED_VIEW_UPDATED` 또는 실제 필요한 `EXCEPTION_MIGRATION_UPDATED`를 사용하며, legacy token을 새 프로젝트의 active 상태로 사용하지 않는다.

정상 종료는 repository primary owner와 필요한 approved PDF canon/exception readback이 일치한 `SYNCED`다.

- repository 쓰기 실패: 기존 댓글에 실패와 재개 조건을 기록한다.
- derived view 또는 exception write/readback 실패: repository 정본은 유지하고 `SYNC_FAILED`와 재발행/재동기화 대상 Decision ID를 기록한다.
- exception/legacy meaning change가 repository owner에 미반영: `PROPOSED_LEGACY_CHANGE` 또는 `REPOSITORY_OUTDATED`.
- 권한·연결·target을 확인할 수 없음: `BLOCKED_UNVERIFIED`.
- `SYNCED`가 아닌 승인 건이 있으면 다음 비차단 질문을 계속 늘리지 않는다.

## 11. PR 중복과 누적 방지

새 PR 전에 다음을 확인한다.

```text
원본 Issue·승인된 Goal
→ 같은 Goal의 열린 PR
→ 같은 작업 Branch
→ 최근 병합 PR
→ 대체·후속 PR
→ 새 PR 필요 여부
```

- 하나의 Goal에는 하나의 활성 PR을 기본값으로 사용한다.
- 리뷰 지적, 테스트 실패, 같은 범위의 문구·데이터·설정 보완은 기존 PR에서 이어간다.
- 승인 결정 sync도 보호된 main에서는 PR을 통해 반영한다.
- 구현 PR은 검증·승인 Gate를 충족하면 Squash merge한다.
- merge-complete가 아니거나 `DO_NOT_MERGE`/history/reference-only인 PR은 main에 억지로 넣지 않고, 후속 owner가 보존되면 이유를 기록해 닫을 수 있다.
- 병합되거나 닫힌 PR conversation은 장기 검토 증거로 보존한다.
- branch 삭제는 repository 설정/도구가 실제 지원하고 안전 조건을 만족할 때만 수행한다.

## 12. 병합 후 적대적 검토

모든 PR 병합과 직접 `main` Decision Commit 뒤 다음을 실행한다.

```text
새 main HEAD 고정
→ 병합 PR·Commit diff 확인
→ CURRENT_CONFIRMED_DECISIONS.md 비교
→ 관련 repository 분야 책임 원본 비교
→ 최근 승인 Decision ID 비교
→ 필요한 exact-SHA derived PDF/repository-native view 또는 실제 exception record 비교
→ attack
→ validate-critique
→ reference freshness·정적·가능한 runtime·회귀 검사
→ finding 분류
→ 필요한 최소 수정
→ regression-recheck
→ 필요한 approved PDF canon/exception readback
→ 최종 충돌 보고
```

필수 공격 항목:

- 최근 승인 사항이 빠졌는가
- 이전에 대체된 결정이 다시 살아났는가
- 프로젝트 코어·플레이어 약속과 충돌하는가
- repository 분야 원본 일부만 갱신됐는가
- 사람이 보는 derived PDF/repository-native view 또는 실제 exception record가 현재 Decision과 다른가
- 실제 diff가 승인 범위를 벗어났는가
- 같은 기능·문서·질문이 중복됐는가
- 관련 테스트·템플릿·참조가 untouched로 남았는가
- 기존 정상 경로가 회귀했는가
- 임시값·플레이스홀더를 확정값으로 승격했는가

최종 판정:

```text
NO_CONFLICT
CONFLICT_FIXED
USER_DECISION_REQUIRED
BLOCKED_UNVERIFIED
```

## 13. 병합 후 보고

```markdown
## 병합 후 적대적 검토 결과

### 병합 정보
- 작업:
- PR 또는 직접 Commit:
- 새 main HEAD:
- 관련 Decision ID:
- head branch 처리:

### 정본·동기화 비교
- CURRENT_CONFIRMED_DECISIONS:
- repository 분야 책임 원본:
- human derived view / exception source:
- 최근 승인 누락:
- compatibility Sheet migration:
- 열린·중복 PR:

### 공격과 비판 검증
- 유효한 finding:
- 기각한 비판:
- 미검증:

### 회귀 재검사
- 실행한 검사:
- 통과:
- 실패:
- 실행하지 못한 검사:

### 최종 판정
- NO_CONFLICT | CONFLICT_FIXED | USER_DECISION_REQUIRED | BLOCKED_UNVERIFIED

### 후속 조치
- 즉시 수정:
- 사용자 결정:
- 보류·재개 조건:
```

문제가 없더라도 `NO_CONFLICT`와 실제 비교·검사 범위를 명시한다.

## 14. 완료 조건

- 질문 전에 최신 main·repository 정본·PR·필요한 approved PDF canon/exception source를 비교했다.
- 기존 승인 결정을 다시 묻지 않았다.
- 기술 기본값과 사용자 기획 결정을 구분했다.
- 질문과 승인 원문이 GitHub 추적 surface에 남았다.
- 승인 Decision이 `CURRENT_CONFIRMED_DECISIONS.md`와 repository 분야 정본에 반영됐다.
- 승인 structured 문서가 PR을 거쳐 `main`에 반영되고 Commit SHA가 기록됐다.
- 사람이 확인해야 하는 전체 그림·시각·예산·Tier·Flow/Wireframe 변화는 repository owner와 필요한 exact-SHA derived view에 반영하고 readback했다.
- exception/legacy source의 의미 변경이 structured/runtime 변경을 요구하면 repository sync before implementation을 지켰다.
- Google Sheets는 compatibility migration이 필요한 경우에만 사용했다.
- 구현 PR은 중복 없이 병합 또는 근거 있는 close로 수명주기를 종료했다.
- 병합 후 적대적 검토와 회귀 재검사를 실행했다.
- 미실행·권한·설정은 성공으로 표시하지 않았다.

## 15. 실패 조건

- 정본을 읽지 않고 같은 질문을 반복함
- 사용자에게 파일 경로·명백한 기술 세부·초기 수치를 결정하게 함
- 승인 답변을 대화나 댓글에만 남김
- 승인 결정을 checkpoint까지 임시 누적함
- `CURRENT_CONFIRMED_DECISIONS.md`만 갱신하고 repository 분야 책임 원본을 누락함
- 사람이 봐야 하는 중요 변경인데 repository-native view 또는 required derived PDF를 갱신하지 않음
- exception/legacy source에서 structured/runtime 의미를 바꾸고 repository 동기화 없이 구현함
- repository 또는 필요한 approved PDF canon/exception source 한쪽만 갱신하고 `SYNCED`로 주장함
- Google Sheets를 새 기본 사용자 workspace로 복원함
- 같은 Goal에 새 PR을 반복 생성함
- merge-complete가 아닌 PR을 열린 상태로 방치하거나 검증 Gate를 무시해 main에 병합함
- 병합된/닫힌 PR 기록을 삭제 대상으로 오인함
- 병합 뒤 정본·최근 승인·approved PDF canon/exception·회귀 비교를 생략함
- 실행하지 않은 CI·runtime·approved PDF canon/exception readback을 통과로 보고함

<!-- FEDERATED_DUAL_CANON_ROUTE -->

> V4 정본 경로: `FEDERATED_DUAL_CANON_SINGLE_FACT_OWNER`. `REPOSITORY_EXECUTION_DATA_CANON`은 편집 가능한 구조화·실행·runtime·작업상태·evidence 정본이다. `USER_APPROVED_AND_MANIFEST_REGISTERED`를 충족한 `APPROVED_HUMAN_BLUEPRINT_PDF_CANON`만 불변 사람용 시각·검수 정본이다. `ONE_EDITABLE_OWNER_PER_ATOMIC_FACT`; `CANDIDATE_PDF_NOT_CANON`과 PDF 주석은 repository-owned fact를 직접 바꾸지 않는다. 상세 owner는 `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`과 `docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md`다.
