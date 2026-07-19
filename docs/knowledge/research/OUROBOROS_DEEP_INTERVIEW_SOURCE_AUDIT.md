# Ouroboros 딥인터뷰 Source Audit

- 원본: `Q00/ouroboros`
- URL: `https://github.com/Q00/ouroboros`
- 기준 브랜치: `main`
- 기준 커밋: `6202662eae2dad0531225a93e27b18f792bb139b`
- 라이선스: MIT, Copyright (c) 2025 Q00
- 전수 인벤토리: `inventories/ouroboros-6202662e.json`
- tracked 파일: 1,465개
- 감사일: 2026-07-19

## 1. 감사 범위와 방법

기준 커밋의 모든 tracked 파일을 Git object에서 읽어 경로, SHA-256, 바이트 수, 텍스트·바이너리, 미디어 유형, 역할로 인벤토리화했다. 분류 결과는 source 497, test 708, documentation 143, skill 48, configuration 34, schema 15, workflow 17, lockfile 2, asset 1이며 미분류 항목은 0개다.

소스·문서·테스트는 인터뷰 시작, 질문 생성, brownfield 사실 조사, 모호성 점수, 질문 분류, 참고자료 대조, 종료·재진술·확인, 실행 계약 생성의 호출 관계로 대조했다. 생성·락 파일은 재현성 근거로 분류했으며 책임 로직과 구분했다. 유일한 tracked asset은 메타데이터와 용도를 확인했다.

## 2. 원본 구조

```text
skills/interview/SKILL.md
├─ MCP 사용 경로와 MCP 없는 fallback
├─ 저장소 사실 질문의 parent-session 조사
├─ ambiguity ledger·closure gate
└─ 목표 재진술·명시 승인

src/ouroboros/bigbang/
├─ ambiguity.py: 목표·제약·성공 기준·brownfield 맥락 명료성
├─ interview.py / pm_interview.py: 인터뷰 상태와 질문 흐름
└─ question_classifier.py: 사용자 판단·기술 질문·보류 질문 분리

src/ouroboros/interview_adapters/
├─ reference_contrast.py: 참고자료를 요구가 아닌 확인 후보로 변환
└─ models/registry/triggers: 어댑터와 트리거 계약

docs/rfc/ 및 tests/
├─ context-first inverted interview
├─ intent preservation·reference-aware adapters
├─ convergence·closure·deadline
└─ 정상·실패·회귀 시나리오
```

## 3. 채택 판정

| 원본 개념 | 판정 | Base 적용 | 근거 |
|---|---|---|---|
| brownfield 저장소 사실을 먼저 조사 | 채택 | `repository_observed`와 Read first | 사용자에게 이미 존재하는 사실을 되묻는 낭비 방지 |
| 상세 맥락의 inverted interview | 채택 | 재진술 후 오류·누락만 질문 | 상세 요청을 처음부터 다시 묻는 피로 방지 |
| 사용자 판단과 코드 사실 라우팅 | 채택 | 출처 유형·질문 분류 | 현재 사실과 원하는 미래 분리 |
| 목표·제약·성공 기준의 다축 모호성 | 변형 채택 | 6개 균형 축과 장부 | 단일 수치가 아닌 실행 가능성 중심 |
| 참고자료 contrast와 재확인 | 채택 | 채택·변형·제외·차별화 대조 | 참고자료를 요구 권한으로 오인하지 않음 |
| closure audit 후 goal restatement | 채택 | 마지막 한 문장과 명시 승인 | 실행 전 의도 손실 차단 |
| free-text answer refinement | 변형 채택 | 결정·제약을 반증 가능한 문장으로 기록 | 별도 LLM 호출 없이도 적용 가능 |
| 질문 breadth control | 채택 | 목표·범위·제약·산출물·검증·보호 축 | 특정 기술 쟁점 편중 방지 |
| PM/DEV/decide-later 분류 | 변형 채택 | 사용자 판단·기술 판단·보류 가능 | 게임 프로젝트 역할과 결정권에 맞춤 |
| 성공 기준을 실제 산출 동작에 고정 | 채택 | 완료 기준·검증 증거 | 출시 후 KPI처럼 현재 작업이 증명할 수 없는 결과를 완료 조건으로 삼지 않음 |
| 보조 steering보다 인터뷰 불변 계약 우선 | 변형 채택 | 저장소 사실·출처 구분·closure·확인 게이트 보호 | 외부 도구·분야 스킬이 딥인터뷰 핵심 절차를 밀어내지 못하게 함 |
| MCP 영속 세션과 ambiguity 점수 | 제외 | Markdown+JSON Registry로 대체 | 외부 MCP 없이도 핵심 절차가 동작해야 함 |
| Claude/OpenCode/Hermes 런타임 연결 | 비이식 | 복사하지 않음 | Base 공용 Skill의 책임 밖이며 환경 종속적 |
| 병렬 persona fanout 강제 | 변형 채택 | 한 작업자의 순차 반대 관점·누락 점검 허용 | 서브에이전트가 없어도 닫힘 검수 가능 |
| Ouroboros 코드·프롬프트 원문 | 비이식 | 공용 원칙으로 새로 작성 | 정체성·표현·구현 종속성 복제 방지 |

## 4. Base에 추가한 독립 계약

- 기능·게임 경험·아트 방향·구조·워크플로·Base 변경 제안은 딥인터뷰를 거친다.
- 오탈자, 명확한 단일 파일 기계 수정, 동일 검사 재실행은 예외다.
- 상태는 `IN_PROGRESS`, `AWAITING_USER_CONFIRMATION`, `CONFIRMED`, `SUPERSEDED`, `ABANDONED`다.
- 실행 프롬프트는 사용자 확인 근거가 있는 `CONFIRMED` 기록에서만 만든다.
- 사용자가 요구한 산출물 종류를 문서나 체크리스트로 임의 축소하지 않는다.
- 기존 프로젝트는 인터뷰 파일을 강제 이동하지 않고 Documentation Map으로 현행 대응 경로를 연결한다.

## 5. 라이선스·출처 처리

MIT 원본의 아이디어와 검증 사례를 분석했지만 원본 Python·Rust·TypeScript 코드, 스킬 본문, 스크린샷, 플러그인 자산을 Base에 복사하지 않았다. Base 산출물은 프로젝트 독립적인 한국어 운영 원칙, 자체 JSON Schema, 자체 템플릿과 검사기로 재작성했다. 출처와 기준 커밋은 이 문서와 전수 인벤토리에 보존한다.

## 6. 미채택 위험

- 정량 ambiguity score는 모델·프롬프트에 따라 거짓 정밀도를 만들 수 있어 강제하지 않는다.
- 자동 deadline 또는 partial seed는 사용자의 미확정 방향을 묵시적으로 확정할 수 있어 도입하지 않는다.
- 외부 도구 장애가 인터뷰 자체를 막지 않도록 파일 기반 fallback을 기본 계약으로 삼는다.
