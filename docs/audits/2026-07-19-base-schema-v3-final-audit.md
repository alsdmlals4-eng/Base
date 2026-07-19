# 최종 읽기 전용 감사

## 1. 총평

- 방향성: 적절
- 병합 판정: 조건부 가능
- 가장 중요한 이유: PR #9에서 보존·운영 계약을 정리했고 PR #10에서 Markdown 기본·구조화 JSON·PDF 상시 동기화·선택 DOCX/Mermaid·원자적 생성을 하나의 schema v3 계약으로 구현했다. 병합 조건은 PR #10 최종 Actions 성공이다.

검수 기준:

- PR #8 부모: `51d3535afa3eea5b19d262e1fe87d06f183c2224`
- PR #8 병합: `30bb3fe0908603c28eee76fc047f3bb75f1efc08`
- PR #9 병합: `45df92c18c12e3b0d070bbc75498490b063e68a0`
- PR #10 검수 head: `084bda2c57f5af0f0d927f8b6edc90809e00f82e`
- 공식 작업 계약: 사용자가 승인한 `Base 최종 감사 및 schema v3 수정 계획`

## 2. 요구사항 추적표

| 요구사항 | 반영 위치 | 상태 | 검증 증거 | 누락·위험 |
|---|---|---|---|---|
| 요구사항·PR #8 무손실 추적 | `docs/audits/2026-07-19-base-schema-v3-read-only-audit.md` | [검증] | PR #8 부모와 병합 tree, 제거 템플릿 4종 대조 | 단순 역사 정보는 복원하지 않음 |
| Markdown 기본·JSON 역할별 혼용 | `AGENTS.md`, Registry v3 Schema, 작성·발행 Skill | [검증] | Markdown/JSON 생성·Governance 회귀 테스트 | 동일 서술의 이중 책임 원본은 금지 |
| PDF 상시 동기화 | `tools/build_design_documents.py`, Manifest v3, Governance | [검증] | stale source/generator 실패 테스트 | 사람이 매번 검수했다는 뜻은 아님 |
| 선택 DOCX·다이어그램 | Registry v3, 두 생성기 | [검증] | Markdown no-DOCX, JSON DOCX, Mermaid 조건부 생성 테스트 | Word 검토가 필요한 문서만 공개 DOCX 사용 |
| Skill Map 선택 Markdown | `tools/build_project_skill_map.py`, Skill Registry Schema | [검증] | 생성 해시·수동 변경 탐지 테스트 | 수동 책임 원본으로 사용 불가 |
| 자동·Codex·사람 검수 분리 | Manifest v3, PDF Method | [검증] | 사람 게이트 해시 테스트, 13페이지 Codex 시각 검수 | 사용자 사람 검수는 `[미검증]` |
| 결정적 재생성 | `tools/publication_v3.py`, 생성기 테스트 | [검증] | 동일 입력 재실행 추적 diff 0 | 다른 LibreOffice 버전 간 byte 동일성은 보장 범위 밖 |
| 원자적 생성·실패 복구 | 두 생성기, `publication_v3.py` | [검증] | 실패 후 기존 PDF·Manifest 해시 보존 테스트 | 외부 프로세스 강제 종료 시 임시 디렉터리 정리는 OS에 의존 |
| Windows/Linux 의존성 | preflight 도구, GitHub Actions | [검증] | Linux 실제 생성, Windows LibreOffice·고정 Poppler·Mermaid 실제 생성 | macOS는 지원 계약 밖 |
| Schema 버전·마이그레이션 | `schemas/`, `docs/migrations/v2.2.0-to-v3.0.0.md` | [검증] | v2 명시 오류·v3 Schema 테스트 | 자동 v2 호환 없음은 승인된 결정 |
| Issue 또는 직접 요청 계약 | `AGENTS.md`, 작업 계약 템플릿 | [검증] | 구조 회귀 테스트 | 장기 다중 PR은 Issue 권장 |
| 11개 분야 선택 적용 | Registry·Governance·설치 문서 | [검증] | 미선택 분야 진입점 비강제 테스트 | 선택 분야는 진입 Skill 또는 통합 책임 필요 |
| Foundation·Godot 프로젝트 경계 | 공용 Method·Skill·Template | [확인] | 공용 Base에 프로젝트 고유 Scene/Node/수치/세계관 없음 | 실제 프로젝트 적용 때 별도 감사 필요 |
| Learning Log 근거 중심 | `skills/SKILL_LEARNING_LOG.md`, Skill evolution Method | [검증] | 구조 회귀 테스트 | 한 번의 성공·미검증 추측 자동 승격 금지 |
| 개발 게이트 증거 | Development Gates Method·템플릿 | [검증] | 게이트 계약 구조 회귀 테스트 | 실제 프로젝트 테스트 증거가 없으면 통과 불가 |
| 콜드 스타트 최소 라우팅 | Cold Start Test·START_HERE·두 Registry | [부분 반영] | 시작 경로와 질문·판정 템플릿 확인 | 독립된 새 Codex 작업 실험은 `[미검증]` |
| 필요한 파일·도구·권한 요청 | `AGENTS.md`, 설치·검증 Skill, preflight | [검증] | 누락 환경 계약 회귀 테스트와 복구 명령 출력 | 권한은 필요할 때 사용자 승인 필요 |
| Branch protection·Required Check | GitHub 저장소 설정 | [확인] | 인증된 API: `main` 보호 없음, ruleset 0개 | 설정 변경은 승인 범위 밖 |

