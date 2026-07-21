# Base 공용 AI 작업 규칙

Base는 여러 게임 프로젝트가 공유하는 **[학습형] [공용]** Skill·Template·Case·Test의 원본이다. 전체 작업 구조와 상태·발행 정책은 `docs/OPERATING_MODEL.md`가 책임진다. 이 문서는 항상 적용되는 강제 규칙만 둔다.

## 1. Base URL 호출

사용자가 다음처럼 요청하면 먼저 `START_HERE.md`를 읽는다.

> `https://github.com/alsdmlals4-eng/Base 를 전부 살펴보고 참고해서 작업해줘.`

모든 파일과 스킬을 무작정 읽지 않는다.

```text
START_HERE.md
→ docs/OPERATING_MODEL.md
→ docs/DOCUMENTATION_MAP.md
→ skills/SKILL_REGISTRY.json
→ 대상 프로젝트의 현재 책임 원본·실제 파일
```

저장소 접근 없이 설치·마이그레이션·검수 완료를 주장하지 않는다.

## 2. 우선순위

1. 사용자의 최신 지시
2. 프로젝트 `AGENTS.md`와 보안·엔진·데이터 규칙
3. 프로젝트 Active Context와 승인된 작업 계약
4. 등록된 책임 원본과 실제 코드·데이터·자산·테스트
5. 프로젝트에 동기화된 Base 기준
6. Base 원격 원본
7. 과거 대화·초안·추정

정상 동작 중인 사용자 변경을 임의로 되돌리지 않는다.

## 3. 필요한 작업 환경·권한

- 필요한 실행 파일, 라이브러리, 폰트, 입력 파일, 인증, 저장소·브랜치 권한을 작업과 검증 전에 확인한다.
- 누락 항목은 `필요 항목 / 이유 / 설치·설정 방법 / 재시작·적용 / 확인 명령 / 최소 권한`으로 안내한다.
- 사용자 승인 없이 시스템 전역 설치, 계정·보안 설정, 권한 확대, Branch protection 변경을 수행하지 않는다.
- 사용자가 설치·권한 부여를 완료했다고 알려도 실제 경로·버전·인증·쓰기 가능 여부를 확인한다.
- 실행하지 않은 검사·렌더·권한을 통과로 보고하지 않는다.

## 4. 요청 라우팅·작업 계약

새 L1 이상 요청은 `managing-project-intake-and-work-contract`에서 한 번만 처리한다.

```text
route
→ 저장소 사실 조사
→ 필요한 경우 clarify
→ 사용자 마지막 확인
→ contract
```

- 작업 수준 L0~L4
- 주 책임 분야 하나와 실제 영향 분야
- 변경 유형
- 최소 Foundation·분야 Skill
- 범위·제외·보호 대상
- 완료 기준·검증·롤백

오탈자, 명확한 단일 파일 기계 수정, 입력이 같은 검사 재실행은 예외다. 상세 요청은 처음부터 다시 묻지 않고 저장소 사실과 결과를 바꾸는 누락만 확인한다.

금지:

- 전체 skills 폴더 기본 로드
- `load_by_default=true`인 활성 Skill
- trigger와 무관한 호출
- 같은 요청의 수준·범위·상태를 여러 Skill에서 중복 판정
- 주 책임 분야 Skill을 여러 개 지정
- 검증·발행·Handoff의 조기 실행
- `[백업]`, `[보류]`, `[제거 후보]` Skill 호출

## 5. 활성 통합 Skill

| 책임 | Skill |
|---|---|
| 요청 라우팅·요구 확정·실행 계약 | `managing-project-intake-and-work-contract` |
| 신규 설치·기존 감사·승인된 마이그레이션·Health Review | `managing-game-project-operating-system` |
| 기획 책임 원본 작성·재구조화·발행·검수 | `managing-design-documents` |
| 프로젝트 Skill 생성·통합·학습 | `evolving-project-discipline-skills` |
| Active Context·Handoff | `maintaining-project-context-and-handoff` |
| 프로젝트 교훈·Base 변경 제안 생명주기 | `managing-base-change-proposals` |
| Vertical Slice | `designing-vertical-slices` |
| 외부 AI 작업 공간 | `orchestrating-deepseek-worktrees` |
| 외부 AI 결과 독립 검수 | `reviewing-external-ai-drafts` |
| 이미지 프롬프트·기술 카드 | `designing-art-prompts-and-technique-cards` |
| 구현된 Godot·Web UI 감사 | `auditing-and-refining-ui-art` |

통합 전 ID는 `skills/LEGACY_SKILL_ALIASES.md`에서 새 Skill과 mode로 변환한다. 새 Registry·문서·작업 계약에는 새 ID만 사용한다.

## 6. 책임 원본과 발행

신규 프로젝트와 승인된 마이그레이션의 활성 기획서는 저장소 루트 아래에 둔다.

```text
<repository-root>/[기획서]/
```

- 한 질문에는 Registry에 등록된 단일 Markdown 또는 JSON 책임 원본 하나를 둔다.
- 서술 중심 기획은 Markdown, Registry·Manifest·상태·ID·경로·게임 데이터는 JSON을 사용한다.
- 같은 서술을 Markdown과 JSON 양쪽에 중복 책임 원본으로 만들지 않는다.
- DOCX·PDF를 독립 책임 원본으로 수동 유지하지 않는다.
- `v2`, `final`, `latest`, 날짜별 활성 복제본을 만들지 않는다.

문서 발행은 `managing-design-documents`와 Registry의 정책을 따른다.

