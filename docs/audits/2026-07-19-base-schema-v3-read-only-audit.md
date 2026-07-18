# 최종 읽기 전용 감사 — Base schema v3 전환 전

## 1. 총평

- 방향성: 조건부 적절
- 병합 판정: 수정 후 가능
- 가장 중요한 이유: PR #8이 만든 생성·해시·렌더 기반은 재사용할 가치가 있지만, JSON 전용 기획 본책·필수 DOCX·고정 11개 분야·삭제된 템플릿 참조는 최신 사용자 계약과 다르다.

기준:

- PR #8 부모: `51d3535afa3eea5b19d262e1fe87d06f183c2224`
- PR #8 병합: `30bb3fe0908603c28eee76fc047f3bb75f1efc08`
- PR #8: 57 commits, 47 changed files, merged
- PR 마지막 검증 tree와 병합 tree: 동일
- GitHub Actions: `Validate Game Project Operating System` 성공
- Branch protection·Required Check 실제 설정: `[검증]` — 인증된 GitHub API에서 `main`은 보호되지 않았고 repository ruleset은 0개였다. 설정은 변경하지 않았다.

## 2. 요구사항 추적표

| 요구사항 | PR #8 이전 위치 | 현재 반영 위치 | 상태 | 검증 증거 | 누락·위험 |
|---|---|---|---|---|---|
| 기존 프로젝트 Audit only | 기존 Migration Method·Skill | Migration Method·Skill | [검증] | 보존→승인→변경 순서 존재 | 목표 형식이 JSON으로 고정됨 |
| 한 질문에 책임 원본 하나 | 공용 규칙·기획 Method | AGENTS·Documentation Map | [확인] | 중복 원본 금지 문구 | JSON/Markdown 역할 구분 필요 |
| Markdown·JSON 역할별 혼용 | Markdown 본책 템플릿 | JSON 전용 Registry·검사기 | [누락] | `source_json` 필수, Markdown 본책 금지 | schema v3 필요 |
| PDF 상시 동기화 | PDF Publication 계획 | 생성기·Manifest·Governance | [부분 반영] | 입력·출력 해시 검사 | DOCX·다이어그램까지 항상 강제 |
| 사람 검수와 최신성 분리 | 범용 Manifest | 전용 Manifest·설정 | [부분 반영] | 전용 검사는 선택적 사람 검수 | 범용 검사는 CURRENT에 시각 검수 강제 |
| DOCX 선택 출력 | 없음 | DOCX 필수 생성·검사 | [누락] | Registry·검사기의 필수 필드 | 임시 출력 계약 필요 |
| 최소 Skill 호출 | Skill Map·Registry | Skill Registry·라우팅 | [검증] | `load_all_skills=false` | 삭제된 Markdown Skill Map 읽기 지시 존재 |
| Learning Log 근거 중심 | Skill evolution 문서 | 모든 의미 있는 호출 기록 | [부분 반영] | 승격 단계 존재 | 사소한 호출 기록 부담 |
| 11개 분야 선택 적용 | 공용 분야 목록 | Governance 필수 coverage | [누락] | 설정에 11개 필수 목록 | 작은 프로젝트에 구조 강제 |
| Issue 또는 직접 요청 | Issue·Goal 중심 | Issue 중심 문구 | [부분 반영] | 사용자 요청 우선순위 존재 | 직접 승인 요청 계약이 명시되지 않음 |
| Base와 프로젝트 Godot 경계 | 공용·전용 구분 | AGENTS·Method | [확인] | 프로젝트 고유 경로·수치 분리 | 설치 템플릿에서 재확인 필요 |
| Windows/Linux 생성 | Linux Actions | Linux 의존성 설치 | [부분 반영] | Ubuntu Actions 및 Windows v2.2 LibreOffice·Poppler 실제 생성 성공 | schema v3 Windows·Linux CI는 PR 2에서 검증 필요 |
| 결정적·원자적 생성 | 없음 | 생성 시각·직접 출력 | [누락] | 동일 입력 diff 테스트 없음 | 실패 시 부분 산출물 위험 |
| 실제 PDF 전 페이지 품질 | PDF 렌더 계획 | PNG 렌더·빈 페이지 검사 | [부분 반영] | 자동 렌더 성공 | Codex 전 페이지 시각 검수·사람 검수 별도 필요 |
| 콜드 스타트 | Handoff Method | START_HERE·Registry | [부분 반영] | 읽기 순서 존재 | 실제 새 작업 실행 증거 없음 |

## 3. 잘 잡힌 방향

- Base 공용 지식과 프로젝트 고유 Godot 정보의 분리.
- 기존 프로젝트의 Audit only·보존 대조·승인 후 변경.
- Skill Registry를 이용한 선택적 호출.
- 작업 게이트와 제품 게이트의 분리.
- PDF 전 페이지 렌더, 빈 페이지 검사, 해시 기반 stale 탐지.
- 승인 이미지·실제 캡처·보류·미검증 상태를 별도 필드로 유지하려는 구조.

## 4. 누락 사항

