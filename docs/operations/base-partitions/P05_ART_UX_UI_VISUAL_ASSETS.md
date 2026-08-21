# P05 · Art, UX/UI & Visual Assets — Context Pack

## 현재 실행 계약
`SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS` · `PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER` · `OPEN_PR_READ_ONLY_BY_DEFAULT`

이 Part는 semantic responsibility / learning / validation checkpoint다. 현재 coordinator가 다른 Part/CP0의 merged-main 오류·충돌·누락을 발견하면 `CROSS_PART_CHANGE`로 owner를 기록해 수정할 수 있다. 모든 open/draft/ready PR·branch는 read-only이며 mutation은 사용자가 PR 번호와 허용 동작을 명시한 경우에만 가능하다.

## 역할
아트 방향·이미지 생성/편집·UX/UI·시각 자산 일관성/재사용·Notion visual flow와 폐기 시각 도구 흡수를 책임진다.

## 핵심 Skill
`designing-art-prompts-and-technique-cards`, `auditing-and-refining-ui-art`, `building-project-visual-dashboards`.

## 중요 규칙
`RELEASE_NEAR_VERTICAL_SLICE_FIRST`, `SYSTEM_ONLY_POC_NOT_PLAYER_EXPERIENCE_EVIDENCE`, Project Notion placement + readback, PROJECT_ASSET_APPROVED, identity-preserving edit, LEGACY_ABSORB_VERIFY_REMOVE.

플레이어 경험 검증에 들어가는 Slice는 **실제 게임 사용 후보**인 UI/UX·이미지/아트·애니메이션/연출·음악/효과음·VFX/피드백을 핵심 시스템/콘텐츠와 연결한다. 플레이어가 보는·듣는·조작하는 경로에 임시 `player-facing placeholder`나 dummy presentation을 남기지 않는다. 시스템-only PoC는 기술 evidence일 뿐 시각적 몰입·가독성·첫인상·전체 UX PASS가 아니다.

## 핵심 Module
Art Direction → Candidate Image → Visual QA → UX/UI → Notion Asset/Flow → PROJECT_ASSET_APPROVED → Reuse/Structure → Complete Release-near Vertical Slice → Runtime Visual Evidence → Retired Tool Absorption.

## 경계
Part 경계는 수정 금지선이 아니라 semantic owner 지도다. 다른 Part/CP0 finding도 현재 coordinator가 증거와 검증 경로를 확보하면 직접 수정한다. 다른 독립 **실제 활성** workstream만 read-only로 보호하며, 실제 조정 blocker만 `CROSS_PART_CHANGE_REQUEST`로 남긴다.

## 우선 공격 대상
AI 티/스타일 drift/가독성 저하, 시스템-only/회색박스만으로 player-facing 데모 최종판정, player-facing placeholder 잔존, Figma/HTML/local Tool 권위 부활, unique 기능 흡수 없는 삭제.

## 검증/완료
visual/BCA 회귀 + scope 검사 + 실제 Notion readback이 필요한 변경은 readback 증거. 최소 5회 **전체 lifecycle** 적대적 검토 후 clean까지. 관점 5개를 5회로 세지 않는다.

## 학습 루프
- 작업마다 `docs/operations/base-partitions/learning/P05_LEARNING_LOG.md`에 Learning Checkpoint를 남긴다.
- 새 공용 교훈이 없으면 `NO_NEW_REUSABLE_LESSON`; 프로젝트 전용이면 `PROJECT_ONLY`; Base 승격 후보면 `BASE_PROMOTION_CANDIDATE`.
- 주기 Source domains: GAME_DEVELOPMENT.
- 전역 Periodic Source Scan Queue에서 기존 Source 새/변경 자료와 신규 관련 사이트를 탐색하고, 원출처 검증 전에는 `UNVERIFIED_DISCOVERY`로 유지한다.
