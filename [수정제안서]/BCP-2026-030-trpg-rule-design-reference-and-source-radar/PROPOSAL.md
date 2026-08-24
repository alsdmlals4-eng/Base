# BCP-2026-030 — TRPG rule-design reference & source radar

## 출처와 상태

- 출처 프로젝트: `이클립스 TRPG` 기획 작업 + 공개 TRPG 룰북/SRD/출판사 자료 벤치마크
- 기준 Base 커밋: `7de18bc6a941b7be11e747f1cf59ae60cb3e4657`
- 외부 자료 확인일: `2026-08-24`
- 제출일: `2026-08-24`
- 상태: `UNDER_REVIEW`
- 지식 상태: `다중 원출처 관찰 + 공용 패턴 후보`
- 사용자 방향 근거: 2026-08-24 현재 작업 대화에서 사용자가 TRPG 자료를 Base에 추가하고 더 많은 참고 링크를 조사하도록 명시함.

## 관찰과 증거

세부 Source Record와 관찰은 `evidence/TRPG_SOURCE_SCAN_2026-08-24.md`에 둔다.

핵심 관찰은 다음과 같다.

1. **Fiction → trigger → rule → fiction**: Dungeon World 공개판은 대화 속 허구에서 발동 조건이 성립할 때 Move/액션이 발동하고, 결과를 다시 허구에 반영하는 구조를 명시한다. 장비 태그도 단순 수치가 아니라 어떤 행동이 가능한지와 실패 결과의 힌트를 제공한다.
2. **Player-facing / GM-facing / reference 분리**: Dungeon World, Fate, TRPG Club 자료실, Blades의 player kit 등은 룰북 본문과 캐릭터/요약/시나리오/관리 시트를 역할별로 분리한다.
3. **Character truth와 mechanical effect 분리**: Fate의 aspect/stunt 계열, 다수의 공개 SRD와 현재 이클립스 설계에서 '무엇이 사실인가'와 '그 사실이 어떤 규칙 효과를 내는가'를 분리하면 자유도와 판정 명료성을 동시에 얻을 수 있다.
4. **Risk와 effect를 별도 축으로 보기**: Blades in the Dark는 Position과 Effect를 분리하고 scale/quality/potency를 통해 허구적 조건을 숫자 난이도 하나로 뭉개지 않는다. 진행 Clock은 복잡한 목표를 반복 가능한 진척 상태로 표현한다.
5. **핵심 단서 실패 봉쇄 방지**: GUMSHOE는 시나리오 진행에 필요한 Core Clue를 단일 성공 판정에 잠그지 않고, 적절한 조사 능력/방법으로 정보를 제공한 뒤 해석과 선택에 플레이를 집중시킨다.
6. **역할 비대칭과 관계 보상**: TRPG Club의 『둘이서 수사』 자료 구조와 공개 소개는 탐정/조수의 역할 차이, 관계 변화, 사건 조사 시트, 사전 조사 시트처럼 장르의 핵심 감정을 별도 규칙·시트로 지지하는 사례다.
7. **Support artifact는 룰북의 부록이 아니라 실행 인터페이스**: TRPG Club 통합 자료실은 캐릭터 시트뿐 아니라 전투/거점/시나리오/NPC/핸드아웃/규칙 요약/관리 시트를 게임별로 제공한다. 룰북을 잘 쓰는 것과 실제 세션에서 필요한 보조 자료를 설계하는 것은 별도 책임이다.
8. **Rules-light reference value**: Fate Condensed, 24XX, Lasers & Feelings 같은 경량 자료는 핵심 플레이 루프와 판정 언어를 짧고 검색 가능하게 유지하는 가치가 있다. 반대로 범용 룰의 확장 가능성은 optional module로 분리하는 편이 읽기 비용을 줄인다.
9. **SRD와 제품의 권리 경계**: Fate/Blades/24XX/Dungeon World처럼 CC 계열로 명시된 SRD와, TRPG Club의 상용 작품/부속 자료처럼 관찰만 가능한 자료를 같은 재사용 권한으로 취급하면 안 된다. Year Zero Engine처럼 전용 라이선스가 있는 경우도 해당 계약 범위만 사용해야 한다.
10. **VTT/ORPG는 룰과 별도 UX 층**: `adventurekeeper`의 Naver 글은 직접 접근이 차단됐지만 외부 색인에서 코코포리아 가이드로 식별된다. 이 계열 자료는 판정 규칙보다 장면 전환·캐릭터 표현·BGM·로그·자동화 수준 등 온라인 세션 운영 UX 참고로 분리해야 한다.

## 일반화 후보

새로운 광역 Skill을 만들지 않는다. 기존 game-development knowledge hub와 benchmark/reuse pipeline의 조건부 reference로 다음 두 문서를 추가하는 안을 제안한다.