- Markdown 기획 본책의 공식 계약과 렌더러.
- Registry·Manifest 정식 JSON Schema.
- 선택적 DOCX와 선택적 다이어그램.
- 동일 입력 결정성·원자적 교체·실패 복구.
- Windows 실제 생성 검증.
- 필수 프로젝트 허브 문서의 설치 템플릿.
- 직접 승인 요청을 Issue의 대체 작업 계약으로 인정하는 규칙.

## 5. 추가·개선 권고

- PR 1에서 삭제 참조·운영 템플릿·Issue 예외·분야 선택·Learning Log 조건을 정리한다.
- PR 2에서 Markdown 기본·JSON 구조 데이터·PDF 상시 동기화·선택 DOCX·Mermaid·결정적 생성을 하나의 schema v3로 전환한다.
- 생성 실패 시 임시 출력만 폐기하고 기존 CURRENT 발행본은 보존한다.

## 6. 기존 정보 손실 위험

| 제거 템플릿 | 현행 승계 | 상태 | 남은 위험 |
|---|---|---|---|
| `DISCIPLINE_BIBLE.md` | `DESIGN_DOCUMENT.json`의 목표·품질·책임·workflow·gate·state·risk·next action | [부분 반영] | RACI, 사람이 편집하기 쉬운 장문 계층, PDF 발행 상태 설명 |
| `PROJECT_SKILL_MAP.md` | `SKILL_REGISTRY.json`·PDF·다이어그램 | [부분 반영] | 콜드 스타트용 텍스트 요약과 중복·통합 검수 설명 |
| `DISCIPLINE_PDF_PUBLICATION.md` | PDF Method·Registry·Manifest | [부분 반영] | 문서별 발행 목적·구성·시각 검수 계획의 사람이 읽는 요약 |
| `PUBLICATION_MANIFEST.json` | 문서별 `_PUBLICATION_MANIFEST.json` | [검증] | 범용 검사와 전용 검사 상태 의미 불일치 |

Git 이력은 복구 근거이지 활성 정보의 대체물이 아니다. PR 1·2에서 현행 계약에 필요한 항목만 복원하고 단순 역사·중복 설명은 복원하지 않는다.

## 7. PDF/DOCX 수동 검수 결과

- 자동 렌더·파일 헤더·빈 페이지: `[검증]` — PR #8 Linux Actions 증거.
- Windows 실제 생성: `[검증]` — LibreOffice 26.2.4.2, Poppler 26.05.0, 맑은 고딕으로 현행 v2.2 DOCX·PDF·다이어그램 생성 테스트를 실행했다.
- Codex 전 페이지 시각 검수: `[미검증]` — schema v3 대표 출력 생성 후 수행.
- 사람 시각 검수: `[미검증]` — 사용자가 직접 보지 않았으므로 PASSED로 기록하지 않음.

## 8. 콜드 스타트 검증 결과

- 라우팅 구조 존재: `[확인]`.
- 실제 새 Codex 작업: `[미검증]`.
- 필수 템플릿 누락으로 현재 완전 통과를 주장할 수 없음.

## 9. 스킬·게이트 검증 결과

- 선택적 Skill Registry와 Foundation·분야 계층: `[검증]`.
- 11개 분야 일률 강제 방지: `[누락]`.
- Learning Log의 근거 중심 기록: `[부분 반영]`.
- 증거 없는 개발 게이트 통과 차단: `[부분 반영]`.

## 10. 테스트와 Actions 증거

- PR #8 Actions: `[검증]`.
- 현재 main JSON 문법과 Markdown 상대 링크: `[검증]`.
- Branch protection·Required Check 설정: `[검증]` — `main` branch protection 없음, repository ruleset 0개. 변경은 별도 사용자 승인 범위다.
- Windows v2.2 생성: `[검증]`. schema v3 동일 입력 diff 0·실패 보존: `[미검증]`.

## 11. GitHub Issue·Plan·Goal 추적성

- PR #8 연결 Issue: 없음.
- 이번 작업 근거: 사용자가 승인한 직접 요청과 구현 계획.
- Issue 부재 자체는 차단하지 않으며 PR 본문에 목표·범위·제외·완료 기준·검증·롤백을 기록해야 한다.

## 12. 병합 차단 항목

- P0: schema v3 전환 전 JSON 전용·DOCX 필수·Markdown 금지 계약을 그대로 새 프로젝트에 적용하지 않는다.
- P1: 삭제 참조, 운영 템플릿 누락, 고정 11개 분야, Issue 예외, 상태 의미를 정리한다.
- P2: 공식 Release·태그와 Branch protection 변경은 별도 승인으로 분리한다.

## 13. 최종 결론

- 지금 그대로 새 프로젝트에 적용해도 되는가: 아니오.
- 반드시 해결할 것: PR 1 운영 정합성, PR 2 schema v3와 생성·검증 회귀.
- 후속 작업으로 분리 가능한 것: 공식 Release·태그, Branch protection 변경.
- 사용자가 결정해야 할 것: 새로운 P0가 발견될 때만 별도 보고한다.
