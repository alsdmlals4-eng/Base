# Base 실행 스킬

이 폴더는 여러 프로젝트에서 직접 적용할 수 있는 단계형 작업 스킬을 관리한다.

전역 productivity 스킬은 이 폴더에 복사하지 않는다. 고정 출처와 파일 해시는 `PRODUCTIVITY_SOURCE_MANIFEST.json`에서, 프로젝트별 사용 경계는 `SKILL_REGISTRY.json`에서 확인한다.

| 스킬 | Trigger |
|---|---|
| `conducting-deep-requirement-interviews` | 기능·경험·아트 방향·구조·워크플로·Base 변경 제안의 사실과 사용자 결정을 실행 전에 확정함 |
| `transforming-requests-into-prompts` | 요청이 짧거나 모호하고 범위·완료·검증이 부족함 |
| `designing-vertical-slices` | 핵심 경험과 최종 품질·제작 파이프라인을 작은 구간에서 검증함 |
| `writing-game-design-documents` | 기획서 종류, 책임 원본, 로드맵과 명세 구조를 정함 |
| `orchestrating-deepseek-worktrees` | 대용량 초안·분류를 별도 worktree의 DeepSeek 또는 외부 AI에 위임함 |
| `reviewing-external-ai-drafts` | 외부 AI·병렬 작업자의 초안과 diff를 기준 저장소 반영 전에 검수함 |
| `designing-art-prompts-and-technique-cards` | 아트·UI 시각 기술을 추천하고 생성·편집 프롬프트와 QA 카드로 기록함 |
| `auditing-and-refining-ui-art` | Godot·Web UI 결과를 A~E 영역으로 감사하고 승인된 범위만 순차 개선·독립 재검수함 |
| `promoting-project-knowledge` | 프로젝트 교훈을 Base 수정제안서로 일반화·제출함 |
| `reviewing-and-implementing-base-change-proposals` | 사용자 승인된 제안만 별도 Base 구현 PR로 진행함 |

## 배치 원칙

- 실행 절차: `skills/<name>/SKILL.md`
- 분야별 참고·능력 매트릭스: `docs/knowledge/skills/`
- 반복 가능한 판단법: `docs/knowledge/methods/`
- 조사·표준·근거 참고: `docs/knowledge/research/`
- 복사 가능한 출력 형식: `templates/`
- 구체 사례: `docs/knowledge/cases/`

새 스킬은 `docs/AI_SKILL_ADOPTION_GUIDE.md`의 검증 절차를 통과한 뒤 `검증` 상태로 표시한다. 외부 모델·플러그인 이름은 교체 가능해야 하며, 핵심 절차와 검증 계약은 도구가 없어도 적용 가능해야 한다.

프로젝트발 공용화 후보는 먼저 `[수정제안서]`에 제출한다. 제안 PR과 활성 Base 구현 PR을 분리하고 사용자 승인 전에는 공용 Method·Skill·Template을 변경하지 않는다.