1. `docs/knowledge/game-development/TRPG_RULE_DESIGN_AND_PLAY_REFERENCE.md`
   - TRPG 설계 질문을 `PLAYER_PROMISE → FICTIONAL_PERMISSION → RESOLUTION → CONSEQUENCE → RESOURCE_LOOP → SCENE/CAMPAIGN_LOOP → GM_PROCEDURE → SUPPORT_ARTIFACT`로 분해한다.
   - 장르와 시스템에 따라 `ADOPT / ADAPT / REJECT / TEST / REFERENCE_ONLY`로 적용한다.
   - '한 시스템을 통째로 복제'하지 않고 장르별 해결 문제와 실패 조건을 기록한다.
2. `docs/knowledge/game-development/TRPG_REFERENCE_SOURCE_RADAR.md`
   - 한국어/영어 공개 룰북·SRD·출판사 자료·VTT 가이드를 source tier, 접근 상태, 권리 상태, 주요 사용처로 관리한다.
   - exact source access가 불가능하면 `UNVERIFIED_DIRECT`로 남기고 검색 스니펫이나 기억으로 내용을 확정하지 않는다.

재사용 가능한 설계 계약 후보:

- `FICTION_FIRST_TRIGGER_CONTRACT`: 허구의 선언이 규칙 발동 조건을 충족할 때만 판정하고 결과를 다시 허구에 반영한다.
- `FICTIONAL_PERMISSION_BEFORE_MODIFIER`: 능력·태그·장비·면모가 무엇을 가능/불가능하게 하는지 먼저 정하고, 그 뒤 수치 보정을 적용한다.
- `CORE_INFORMATION_MUST_NOT_BE_SINGLE_ROLL_GATED`: 진행에 필수인 정보는 단일 성공 굴림 실패로 영구 봉쇄하지 않는다.
- `RISK_AND_EFFECT_ARE_DISTINCT`: 위험의 크기와 목표에 미치는 효과의 크기를 가능하면 분리해 판단한다.
- `SUPPORT_ARTIFACT_IS_PLAY_INTERFACE`: 캐릭터 시트, 규칙 요약, 시나리오/전투/세력/NPC/단서 관리 시트를 실제 세션 인터페이스로 설계한다.
- `ROLE_ASYMMETRY_REQUIRES_RECIPROCAL_VALUE`: 역할이 비대칭이면 각 역할이 서로 다른 방식으로 핵심 경험에 기여하고 보상을 받도록 설계한다.
- `COMPACT_CORE_OPTIONAL_MODULES`: 첫 세션에 필요한 core와 campaign/advanced option을 분리해 학습 비용을 관리한다.
- `SRD_RIGHTS_BOUNDARY`: 관찰 가능한 디자인 원리와 실제 재사용 가능한 텍스트/도표/상표/자산의 권리를 분리한다.
- `VTT_IS_PRESENTATION_AND_OPERATION_LAYER`: Roll20/Cocofolia/Foundry류의 온라인 운영 특성은 룰 엔진과 별도 축으로 평가한다.

## 프로젝트 전용으로 남길 내용

다음은 Base에 넣지 않는다.

- 이클립스 세계관, 세력, 균열, 마석, 캐릭터 예시, 능력치 수치, 스킬 수치.
- 특정 프로젝트 Google Sheet의 셀 구조와 승인 상태.
- 상용 TRPG의 고유 문구, 고유 데이터 표, 캐릭터/카드/시트 원본 이미지.
- 특정 VTT의 프로젝트별 방 세팅, 이미지, 매크로, 계정 정보.

Base는 **공용 설계 질문·출처 지도·권리 경계·벤치마크 패턴**만 소유한다.

## 적용 조건과 비사용 조건

적용 조건:

- 새로운 TRPG/보드형 RPG 규칙을 설계하거나 기존 시스템을 크게 개조할 때.
- 캐릭터 생성, 판정, 전투, 조사, 관계, 성장, GM 절차, 보조 시트를 비교할 때.
- 공개 SRD나 상용 룰북을 벤치마킹하여 재사용 가능한 원리만 추출할 때.
- 온라인/오프라인 세션 인터페이스를 함께 설계할 때.

비사용 조건:

- 디지털 액션게임처럼 tabletop conversation/procedure가 핵심이 아닌 시스템에 그대로 적용하지 않는다.
- 특정 장르의 장치(비밀 카드, Core Clue, Position/Effect, Aspect)를 모든 TRPG의 필수 규칙으로 강제하지 않는다.
- 상용 자료에서 관찰한 문구·수치·표를 권리 확인 없이 복제하지 않는다.
- 공개 라이선스가 있어도 상표, 로고, Product Identity, 아트 권리가 동일하게 열려 있다고 가정하지 않는다.

## 반례와 위험

### 최소 3안 비교

