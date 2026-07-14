# Base 문서 역할표

## Base의 책임

Base는 여러 프로젝트에 공통으로 필요한 AI 협업 원칙과 템플릿의 원본 저장소다.

프로젝트별 엔진 규칙, 제품 기획, 코드, 데이터, 테스트 결과는 각 프로젝트 저장소가 책임진다.

## 공용 원본 문서

| 구분 | 파일 | 역할 |
|---|---|---|
| 공용 원본 | `AGENTS.md` | 최소 공용 AI 작업 원칙 |
| 공용 원본 | `docs/AI_SHARED_WORK_RULES.md` | 역할, 범위, 품질 원칙, Base 승격 운영 방식 |
| 공용 원본 | `docs/AI_WORKFLOW_RULES.md` | 공통 작업 순서와 Goal 작성 기준 |
| 공용 원본 | `docs/CONTENT_DESIGN_METHOD.md` | 의도→경험→규칙→흐름 기반 콘텐츠 기획, 첫 10분, PoC, 채택·제외 기준 |
| 공용 원본 | `docs/AI_SKILL_ADOPTION_GUIDE.md` | 외부 스킬 채택, 권한 점검, 최소 라우팅, context compact 기준 |
| 공용 원본 | `docs/MVP_WORKFLOW_CHECKLIST.md` | 실제 작업 시작/종료 체크리스트 |
| 공용 원본 | `docs/BENCHMARKING_REFERENCE_GUIDE.md` | 벤치마킹 기록과 적용 기준 |
| 공용 원본 | `docs/DOCUMENTATION_MAP.md` | 공용 문서와 프로젝트 문서의 책임 경계 |
| 공용 원본 | `docs/CUSTOM_INSTRUCTIONS_GUIDE.md` | ChatGPT/Codex 맞춤형 지침 작성 기준 |
| 공용 원본 | `docs/CHANGELOG.md` | Base 규칙 변경 기록 |
| 공용 템플릿 | `templates/CONTENT_DESIGN_BRIEF.md` | 핵심 재미·첫 10분·콘텐츠 정체성·PoC를 정리하는 프로젝트용 양식 |
| 공용 원본 | `templates/` | 프로젝트용 문서 템플릿 |

## 프로젝트 동기화 규칙

1. 프로젝트는 필요한 Base 문서를 로컬 사본으로 둔다.
2. 일상 작업에서는 프로젝트 내부의 로컬 사본을 우선 읽는다.
3. Base의 커밋 SHA와 동기화 날짜는 프로젝트의 `docs/BASE_RULES_VERSION.md`에 기록한다.
4. 프로젝트 전용 규칙은 Base 문서를 보완하며, 더 구체적인 규칙이 우선한다.
5. Base 규칙을 바꿀 필요가 생기면 먼저 공용성 여부를 확인하고, 프로젝트 전용 내용은 프로젝트에 남긴다.

## 새 프로젝트에 복사할 기본 문서

- `AGENTS.md`
- `docs/AI_SHARED_WORK_RULES.md`
- `docs/AI_WORKFLOW_RULES.md`
- `docs/CONTENT_DESIGN_METHOD.md`
- `docs/AI_SKILL_ADOPTION_GUIDE.md`
- `docs/MVP_WORKFLOW_CHECKLIST.md`
- `docs/BENCHMARKING_REFERENCE_GUIDE.md`
- `docs/DOCUMENTATION_MAP.md`
- `docs/CUSTOM_INSTRUCTIONS_GUIDE.md`
- `templates/CONTENT_DESIGN_BRIEF.md`
- 필요한 `templates/` 파일

## 프로젝트에서 새로 작성할 문서

- `docs/BASE_RULES_VERSION.md`
- 프로젝트 전용 `AGENTS.md` 보강
- 프로젝트 전용 Codex / 구현 규칙
- `README.md`
- `PROJECT_BRIEF.md`
- `DESIGN_INTENT.md`
- `MVP_ROADMAP.md`
- `TEST_CHECKLIST.md`
- 프로젝트 설정, 데이터, 코드, 씬, 테스트 자산

## 관리 원칙

- 같은 규칙을 여러 문서에 장문으로 중복 작성하지 않는다.
- 반복 가능한 작업 원칙은 Base에 둔다.
- 엔진, 폴더 구조, 세계관, 데이터, MVP 상태는 프로젝트 전용 문서에 둔다.
- Issue는 현재 작업 기준서다.
- Goal은 구현 실행 지시서다.
- 맞춤형 지침은 짧고 안정적인 행동 원칙만 담고, 상세 정보는 GitHub 문서에 둔다.
- Base 승격 후보는 사용자 승인 후 Base에 별도 커밋으로 반영한다.