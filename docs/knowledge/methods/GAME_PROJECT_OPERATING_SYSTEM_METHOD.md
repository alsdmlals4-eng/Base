# 게임 프로젝트 저장소 운영체계 방법

- 상태: 공용 원칙·호환 경로
- 단일 운영 설명 원본: `docs/OPERATING_MODEL.md`
- 실행 Skill: `skills/managing-game-project-operating-system/SKILL.md`

이 문서는 기존 참조 경로를 보존하면서 운영체계의 고유 원칙만 요약한다. 설치·감사·마이그레이션·Health Review의 단계형 실행 절차는 통합 Skill의 `install`, `audit`, `migrate`, `verify` mode가 책임진다.

## 핵심 원칙

```text
사용자 방향
→ 저장소 루트 [기획서]
→ DESIGN_DOCUMENT_REGISTRY.json
→ 등록된 Markdown 또는 JSON 책임 원본
→ Development Gates·Roadmap
→ SKILL_REGISTRY.json·선택적 Skill
→ 코드·데이터·자산·테스트
→ Active Context·Learning Log
→ 정책 기반 사람용 발행·GitHub Governance
```

- 새 GPT와 Codex가 같은 시작 경로를 읽는다.
- 한 질문에는 현행 책임 원본 하나만 둔다.
- 승인·구현·검증·발행 최신성·사람 검수를 분리한다.
- 전체 스킬이 아니라 trigger가 일치하는 최소 Skill과 mode만 호출한다.
- 프로젝트 고유 정보는 프로젝트 저장소에 둔다.
- 기존 프로젝트는 Audit only와 사용자 승인 없이 구조를 강제 변경하지 않는다.
- 파일 존재와 실제 실행·GitHub Actions·Required Status Check 강제를 구분한다.
- 새 AI가 과거 대화 없이 저장소만으로 작업을 재개한다.

## 책임 분야

설정·내러티브, 게임 디자인, UX·UI·접근성, 개발·엔지니어링, 테크니컬 아트·파이프라인, 아트, 사운드, QA, 프로덕션·PM, 분석·유저리서치, 통합검수는 선택 가능한 공용 카탈로그다. 프로젝트가 실제로 사용하는 책임만 Registry에 등록한다.

작은 프로젝트는 여러 책임을 한 원본에 통합할 수 있지만 `responsibility_coverage`에서 누락 없이 선언한다.

## 실행 라우팅

| 작업 | Skill·mode |
|---|---|
| 신규 운영체계 설치 | `managing-game-project-operating-system: install` |
| 기존 구조 감사 | `managing-game-project-operating-system: audit` |
| 승인된 구조 이관 | `managing-game-project-operating-system: migrate` |
| 설치·마이그레이션·주요 게이트 검수 | `managing-game-project-operating-system: verify` |
| 기획 책임 원본·발행 | `managing-design-documents` |
| Skill 구조·학습 | `evolving-project-discipline-skills` |
| Active Context·Handoff | `maintaining-project-context-and-handoff` |
| 작업·제품 게이트 | `DEVELOPMENT_GATES_METHOD.md` |

## 발행 정책

문서마다 Registry에서 `source_only`, `milestone_sync`, `always_sync` 중 하나를 선택한다. PDF는 정책이 요구할 때 동기화하고 DOCX·다이어그램은 선언한 경우만 생성한다.

## 상태 언어

```yaml
lifecycle_status: ACTIVE/HOLD/BACKUP/REMOVAL_CANDIDATE
approval_status: UNCONFIRMED/CONFIRMED/REJECTED
implementation_status: NOT_STARTED/IN_PROGRESS/IMPLEMENTED
verification_status: NOT_RUN/PASSED/FAILED/PARTIAL
publication_status: NOT_BUILT/STALE/CURRENT/FAILED
```

JSON·DOCX·PDF·Skill 존재는 구현·검증 완료 증거가 아니다.

## 콜드 스타트

새 작업자는 프로젝트 목적·핵심 경험, 현재 단계·다음 작업, 보호 범위, 책임 원본, 실제 파일, 필요한 Skill과 검증, 미확정·보류·위험을 저장소만으로 찾을 수 있어야 한다.
