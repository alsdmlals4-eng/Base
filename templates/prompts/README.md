# Base 공용 실행 지시문

이 폴더는 Base의 현행 Skill·정책을 실제 작업 요청에 연결하는 공용 Prompt를 보관한다. Prompt는 최신 사용자 지시, 대상 프로젝트의 정본·실제 파일, 프로젝트에 고정된 Base Adapter보다 높은 권한이 아니다.

## 현행 사용 경로

| 지시문 | 사용 목적 | 주 실행 경로 |
|---|---|---|
| `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md` | 저장소 우선 인터뷰부터 기획·Demo-First Vertical Slice·GPT→Codex 인계·구현·검수까지 하나의 첨부 파일로 전달 | 프로젝트 Intake·운영·기획·구현·검수 Skill 조합 |
| `PROJECT_ADAPTIVE_INGAME_ART_CHECKPOINT_PROMPT.md` | 대상 프로젝트를 먼저 조사하고 핵심 장면 구성을 Grill Me로 승인받은 뒤, 인게임 이미지와 비주얼 보드를 제작·검수 | `designing-art-prompts-and-technique-cards: intermediate-visual-checkpoint` + UI/UX·적대적 검토 |

## 프로젝트 적응형 인게임 아트 지시문

`PROJECT_ADAPTIVE_INGAME_ART_CHECKPOINT_PROMPT.md`는 다음 요청에 사용한다.

- 프로젝트별 인게임 화면·핵심 장면을 이미지로 중간 점검
- 프로젝트 코어와 실제 화면 흐름을 반영한 비주얼 보드 제작
- 캐릭터·배경·UI·카메라·그림체 일관성 점검
- 전투·추리·경영·서사 등 프로젝트 고유의 결정적 순간 시각화

핵심 Gate:

```text
프로젝트 정본·실제 파일·열린 PR·최근 병합 PR 확인
→ 프로젝트별 장면 후보 선정
→ Grill Me 화면 구성 승인
→ 승인 장면 개별 생성
→ 보드 편성
→ 적대적 검토·회귀 재점검
→ 사용자에게 최종 이미지 보드 우선 제공
```

모든 프로젝트에 메인·전투·인벤토리·결과 같은 고정 화면 세트를 강제하지 않는다. 이미지 생성은 장면 구성 승인 뒤에만 시작하며, 생성 결과는 기본 `DRAFT_VISUAL`이다.

## 구형·호환 지시문

`VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md`와 `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md`는 과거 계약 복원과 호환성 확인용이다. 신규 작업의 현행 통합 진입점으로 사용하지 않는다.

## 사용 전 확인

1. Base `START_HERE.md`, `AGENTS.md`, `docs/WORK_MODE_AND_SKILL_ROUTING.md`에서 현재 요청의 Skill·Skill Mode를 선택한다.
2. 대상 프로젝트의 `AGENTS.md`, 현재 상태, 문서 지도, 최신 Decision, 실제 코드·데이터·Scene·Resource·자산·테스트를 확인한다.
3. Prompt와 프로젝트 정본이 충돌하면 프로젝트 정본을 우선하고 `STALE_PROMPT_CONTRACT` 또는 해당 충돌 상태를 보고한다.
4. 실행하지 않은 검증은 `PASS`나 완료로 표시하지 않는다.