- `source_only`: 원본과 직접 검증만 유지
- `milestone_sync`: 주요 게이트·공유 시 PDF·Manifest 동기화
- `always_sync`: 원본·승인 이미지·생성기 변경과 같은 작업에서 동기화

DOCX와 다이어그램은 선언한 경우만 생성한다. `CURRENT`, 자동 렌더, Codex 시각 검수, 사용자 시각 검수는 독립 상태다.

## 7. 기존 프로젝트 안전 마이그레이션

`managing-game-project-operating-system`을 사용한다.

```text
audit
→ 책임·참조·고유 정보 조사
→ 목표 구조·보존·롤백 제안
→ 사용자 승인
→ 승인된 처리표만 migrate
→ 보존·참조·발행 대조
→ verify
```

사용자 승인 전 금지:

- 파일·폴더 대량 삭제·이동·통합
- 기존 책임 문서 대규모 축약
- 승인 이미지·자산 제거 또는 임의 교체
- 프로젝트 용어·수치·결정 변경
- `[보류]` 폐기
- Base 구조에 맞춘 강제 개명

고유 정보·참조·복구·사용자 승인이 확인되지 않은 항목은 삭제하지 않고 `[제거 후보]`로 유지한다.

## 8. Active Context·Handoff

Active Context는 현재 상태의 기본 원본이다. 프로젝트 방향·분야 본책·Roadmap·Skill을 먼저 갱신한 뒤 현재 차이·다음 작업·위험·읽기 순서만 압축한다.

별도 Handoff는 세션·담당자·브랜치·마일스톤 경계의 스냅샷이며 두 번째 활성 현재 상태 원본으로 유지하지 않는다.

## 9. Skill 학습·통합

새 Skill을 만들기 전에 기존 통합 Skill의 mode로 처리할 수 있는지 확인한다. 독립된 입력·산출물·Quality Bar·검증·승인 경계가 있을 때만 새 Skill을 만든다.

실패, 중요한 결정, 재사용 가능한 교훈 또는 실제 검증 결과가 있는 호출을 Learning Log에 기록한다. 한 번의 성공을 공용 강제 규칙으로 만들지 않는다.

통합 시 고유 입력·산출물·실패 조건·검증·reference·script·Learning Log를 보존하고 이전 ID를 `LEGACY_SKILL_ALIASES.md`에 연결한다.

## 10. 프로젝트 교훈의 Base 승격

`managing-base-change-proposals`를 사용한다.

```text
프로젝트 증거
→ extract
→ submit
→ [수정제안서] SUBMITTED
→ review·사용자 승인
→ 별도 구현 PR에서 implement
→ verify
```

신규 제안 PR과 활성 Base 구현 PR을 합치지 않는다. 사용자 승인 전에는 활성 Base Skill·Template·Tool·Schema·Test를 바꾸지 않는다. 사용자가 직접 승인한 Base 변경 요청은 별도 제안서 없이 작업 계약이 될 수 있다.

## 11. 이미지·UI 계약

- 기존 승인 이미지가 있으면 별도 지시 없이 새 시안을 만들지 않는다.
- Asset ID·캐노니컬 경로·출처·승인 상태·채택·비채택 요소·실제 캡처를 기록한다.
- 이미지 안 임시 수치·문구를 공식 기획값으로 해석하지 않는다.
- 생성 전 프롬프트 설계와 구현 후 UI 감사는 독립 Skill로 유지한다.
- UI 감사 정적 패턴은 후보일 뿐 결함·자동 삭제 권한이 아니다.
- 사용자 승인된 finding만 수정하고 실제 Godot/Web 전후 렌더로 독립 재검수한다.

## 12. 검증과 완료

최소 검증 순서:

```text
포맷·문법·정적 검사
→ 관련 자동 테스트
→ 정상·실패·경계 경로
→ 저장·불러오기·호환성
→ 실제 화면·플레이·오디오·성능
→ diff와 승인 범위
→ 사용자 수동 검수
```

작업 완료 조건:

1. 실제 결과와 승인·구현·검증 상태가 일치한다.
2. 관련 책임 원본·Registry·Skill·Learning Log가 최신이다.
3. 발행 정책이 요구하는 PDF·Manifest와 선택 파생본이 최신이다.
4. Development Gates·Roadmap·Active Context·Documentation Map이 최신이다.
5. 자동·수동·시각 검증과 미검증이 분리됐다.
6. PR Required Checks와 리뷰가 통과했다.
7. 다음 작업·선행 조건·롤백이 존재한다.
8. 새 AI가 저장소만으로 방향·상태·책임 원본·Skill·검증을 찾는다.

## 13. 로컬과 GitHub

GitHub와 로컬 파일은 자동 양방향 동기화가 아니다.

- 작업 전 원격·로컬 상태를 확인한다.
- 로컬 변경은 검증 후 commit·push한다.
- 원격 변경은 fetch·pull한다.
- Workflow 파일 존재와 실제 실행·Required Check 강제를 구분한다.
- 생성 실패나 미검증 바이너리를 자동 push하지 않는다.

## 14. 완료 보고

- 주 책임·영향 분야
- 실제 변경한 문서·코드·자산·Skill
- 생성한 PDF·선택 DOCX·다이어그램·Manifest
- 유지한 기존 결정·동작·자산
- 실행한 검증과 결과
- 미검증·불일치·남은 위험·롤백
- 보존·통합·백업·보류·제거 후보
- 콜드 스타트 결과
- Base 환류와 다음 작업

실행하지 않은 테스트, 렌더링, 구현, 브랜치 보호를 완료로 보고하지 않는다.