상태는 `[확인]`, `[검증]`, `[부분 반영]`, `[누락]`, `[미검증]`만 사용했다.

## 3. 잘 잡힌 방향

- 한 문서에 Markdown 또는 JSON 책임 원본 하나만 두고 PDF를 사람용 최신 열람본으로 상시 동기화한다.
- PDF 최신성과 자동 렌더, Codex 시각 검수, 사용자 사람 검수를 독립 상태로 유지한다.
- 기존 프로젝트는 감사·보존 대조·승인 전까지 경로·원본·분야를 강제 변경하지 않는다.
- 11개 분야는 공용 카탈로그이며 프로젝트가 선택한 분야만 진입 Skill 또는 통합 책임을 요구한다.
- Base는 공용 방법·스킬·템플릿·검증만 소유하고 Godot 버전·Scene·Node·Resource·Signal·GDScript·수치·세계관은 프로젝트가 소유한다.

## 4. 누락 사항

- 독립된 새 Codex 작업으로 실행한 콜드 스타트 결과는 없다. 구조와 재현 시험서는 구현했지만 실제 새 작업 증거가 없으므로 `[미검증]`이다.
- 사용자 본인의 PDF 시각 검수는 요청되지 않았으며 `human_visual_review: NOT_RUN`이다.
- Branch protection과 Required Check는 활성화되어 있지 않다. 이 감사에서는 설정을 변경하지 않았다.

## 5. 추가·개선 권고

- 첫 실제 프로젝트 적용 때 콜드 스타트 시험을 독립 작업으로 실행하고 답변별 파일 경로·미검증 판정을 보존한다.
- `main` 보호와 Required Check 활성화 여부는 저장소 운영 정책으로 별도 승인한다.
- macOS 생성 지원이 필요해질 때 별도 CI·폰트·LibreOffice 계약을 추가한다.

## 6. 기존 정보 손실 위험

| 제거 템플릿 | schema v3 승계 위치 | 상태 | 판정 |
|---|---|---|---|
| `DISCIPLINE_BIBLE.md` | Markdown 기본 템플릿, 구조화 JSON 템플릿, Registry, PDF Method | [검증] | 목표·배경·범위·규칙·제약·검증, 상태·게이트·책임·위험·다음 행동 보존 |
| `PROJECT_SKILL_MAP.md` | `SKILL_REGISTRY.json` + 선택 자동 생성 Markdown + 필수 PDF/Manifest | [검증] | AI 라우팅 책임과 사람 요약을 분리하고 해시로 수동 변경 탐지 |
| `DISCIPLINE_PDF_PUBLICATION.md` | 공용 PDF Publication Method + 문서 Registry/Manifest | [검증] | 발행 목적·입력·출력·검수·실패 계약 보존 |
| 범용 `PUBLICATION_MANIFEST.json` | 문서별 Manifest v3 Schema | [검증] | 입력·출력·다이어그램 해시와 세 검수 상태 보존 |

