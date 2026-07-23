# BCP-2026-003 — 결정 표면·구현 전달·파생 산출물 증거 모드 보강

## 출처와 상태

- 출처 프로젝트: Ten-Paces-Hidden-Moves, Blacksmith, omenward, urban-legend, Coc-Fiction
- 기준 커밋: Base `41a20584dd2ee51d917e5c9d7cab6838e1ceba7e`; Blacksmith `519608176679399011203ec7609f232610796caa`; omenward `2670a9a0040d0618a8dfb98683076f6b4ded5c54`; urban-legend `ed2587322feb69ad43de87f5f4ef1df918a0bc7b`; Coc-Fiction `4ee143dcb218c58ebaf96e9668368090efce5a59`
- 제출일: 2026-07-23
- 상태: `SUBMITTED`
- 지식 상태: `패턴`

## 관찰과 증거

- 십보강호는 두 수 비공개 잠금·동시 공개·순차 해상과 절초 기세 HUD를 같은 플레이 약속으로 유지해야 하지만, 규칙·표시·실행 증거가 분리될 때 플레이어 신뢰가 무너질 위험이 있다.
- Blacksmith는 JSON 정본·도메인 코드·Scene·테스트를 분리해 제작·강화·피버 결과를 검증했으며, 다음 우선순위도 실패 정책 정본 통합과 수치 시뮬레이션이다. 구현자에게 정본·보호 범위·검증·문서 갱신을 한 패킷으로 넘기는 작업이 반복됐다.
- omenward는 C1·C2 자동 검증이 끝났어도 첫 10분의 건설→룰렛→배치→역전과 사람 플레이는 미증명이다. 전장·룰렛·HUD는 플레이어가 그 순간 내려야 할 결정을 중심으로 명세화해야 한다.
- urban-legend는 전조→가설→근거→대응의 페어플레이 추리와 후보·공식 규칙·위험 사례의 기록 상태를 연결한다. 준비·조사·결과 화면의 정보 위계가 설계와 구현 계약 모두에 필요하다.
- Coc-Fiction은 225화 장편을 수정할 때 원고뿐 아니라 색인·역개요·Scene Pass Registry·Revision Report를 같은 PR에서 재생성해 파생 산출물의 기준 SHA를 보존한다.

## 일반화 후보

새 독립 Skill을 추가하지 않고, 다음 기존 통합 Skill에 선택적 mode와 템플릿을 보강한다.

1. `managing-project-intake-and-work-contract`의 `implementation-handoff-packet`
   - Goal, 플레이어 가치, 현행 정본·실제 파일, 보호·제외 범위, 결정 보류, 정확한 검증 순서, 문서 갱신, 구형 참조 검색, 중단 조건을 한 작업 패킷으로 만든다.
   - GPT의 기획 결과를 Codex·HiGodot 구현 계약으로 넘길 때만 사용한다. 짧은 오탈자나 단일 검사 재실행에는 사용하지 않는다.
2. `managing-design-documents`의 `decision-surface-spec`
   - 플레이어가 지금 답해야 할 질문, 보이는 근거, 선택지·비용, 숨겨야 할 정보, 상태 소유자, 피드백, 실패·복구, 입력·접근성 폴백을 한 표로 명세화한다.
   - 전투 HUD, 조사 판단, 룰렛·배치, 결과·기록처럼 플레이 중 판단을 바꾸는 화면에만 사용한다. 단순 장식·비상호작용 소개 화면에는 사용하지 않는다.
3. `auditing-canonical-reference-freshness`의 `derived-artifact-provenance`
   - 생성·합성된 DOCX/PDF, 색인, 역개요, 대시보드, 검증 보고서에 입력 원본·기준 커밋/SHA·생성 도구·범위·검증 상태를 연결하고, 원본 변경 뒤 stale 파생본을 찾는다.
   - 파생물이 실제 의사결정·인수인계·검증에 쓰일 때만 사용한다. 단순 임시 미리보기나 Git 이력만으로 충분한 파일에는 강제하지 않는다.

## 프로젝트 전용으로 남길 내용

- 십보강호의 10칸·두 수·합·절초 수치와 무협 표현.
- Blacksmith의 강화 단계·피버 배율·Android 규격·JSON 경로.
- omenward의 3라인·건설 노드·룰렛·공용 10병종·웨이브.
- 괴이 기록국의 용어, 사건 규칙, 저장 키, 매뉴얼 상태와 에피소드 ID.
- Coc-Fiction의 작품명, 225화 구성, 인물·Canon·원고 경로.

## 적용 조건과 비사용 조건

- 적용 전 기존 mode와 출력 계약이 실제로 부족한지 확인한다. 같은 책임을 새 Skill ID로 중복하지 않는다.
- `implementation-handoff-packet`은 사용자 승인 전 구현 권한을 만들지 않는다.
- `decision-surface-spec`은 UI가 게임 상태를 직접 소유하도록 허용하지 않는다.
- `derived-artifact-provenance`는 파생 파일을 두 번째 정본으로 만들지 않는다.

## 반례와 위험

- 전달 패킷이 장황해져 작은 변경의 속도를 해치거나, 사람이 아닌 자동화에 판단을 떠넘길 수 있다.
- 결정 표면 표가 모든 UI를 같은 레이아웃으로 평준화할 수 있다.
- SHA·생성기 기록이 수동 작업을 과도하게 부담시킬 수 있다.
- 따라서 세 mode 모두 trigger 기반 선택형으로 두고, 필요한 최소 필드와 PASS/PARTIAL/NOT_RUN 증거만 요구한다.

## 영향 범위와 검증

- 영향 대상: 세 기존 Skill 본문·Registry trigger/skill mode·작업 계약/결정 표면/파생 산출물 템플릿·대표 회귀 테스트.
- 비영향 대상: 프로젝트 고유 Skill, 게임 규칙, 기존 문서 구조, 활성 Base 책임의 자동 마이그레이션.
- 검증: 각 mode에 게임 전투 HUD, 조사 판단 UI, 코드 구현 전달, 장편 원고 파생 색인, 단순 문서 수정의 비사용 사례를 둔다. Registry와 alias, template, stale-reference 검사, 기존 운영체계 회귀를 실행한다.
- 롤백: mode·template·trigger만 별도 커밋으로 되돌리고, 프로젝트별 기존 정본과 생성물은 변경하지 않는다.

## 승인과 구현

- 사용자 승인 근거: `미승인`
- 구현 PR: `없음`
- 롤백: 승인 후 별도 구현 PR의 mode·template·test 범위만 되돌린다.
