# Base 운영 모델

이 문서는 Base의 공용 작업 구조와 생명주기의 단일 설명 원본이다. `README.md`, `START_HERE.md`, `AGENTS.md`, 실행 Skill과 체크리스트는 이 문서의 전체 내용을 반복하지 않고 필요한 규칙과 경로만 연결한다.

## 1. 목적

Base는 게임 프로젝트가 다음을 저장소만으로 지속하도록 돕는다.

```text
사용자 방향
→ 등록된 책임 원본
→ 승인된 작업 계약
→ 핵심 컨셉·PoC 또는 실제 코드·데이터·자산
→ 검증 증거
→ 현재 상태·다음 작업
→ 반복 가능한 스킬 학습
```

Base에는 여러 프로젝트에서 재사용 가능한 판단·절차·검증만 둔다. 프로젝트 고유 세계관·수치·경로·자산·구현 상태는 대상 프로젝트가 책임진다.

## 2. 우선순위

1. 사용자의 최신 지시
2. 프로젝트 `AGENTS.md`와 보안·엔진·데이터 규칙
3. 프로젝트 Active Context와 승인된 작업 계약
4. 등록된 프로젝트·분야 책임 원본과 실제 파일·테스트
5. 프로젝트에 동기화된 Base 기준
6. Base 원격 원본
7. 과거 대화와 추측

정상 동작 중인 사용자 변경을 되돌리지 않는다. 실행하지 않은 검사·권한·도구는 통과로 보고하지 않는다.

## 3. 최소 시작 경로

```text
Base START_HERE
→ Base AGENTS
→ Base Documentation Map
→ Base Skill Registry
→ 대상 프로젝트 AGENTS
→ 프로젝트 START_HERE·Active Context·Documentation Map
→ 현재 책임 원본·Issue·Plan
→ 필요한 최소 Skill
→ 실제 파일·테스트
```

`모두 확인`은 모든 파일을 읽는다는 뜻이 아니다. Registry와 Documentation Map으로 현재 작업에 적용되는 책임 원본과 영향 파일만 선택한다.

## 4. 작업 생명주기

```text
요청 접수·라우팅·요구 확정
→ Definition of Ready
→ 핵심 컨셉·기획 방향·PoC 또는 계획·승인
→ 구현·제작
→ 검증
→ 책임 원본·발행·상태 동기화
→ 통합·완료
→ 인수인계·학습
```

작업 실행 게이트와 제품 마일스톤 게이트는 구분한다. 한 기능의 Done은 프로젝트 전체의 Vertical Slice 통과를 뜻하지 않는다.

### 기획 방향 루프

```text
핵심 컨셉
→ 제약 확인
→ 뾰족한 재미 가설
→ 모든 기획 요소 정렬
→ PoC
→ 결과 기반 재조정
→ Production·Vertical Slice 진입 판정
```

PoC는 가장 위험한 가설을 빠르게 틀릴 수 있게 만드는 최소 검증이다. Vertical Slice는 대표 경험의 목표 품질과 제작 파이프라인까지 증명한다.

## 5. 통합 실행 스킬

| 책임 | 실행 Skill |
|---|---|
| 요청 라우팅·사실 조사·사용자 확인·실행 계약 | `managing-project-intake-and-work-contract` |
| 운영체계 신규 설치·기존 감사·승인된 마이그레이션·Health Review | `managing-game-project-operating-system` |
| 기획 책임 원본 작성·구조 변경·발행·검수 | `managing-design-documents` |
| 프로젝트 스킬 생성·통합·학습 | `evolving-project-discipline-skills` |
| 현재 상태·다음 작업·위험 압축 | `maintaining-project-context-and-handoff` |
| 핵심 컨셉·뾰족한 재미·SWOT·MDA/DDE·DDD·PoC·기획 재조정 | `analyzing-and-refining-game-concepts` |
| 대표 플레이 구간 검증 | `designing-vertical-slices` |
| 외부 AI 작업 공간 운용 | `orchestrating-deepseek-worktrees` |
| 코드·데이터·문서·자산 변경의 계약·정적·런타임·회귀 검증 | `reviewing-and-validating-project-changes` |
| 정본 변경의 오래된 참조·내용 drift·파생본·전파 누락 감사 | `auditing-canonical-reference-freshness` |
| 이미지 프롬프트·기술 카드 | `designing-art-prompts-and-technique-cards` |
| 구현된 Godot·Web UI 감사·개선 | `auditing-and-refining-ui-art` |
| 프로젝트 교훈 추출·BCP 제출·검토·승인된 구현 | `managing-base-change-proposals` |

활성 스킬은 모두 `load_by_default=false`이며 trigger가 일치할 때만 호출한다. 주 책임 분야 스킬은 최대 하나다. 검증·발행·Handoff는 해당 단계에서만 호출하거나 통합 스킬의 해당 모드로 실행한다.

`auditing-canonical-reference-freshness`는 모든 변경에 무조건 추가하지 않는다. 파일·경로·ID·Schema·정책·생성기·정본이 바뀌어 여러 소비자에 전파될 가능성이 있을 때 `reviewing-and-validating-project-changes: reference-freshness`에서 전문 검증으로 호출한다.