승인 이미지의 Asset ID·출처·승인 상태·캡션, 보류·확인 필요·미검증, 책임·인터페이스·게이트·다음 행동은 현행 계약에서 추적한다. Git 이력에만 필요한 활성 정보는 발견되지 않았다.

## 7. PDF/DOCX 수동 검수 결과

- 대표 Markdown+Mermaid PDF 2페이지: `[검증]`.
- 대표 구조화 JSON+선택 DOCX+승인 이미지 PDF 6페이지: `[검증]`.
- Skill Map PDF 5페이지: `[검증]`.
- Codex가 총 13페이지의 제목·목차·계층·페이지 번호·기준 커밋·책임 원본·한글·표·코드·링크·이미지·Mermaid·잘림·겹침·빈 페이지를 전 페이지 확인했다.
- 승인 이미지의 Asset ID·출처·승인 상태·캡션과 Mermaid SVG/PNG 가독성을 확인했다.
- 사용자 사람 검수: `[미검증]`; Manifest 값은 `NOT_RUN`으로 유지한다.

## 8. 콜드 스타트 검증 결과

- `AGENTS → START_HERE → Active Context → Documentation Map → Registry` 최소 읽기 경로: `[검증]`.
- 전체 `skills/`를 읽지 않는 선택 라우팅: `[검증]`.
- 목적·현재 단계·다음 게이트·다음 작업·보호 대상·확정/구현/검증/미검증/보류를 묻는 재현 시험서: `[확인]`.
- 과거 채팅이 없는 실제 새 Codex 작업 실행: `[미검증]`.

## 9. 스킬·게이트 검증 결과

- Foundation 공통 절차와 프로젝트/분야 고유 지식 경계: `[검증]`.
- 선택한 분야만 진입 Skill 또는 통합 책임 요구: `[검증]`.
- 실패·중요 결정·재사용 교훈·실제 검증 중심 Learning Log: `[검증]`.
- Ready·구현·검증·문서화·완료 및 제품 게이트 분리: `[검증]`.
- 증거 없는 완료 통과 금지: `[검증]`.

## 10. 테스트와 Actions 증거

- 로컬 Windows 전체 회귀: 44 tests, 모두 성공.
- Python 문법·JSON 문법·내부 링크·whitespace: 성공.
- 동일 입력 재생성 추적 diff: 0.
- 누락 의존성·v2 schema·raw HTML·원격 이미지·stale source/generator·변조 Skill Map·부분 생성 실패 경로: 기대한 실패 확인.
- Actions run `29667114958`: Linux 실제 생성, Windows 실제 생성, whitespace 모두 성공.
- Windows CI Poppler는 `v24.08.0-0` 바이너리와 SHA-256 `58A6F9AE269756231D2F9AA6CBA39D75FEC6DEACAF3C4A50683383B5F3D5A527`을 고정한다.

## 11. GitHub Issue·Plan·Goal 추적성

- GitHub Issue는 없다.
- 작업 계약은 사용자가 승인한 직접 요청이며 PR #9·#10 본문에 목표·범위·제외·보호 대상·acceptance criteria·테스트·롤백을 기록했다.
- PR #9는 schema 전환 전 보존·운영 정합성, PR #10은 schema v3 생성·검증으로 분리했다.
- 공식 태그·Release와 Branch protection 변경은 별도 사용자 승인 범위다.

## 12. 병합 차단 항목

- P0: 없음.
- P1: PR #10 최종 Actions가 모두 성공해야 한다.
- P2: 실제 독립 콜드 스타트 시험, Branch protection·Required Check 활성화 여부 결정, 공식 v3.0.0 태그·Release.

## 13. 최종 결론

- 지금 병합해도 되는가: PR #10 최종 Actions 성공 후 가능.
- 병합 전에 반드시 해결할 것: 최종 Linux·Windows 실제 생성과 whitespace 성공 확인.
- 후속 작업으로 분리 가능한 것: 실제 독립 콜드 스타트, Branch protection·Required Check, 공식 태그·Release, macOS 지원.
- 사용자가 결정해야 할 것: 사람 PDF 검수 실행 시점, Branch protection 활성화, 공식 v3.0.0 Release 발행 여부.
