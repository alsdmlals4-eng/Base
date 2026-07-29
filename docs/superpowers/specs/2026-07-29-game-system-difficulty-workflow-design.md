# 게임 시스템·난이도·전투 AI 설계 구조

## 1. 목표

게임 시스템, 적 전투 AI, 고정·적응형 난이도를 플레이어 경험과 검증 증거에 연결하는 공용 설계 절차를 Base에 추가한다. 프로젝트는 기능·수치 목록이 아니라 `플레이어 경험 목표 → 시스템 경계 → 행동·선택·결과 → 공정성 → 압박·회복 페이싱 → 난이도 변수 → 텔레메트리·플레이테스트`를 한 계약으로 작성해야 한다.

## 2. 현행 구조 분석

### 2.1 권한·라우팅

- `AGENTS.md`는 새 Skill을 만들기 전에 기존 통합 Skill의 Skill Mode로 처리할 수 있는지 먼저 확인하도록 강제한다.
- `skills/SKILL_REGISTRY.json`은 주 책임 분야 Skill을 최대 하나만 선택한다.
- `analyzing-and-refining-game-concepts`가 핵심 컨셉·제약·게임 요소 정렬·벤치마크·플레이테스트·PoC·재조정의 단일 기획 전략 책임을 가진다.
- `GAME_DESIGN_AND_PLAYER_EXPERIENCE_GUIDE.md`는 이미 난이도·실패·복구를 다루지만, 게임 시스템 경계·전투 조율·긴장도·DDA의 실행 계약은 부족하다.

### 2.2 중복 위험

`designing-game-difficulty` 또는 `designing-combat-ai` 같은 새 Specialist Skill을 추가하면 다음 책임이 겹친다.

- 플레이어 경험·핵심 재미 정렬
- 벤치마크·플레이어 근거
- 플레이테스트·텔레메트리
- PoC·Production Gate

따라서 새 독립 Skill은 만들지 않는다.

### 2.3 채택 구조

```text
analyzing-and-refining-game-concepts
├─ 기존: frame / constrain / sharpen / structure / analyze
├─ 신규: system-design
├─ 신규: difficulty-and-combat-ai
├─ 기존: benchmark-and-player-research
├─ 기존: playtest-and-experiment / poc-contract / recalibrate / production-gate
└─ reference: game-system-difficulty-and-combat-ai.md
```

프로젝트별 실제 설계값은 `GAME_SYSTEM_DIFFICULTY_AND_COMBAT_AI_CONTRACT.md`를 복사해 해당 프로젝트의 등록된 기획 책임 원본에 통합한다. Template 자체는 프로젝트 정본이 아니다.

## 3. 책임 경계

### `system-design`

- 플레이어 경험 목표와 시스템 목적
- 입력·행동·자원·상태·규칙·피드백·결과
- 시스템 경계와 인접 시스템 인터페이스
- 정상·실패·경계 상태
- 접근성·저장·성능·콘텐츠 제작 영향
- 제거·축소·통합 우선순위

### `difficulty-and-combat-ai`

- 난이도 장벽 프로필
- 공정성·가독성·대응 가능성 안전 규칙
- 개별 적 판단, 전투 조율자, 난이도·페이싱 디렉터의 분리
- 공격·위협 예산과 동시 공격 제한
- 반응시간·예고·회복·의도적 빗나감
- Build Up → Sustain Peak → Peak Fade → Relax 긴장도 곡선
- 고정 난이도와 적응형 난이도 변수
- 장기 실력과 단기 스트레스의 분리
- 히스테리시스·변경 쿨다운·적용 시점
- 텔레메트리·플레이테스트·롤백

### 다른 Skill로 넘길 책임

- 프로젝트 코어 사실 판정: `identifying-project-core`
- 프로젝트 코어 승인: `establishing-project-core`
- 기획 정본 작성·발행: `managing-design-documents`
- Vertical Slice 품질·제작 증명: `designing-vertical-slices`
- 실제 변경 검증: `reviewing-and-validating-project-changes`
- 프로젝트 전용 교훈의 Base 승격: `managing-base-change-proposals`

## 4. 핵심 설계 원칙

1. 플레이어가 느낄 경험과 기억을 먼저 정의한다.
2. 적의 지능과 전투 압박량을 분리한다.
3. 쉬움 난이도에서 적을 멍청하게 만들지 않고 반응시간·동시 공격·전술 빈도·회복 폭을 조절한다.
4. 높은 난이도에서도 정보·예고·인과·대응 가능성을 유지한다.
5. 적응형 난이도는 성공을 즉시 상쇄하지 않는다.
6. 현재 전투의 구조·체력·피해를 노골적으로 바꾸기보다 다음 웨이브·공격 예산·페이싱·지원 자원에 적용한다.
7. 한 번의 플레이 결과를 공용 강제 수치로 승격하지 않는다.

## 5. 산출물

- 기존 Skill에 신규 Skill Mode와 출력 계약 추가
- 상세 reference 1개
- 프로젝트 적용 template 1개
- Game Design Guide 확장
- START_HERE·Documentation Map·Registry 라우팅 동기화
- Change Log·Learning Log 기록
- 구조 계약 테스트

## 6. 제외 범위

- Godot 런타임 AI 코드 구현
- 특정 프로젝트의 적 체력·공격력·반응시간 확정
- 머신러닝 기반 DDA
- 프로젝트별 적 종류·행동 트리·보스 패턴 생성
- 법적 접근성 준수 인증

## 7. 완료 기준

- 새 독립 게임 난이도·전투 AI Skill ID가 없다.
- 기존 게임 기획 Skill에서 두 신규 mode를 발견할 수 있다.
- reference와 template이 실행 가능한 입력·출력·검증 필드를 가진다.
- Registry trigger와 사람용 라우팅이 같은 책임을 가리킨다.
- 난이도 설계가 공정성·긴장도·접근성·텔레메트리·플레이테스트에 연결된다.
- 관련 자동 테스트가 통과한다.

## 8. 롤백

문제가 발생하면 신규 reference·template·test를 제거하고, Skill·Registry·START_HERE·Documentation Map·Guide·Change/Learning Log를 변경 전 commit으로 되돌린다. 기존 Skill ID와 기존 mode는 변경하지 않으므로 프로젝트 호환성 손실은 없어야 한다.