Base 내부에서 `DDD`는 `Digital Dopamine Design`으로 정의한다. 빠른 보상·즉각 피드백을 통해 뾰족한 재미를 빠르게 이해시키는 설계축이며, 실제 도파민 분비량 측정이나 의학적 중독 진단으로 사용하지 않는다. 외부 자료에서 같은 약어가 나오면 해당 출처의 정의를 확인하기 전 임의 해석하지 않는다.

## 6. 책임 원본

```text
프로젝트 현재 상태 → ACTIVE_CONTEXT.md
문서 위치·책임 → DESIGN_DOCUMENT_REGISTRY.json
프로젝트·분야 방향 → 등록된 Markdown 또는 JSON 원본
작업 범위 → Issue·승인된 직접 요청·Plan
스킬 선택·상태 → SKILL_REGISTRY.json
반복 절차 → Skill
사람용 발행 → Registry 정책이 요구하는 PDF·선택 DOCX·assets
발행 최신성 → Publication Manifest
실제 상태 → 코드·데이터·자산·테스트·캡처
과거 상태 → Git 이력
```

한 질문에는 현행 책임 원본 하나만 둔다. 전문을 여러 문서에 복사하지 않고 다른 문서는 경로와 현재 차이만 기록한다.

## 7. 문서 발행 정책

각 문서는 Registry에서 하나의 정책을 선택한다.

- `source_only`: 원본과 직접 검증만 유지한다.
- `milestone_sync`: 주요 게이트·정기 검토·외부 공유 시 PDF와 Manifest를 동기화한다.
- `always_sync`: 원본·승인 이미지·생성기 변경과 같은 작업에서 PDF와 Manifest를 항상 동기화한다.

DOCX·다이어그램은 선언한 경우만 생성한다. `CURRENT`, 자동 렌더, Codex 시각 검수, 사용자 시각 검수는 독립 상태다.

## 8. 상태 축

하나의 `status`에 모든 의미를 섞지 않는다.

```yaml
lifecycle_status: ACTIVE/HOLD/BACKUP/REMOVAL_CANDIDATE
approval_status: UNCONFIRMED/CONFIRMED/REJECTED
implementation_status: NOT_STARTED/IN_PROGRESS/IMPLEMENTED
verification_status: NOT_RUN/PASSED/FAILED/PARTIAL
publication_status: NOT_BUILT/STALE/CURRENT/FAILED
```

문서·스킬·PDF 존재는 구현이나 검증 증거가 아니다.

## 9. 기존 프로젝트 안전 규칙

기존 운영 프로젝트는 다음 순서를 지킨다.

```text
Audit only
→ 현행 책임·참조·고유 정보 인벤토리
→ 목표 구조·보존·롤백 제안
→ 사용자 승인
→ 승인된 처리표만 마이그레이션
→ 참조·발행·보존 대조
→ Health Review
```

승인 결정·세계관·수치·구현·자산·실패·보류·외부 참조는 조사와 승인 없이 삭제·축약·이동하지 않는다.

## 10. 완료와 검증

변경 완료 판정은 `reviewing-and-validating-project-changes`의 증거 기준을 따른다.

```text
작업 계약 대조
→ 실제 diff·책임 원본 확인
→ 정본·경로·ID·Schema 변경 시 reference-freshness
→ 정적 검사
→ 가능한 런타임·렌더·빌드
→ 대표·경계·반례·회귀
→ 판정·미실행·위험·롤백 보고
```

`reference-freshness`는 변경된 파일뿐 아니라 변경됐어야 하지만 untouched인 소비자·테스트·템플릿·파생본을 확인한다. Legacy Alias·Change Log·과거 case는 활성 stale reference와 구분한다.

외부 AI 결과만 검수할 때도 같은 스킬의 `external-source-review` mode를 사용한다. 설명이나 파일 존재만으로 검증 완료를 주장하지 않는다.

완료 시 다음을 구분한다.

- 실제 변경
- 실행한 검증
- 실행하지 못한 검증
- 사용자 확인 대기
- 남은 위험과 롤백
- 다음 작업과 선행 조건

실패, 중요한 결정, 재사용 가능한 교훈, 실제 검증 결과가 있는 Skill 호출은 Learning Log에 기록한다. 한 번의 성공은 관찰 또는 가설이며, 반복 검증 전에는 공용 강제 규칙으로 승격하지 않는다.

프로젝트 교훈의 Base 환류는 `managing-base-change-proposals`를 사용한다. 제안 PR과 승인된 구현 PR은 분리한다.

## 11. 콜드 스타트 기준

새 작업자가 저장소만으로 다음에 답할 수 있어야 한다.

1. 무엇을 만드는가?
2. 현재 단계와 가장 높은 우선순위는 무엇인가?
3. 무엇을 변경하면 안 되는가?
4. 현재 책임 원본과 실제 파일은 어디인가?
5. 필요한 Skill과 검증은 무엇인가?
6. 다음 작업과 선행 조건은 무엇인가?
7. 미확정·보류·위험은 어디에 기록돼 있는가?

Base 저장소 자체에서는 프로젝트 설치 템플릿을 활성 상태로 오인하지 않는다. Base의 완료 변경은 `docs/CHANGELOG.md`, 활성 스킬은 `skills/SKILL_REGISTRY.json`, 검토 대기 제안은 `[수정제안서]/PROPOSAL_REGISTRY.json`, 진행 중 구현은 GitHub PR·Actions가 책임진다.