| 안 | 장점 | 위험·비용 | 판정 |
| --- | --- | --- | --- |
| A. 이클립스 프로젝트 시트에만 참고 링크를 축적 | 즉시 사용 가능 | 다른 TRPG 프로젝트가 같은 조사를 반복, 공용 권리/설계 원리 축적 안 됨 | `REJECT` |
| B. Base에 특정 TRPG별 긴 요약/룰 복사본을 저장 | 검색은 쉬움 | 저작권·라이선스 위험, stale copy, 컨텍스트 비용, 특정 시스템 편향 | `REJECT` |
| C. Base에 공용 설계 Guide + Source Radar를 두고 프로젝트는 필요한 source만 선택 로드 | 재사용성·권리 경계·컨텍스트 비용 균형 | source freshness 관리가 필요 | `ADOPT` |

주요 위험:

1. **Cargo-cult 위험**: 유명 시스템의 메커닉을 문제 정의 없이 가져오면 게임의 핵심 감정과 어긋난다.
2. **라이선스 혼동**: '무료 공개'와 '자유 변형/상업 이용 가능'은 다르다. Source Radar에 권리 상태를 별도 필드로 둔다.
3. **한국어 2차 자료 과신**: 블로그/커뮤니티 요약은 discovery에는 유용하지만 규칙 정본이나 라이선스 판단은 공식/원문으로 역추적한다.
4. **보조 시트 과잉**: TRPG Club의 많은 보조 자료를 보고 모든 프로젝트에 동일 수의 시트를 만들면 관리량이 폭증한다. 실제 반복 절차가 있을 때만 분리한다.
5. **2d6/PbtA 과적합**: Dungeon World/현재 이클립스의 2d6 결과 구간은 한 사례군이다. d20, dice pool, diceless 등 다른 해법과 비교 후 프로젝트별 선택한다.
6. **Fate 과적합**: 면모/서사점은 서사 중심 플레이에 강하지만 tactical resource planning이나 mystery certainty를 그대로 대체하지 않는다.
7. **직접 접근 실패**: Dropbox exact folder와 Naver `adventurekeeper`는 현재 web 도구로 직접 읽히지 않았다. 각각 공식 주변 출처/2차 색인으로 존재 목적만 확인했으며 세부 내용은 확정하지 않는다.

## 영향 범위와 검증

승인 시 최소 구현 범위:

- 새 Guide 1개: `TRPG_RULE_DESIGN_AND_PLAY_REFERENCE.md`
- 새 Source Radar 1개: `TRPG_REFERENCE_SOURCE_RADAR.md`
- `docs/knowledge/game-development/README.md`에 조건부 routing 1행 추가.
- `docs/knowledge/game-development/REFERENCE_SOURCE_CATALOG.md`에는 장기 권위가 높은 공식/open source만 최소 entry로 연결하거나 Source Radar를 owner로 라우팅.
- 새 Skill, 새 Tool, 새 dependency, scheduler, runtime 변경 없음.

검증:

1. 프로젝트 고유 이클립스 명칭·수치가 active Base guide에 남지 않는지 검색.
2. Source Radar의 각 source에 `source_tier`, `access_status`, `rights_status`, `use_for`, `limitations`, `recheck_condition`이 있는지 확인.
3. 공식/CC source와 상용/reference-only source가 구분되는지 확인.
4. 기존 benchmark/reverse-engineering owner와 중복되는 새 workflow를 만들지 않았는지 확인.
5. 최소 5회 full-scope adversarial review 후 blocking finding 0일 때만 구현 merge.

## 필요한 도구·파일·권한

- 필요 항목: 기존 GitHub 문서/PR/Actions + 공개 웹 자료.
- 필요한 이유: 공용 TRPG reference를 Base knowledge owner에 추가하고 provenance를 추적하기 위해 필요.
- 설치·적용 방법: 신규 설치 없음. branch/PR을 사용한 문서 변경만 수행.
- 설치 후 확인 명령: 해당 없음. 구현 PR에서는 repository 문서 회귀/검증 경로를 사용.
- 최소 권한: 정상 branch/PR/squash merge. `--admin`, ruleset bypass, force push 불필요.
- 추가 금전 비용: `0`.

## 승인과 구현

- 사용자 승인 근거: 2026-08-24 현재 작업 대화의 `base에 trpg 자료로 추가하고. 더 많은 링크를 찾아봐` 및 뒤이은 5개 링크 재확인 지시.
- 현재 lifecycle 해석: **Base 추가 방향은 사용자 승인됨.** 다만 Base 규칙에 따라 제안 PR → 승인 상태 PR → 구현 PR의 경계를 분리한다.
- 구현 PR: `없음 — proposal/approval lifecycle 이후 별도 생성`
- 롤백: 승인 전에는 `[수정제안서]/**`만 제거하면 active Base 동작은 변하지 않는다. 구현 후에는 Guide/Source Radar/라우팅 entry만 되돌리며 Skill·runtime migration은 없다.
