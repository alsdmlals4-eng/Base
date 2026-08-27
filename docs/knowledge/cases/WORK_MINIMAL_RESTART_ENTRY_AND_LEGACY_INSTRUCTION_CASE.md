# Work 최소 재개 입력과 legacy 지시문 의존 제거 사례

```text
MINIMAL_RESTART_INPUT_SHOULD_ROUTE_CURRENT_OWNERS
LONG_CHAT_INSTRUCTION_ATTACHMENT_IS_NOT_CANON
LEGACY_RETIREMENT_REQUIRES_UNIQUE_CONTENT_RECONCILIATION
ONE_LINE_ENTRY_MUST_NOT_WEAKEN_GATES
```

## 1. 문제

Work 프로젝트 운영 기능은 Base와 Project 정본에 이미 있어도, 사용자가 새 프로젝트 채팅을 열 때마다 과거 장문 작업지시문 파일을 다시 첨부해야 한다고 느끼면 다음 문제가 생긴다.

- 같은 계약이 Base와 채팅 첨부 파일에 중복된다.
- 과거 파일이 current Base보다 오래되어도 눈앞의 긴 문구가 우선되는 drift가 생긴다.
- 프로젝트별 채팅 용량과 재개 비용이 늘어난다.
- 여러 프로젝트가 서로 다른 복사본을 사용한다.
- 파일을 갑자기 버리면 아직 정본으로 이관되지 않은 고유 프로젝트 규칙이 사라질 수 있다.

## 2. 실제 Base 상태

Current Router는 exact Project와 Base를 fresh-read한 뒤 다음 owner를 progressive-load한다.

```text
WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md
WORK_PROJECT_START_CANON_CHECKLIST.md
WORK_FIVE_PHASE_VERTICAL_SLICE_EXECUTION_CONTRACT.md
WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md
WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md when delegated
WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md
```

Starter는 이미 다음을 소유한다.

```text
AUTO_GIT_FETCH_AND_SAFE_PULL
AUTO_PUSH_CURRENT_TASK_BRANCH_AFTER_VERIFICATION
current-task PR / required checks / squash merge / readback
INCIDENT_SOLUTION_LESSON_LOOP
BASE_PROMOTION_DISPOSITION_REQUIRED
DO_NOT_AUTO_ADVANCE_TO_NEXT_SLICE_BEFORE_USER_VALIDATION
```

따라서 채팅 입력에 세부 절차를 재복사할 필요가 없다. 필요한 것은 **짧은 입력을 Router invocation으로 해석하는 계약**이다.

## 3. 채택 패턴

사용자 routine 입력은 다음 한 줄이다.

```text
[프로젝트명] 작업 재개. Base 최신 main과 프로젝트 고유 GitHub·Notion·actual implementation을 fresh-read하고, 현재 5단계 위치를 복원한 뒤 다음 안전 작업부터 진행해.
```

처리:

```text
exact Project identity resolve
→ Base latest completed main read
→ Project GitHub·Notion·actual implementation read
→ Current Router
→ Starter + five-phase + specialist owners progressive-load
→ native state mapping / canon correction
→ next safe current-Slice work
```

## 4. legacy 지시문 처리

```text
legacy file exists
→ current canon과 비교
→ current owner에 이미 흡수된 공용 규칙: historical reference
→ Project에만 유효한 unique rule: Project canon으로 bounded migration
→ 여러 프로젝트에 재사용 가능한 unique rule: Base promotion disposition
→ superseded/conflicting rule: superseded evidence와 이유 기록
→ routine 채팅 첨부 의존 종료
```

다음은 금지한다.

- 긴 파일이 있다는 이유로 current Base보다 우선하기
- 파일을 읽지 않았는데 모든 unique 내용이 이관됐다고 추측하기
- 미이관 규칙을 조용히 삭제하기
- historical instruction을 새 current truth로 다시 복사하기

## 5. 안전 경계

한 줄 입력은 다음을 자동 승인하지 않는다.

- 새 core identity·Core Loop·핵심 시스템 의미
- 별도 명시 Gate가 필요한 이미지 생성
- 새 비용·권한·권리 불확실성
- 공개 배포·store 제출
- 파괴적 migration·direct main·force/admin bypass

필수 Base/Project source를 읽을 수 없거나 exact 프로젝트가 식별되지 않으면 memory·과거 채팅으로 보충하지 않고 `BLOCKED_UNVERIFIED`다.

## 6. 교훈

```text
PROMPT_LENGTH_IS_NOT_EXECUTION_COVERAGE
CURRENT_OWNER_ROUTING_BEATS_INLINE_DUPLICATION
NO_ATTACHMENT_REQUIRED_DOES_NOT_MEAN_NO_MIGRATION_CHECK
SHORT_ENTRY_REQUIRES_STRONG_CANON_AND_READBACK
```

- 짧은 재개문이 안전하려면 Base Router와 Project canon이 실제로 current여야 한다.
- 기능 보존은 긴 prompt 복사가 아니라 owner routing·contract test·readback으로 보증한다.
- legacy 파일 의존 제거와 unique content 유실 방지는 동시에 수행해야 한다.
- 문제·해결·교훈과 Base 승격은 새 알고리즘이 아니라 기존 Starter owner를 재사용한다.

## 7. Evidence ceiling

이 사례는 Base process 입력·routing 계약이다. 특정 프로젝트의 기획·에셋·구현·runtime·Human/Player PASS를 증명하지 않는다.
