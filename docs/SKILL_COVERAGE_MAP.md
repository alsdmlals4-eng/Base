# Source Text → Base Skill Coverage

이 문서는 사용자가 제공한 학습 텍스트의 작업 책임을 활성 Skill에 매핑한다. 개념마다 파일을 만들지 않고 **독립 입력·산출물·권한·검증 경계**가 있을 때만 새 Skill로 분리한다. 기계 검증 원본은 `skills/SKILL_COVERAGE.json`이다.

## 새 독립 Skill

| 책임 | Skill | 분리 이유 |
|---|---|---|
| 로컬·GitHub 상태 동기화 | `synchronizing-local-and-github-state` | Git 상태·권한·충돌·손실 방지 계약이 독립적임 |
| 행동 보존 리팩토링 | `refactoring-with-contract-preservation` | baseline·호환성·회귀 증거가 필요함 |
| 장기 작업 연속성 | `maintaining-long-running-task-continuity` | checkpoint·재개·부분 전달 상태가 독립적임 |
| Skill 본문 간소화 | `simplifying-skill-bodies` | 점진적 공개와 reference 발견성 검증이 필요함 |
| 죽은 자료 가지치기 | `pruning-stale-and-nonfunctional-material` | 역참조·고유 기능·삭제 승인·롤백이 필요함 |
| Games User Research 11영역 | `governing-game-user-research-coverage` | 설치·coverage·증거 상태 감사가 독립적임 |
| 사용자 학습 노트 | `creating-user-learning-notes` | 학습 독자·설명·연습 산출물이 운영 지침과 다름 |
| 프로젝트 시각 대시보드 | `building-project-visual-dashboards` | 시각 작업 공간·원본 연결·상태 바인딩이 독립적임 |
| 엔진 런타임 디버깅 | `diagnosing-game-engine-runtime-failures` | 재현·원인 격리·최소 수정·엔진 재검증이 독립적임 |

## 기존 Skill에 유지한 책임

- 모호한 요청→실행 계약, Issue·Goal·Plan, 작업 분해: `managing-project-intake-and-work-contract`.
- Grill Me 한 질문 인터뷰·권장안·결정 원장·종료 판정: `managing-project-intake-and-work-contract`의 `clarify` Mode와 `grill-me-protocol.md`.
- 플레이어 경험·벤치마킹·MVP·PoC·플레이테스트: `analyzing-and-refining-game-concepts`.
- 프로젝트 코어 사실 판정과 승인 확정: `identifying-project-core`, `establishing-project-core`.
- 문서 기억·정본·단계별 컨텍스트 압축: `managing-design-documents`, `maintaining-project-context-and-handoff`.
- GPT 비-Godot 완료→Codex 읽기 전용 Plan→단계별 Godot 구현→GPT 검수→사용자 병합 승인: `maintaining-project-context-and-handoff`의 `implementation-package-handoff` Mode.
- 다중 관점 공격·개선: `running-adversarial-review-and-refinement`.
- 실제 diff·테스트·완료 증거: `reviewing-and-validating-project-changes`.
- 변경 유형별 CI 계층, GitHub Actions 비용 절감, concurrency·`ci-gate`, Actions 차단 시 보류 상태: `reviewing-and-validating-project-changes`의 `ci-cost-optimization` Mode.
- Skill 생성·통합·학습: `evolving-project-discipline-skills`.

## Base 자체 적용 순서

```text
coverage inventory
→ pruning-stale-and-nonfunctional-material
→ simplifying-skill-bodies
→ refactoring-with-contract-preservation
→ running-adversarial-review-and-refinement
→ reviewing-and-validating-project-changes
→ auditing-canonical-reference-freshness
→ PR checks
```
