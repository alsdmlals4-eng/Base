# BCP-2026-030 — TRPG 룰 설계 벤치마크·룰북 설명 구조 Reference Radar

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base` + 이클립스 TRPG 기획 작업 + 공개 TRPG 공식/SRD/Quickstart 벤치마크
- 기준 Base 커밋: `7de18bc6a941b7be11e747f1cf59ae60cb3e4657`
- 제안 병합 기준: `4c51250b7cf12b43b3baa70916ad6646ab733fa4` / PR `#651`
- 외부 자료 확인일: `2026-08-24`
- 제출일: `2026-08-24`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 지식 상태: `다중 공식/SRD/공개판 관찰 + 사용자 승인 공용 분석 프레임 + 구현 전 검증 완료`

## 관찰과 증거

사용자는 새 TRPG를 설계하면서 다음 핵심 목표를 밝혔다.

- RP에서는 Fate 계열의 `면모`처럼 서사적 사실과 캐릭터 정체성을 사건 해결에 직접 사용한다.
- 전투에서는 고정 스킬 목록보다 플레이어가 직접 작성한 능력/스킬을 사용해 공격·제압·기동·지원 등 여러 해결책을 만든다.
- 규칙은 지나치게 복잡하지 않되 다양한 캐릭터와 플레이를 허용한다.
- 실제 룰북은 사람이 읽기 쉬워야 하며, 각 룰북이 무엇을 어떤 순서로 가르치는지도 벤치마킹한다.
- 사용자가 추후 제공할 룰북 ZIP도 각 파일의 특징뿐 아니라 **어떤 플레이 문제를 어떤 규칙으로 풀었는지, 개념을 어떤 순서로 처음 소개·예시·심화·레퍼런스화하는지**까지 같은 기준으로 분석한다.

상세 Evidence:

- `evidence/TRPG_SOURCE_SCAN_2026-08-24.md` — 사용자 지정 국내 source + materially distinct 공개 TRPG의 특징, 해결 방식, 설명 순서, support artifact 비교.
- `evidence/TRPG_SOURCE_RIGHTS_AND_FRONTIER_ADDENDUM_2026-08-24.md` — exact official URL, 라이선스/권리 경계, BRP 추가 대조군, 사용자 지정 5개 링크 coverage.
- `evidence/ADVERSARIAL_REVIEW_2026-08-24.md` — proposal 범위에 대한 5회 full-scope 적대 검토와 수정 기록.

Base의 현행 `docs/knowledge/game-development/README.md`, `REFERENCE_SOURCE_CATALOG.md`, `PERIODIC_SPECIALTY_SOURCE_RADAR.md`에는 게임 설계·외부 Source 검증을 위한 공통 구조는 있으나, TRPG 룰 시스템·룰북 설명 구조를 설계 질문별로 비교하는 전용 Reference는 없다.

2026-08-24 조사에서 다음 서로 다른 설계 계열을 비교했다.

- Fate Condensed/Core — 면모, 서사적 허가, invoke/compel, create advantage.
- Dungeon World / PbtA — fiction trigger → move → 결과를 다시 fiction에 반영, GM agenda/principles/moves.
- Blades in the Dark — action choice 뒤 Position과 Effect를 분리해 위험과 성과를 조정, Clock과 player kit.
- 13th Age — 자유작성 Background와 One Unique Thing, 한 판정에 관련 Background 하나.
- GUMSHOE — 핵심 단서를 실패 판정으로 봉쇄하지 않고 조사 진행을 보장; SRD 자체가 teaching rulebook이 아님을 명시.
- Year Zero Engine — 핵심 약속과 기본 구조를 먼저 제시하고 모듈을 점진적으로 추가; 전용 Free Tabletop License.
- QuestWorlds — 자유로운 능력 표현, Basic/Advanced 분리.
- Cypher System — 난이도와 자원 소비로 플레이어가 성공 확률/효과를 조절.
- Freeform Universal — Descriptor와 Yes/No + And/But 결과 언어.
- Risus — 자유작성 Cliché가 직업·배경·기술 묶음을 함축.
- Savage Worlds Test Drive — 최소 판정 루프를 먼저 가르친 뒤 캐릭터와 전투를 확장.
- Cairn / Mausritter — 필요한 경우에만 굴림, 상태·피로·인벤토리를 작은 가시적 자원으로 통합.
- Ironsworn — strong/weak/miss와 Momentum, core flow와 Move reference 및 playkit 분리.
- Resistance — 성공만큼 실패의 결과와 손실을 테마에 연결.
- City of Mist — Theme/Tag/Status를 서사 문장과 표준화된 기계 효과 사이의 인터페이스로 사용.
- Fudge — Trait 자체를 커스터마이즈 가능하게 하고 Trait Ladder로 공통 언어를 유지.
- Basic Roleplaying — d100 roll-under, 성공 확률 가독성, 사용 기반 성장, modular toolkit, Quickstart/Core/Options 분리.
- Pathfinder 2e / D&D SRD — 상세 규칙·구조화된 ability format·전통적 crunch의 대조군.
- 24XX / Lasers & Feelings — 극단적으로 작은 rules-light core와 즉시 플레이/즉흥 시나리오 생성의 대조군.
- Mothership — horror identity를 Stress/Panic에 집중하고 Player/GM/domain book과 캐릭터 생성 flowchart를 분리.

사용자가 직접 지정한 고정 조사 Source:

- `https://cympub.kr/`
- `https://sites.google.com/view/dwtemporary/%ED%99%88?authuser=0`
- `https://www.trpgclub.com/`
- `https://www.dropbox.com/scl/fo/ujjpyxy96tem420xotrpy/AKPLR0cPK7cifVgK5mTdYh8?rlkey=05ohszhw1foeoyvib0etc95qd&st=b25ypv0k&e=1&dl=0`
- `https://blog.naver.com/adventurekeeper`
- `https://hangyul219-prog.github.io/TRPG-/`

직접 접근 검증 경계:

- 초여명(cympub)은 Fate Core 시스템 시리즈 PDF 무료 공개와 Dropbox 링크를 공식 게시했다.
- 던전월드 한국어 공개판은 페이지에서 CC BY 3.0 공개 조건과 룰북 목차를 직접 확인했다.
- TRPG Club은 국내 TRPG 카탈로그와 통합 자료실을 직접 확인했다.
- Dropbox 폴더와 Naver 블로그는 현재 조사 도구에서 직접 내용을 안정적으로 열지 못했으므로 `UNVERIFIED_DIRECT_ACCESS`로 유지한다. 링크 제목이나 검색 스니펫만으로 세부 룰을 주장하지 않는다.
- 사용자가 추후 제공할 ZIP 룰북은 별도 원문 Evidence로 분석해 같은 비교 Schema에 합친다. ZIP 원본 자체는 Base에 재배포하지 않는다.

## 일반화 후보

새 Skill이나 두 번째 Watchlist를 만들지 않고, 기존 게임 개발 지식 허브 아래에 비실행 Reference인 `TRPG_RULE_DESIGN_REFERENCE_RADAR.md`를 추가한다.

```text
TRPG 설계 질문
→ 서로 다른 룰 계열의 공식/SRD/Quickstart/검증 가능한 사용자 제공 원문
→ 메커닉 + 해결한 플레이 문제 + 룰북 teaching order + support artifact 분석
→ 동일 기준 비교
→ ADOPT | ADAPT | TEST | AVOID | REFERENCE_ONLY
→ 프로젝트 고유 룰에서 PoC/플레이테스트
```

공통 분석 Schema:

```yaml
source_id:
system:
edition_or_version:
language:
source_type: FULL_RULEBOOK | SRD | QUICKSTART | PLAYER_AID | DESIGN_ARTICLE
source_tier:
verification_status:
license_or_usage:
rights_boundary:
core_player_promise:
signature_experience:
problem_solved:
mechanic_solution:
core_loop:
character_model:
freeform_elements:
freeform_bounds:
fictional_permission:
resolution_trigger:
resolution_model:
who_sets_stakes:
who_sets_risk:
who_sets_effect:
outcome_bands:
conflict_or_combat_model:
resource_economy:
core_information_policy:
gm_authority_and_procedure:
progression:
chapter_or_teaching_order: []
teach_first:
progressive_disclosure:
example_and_reference_strategy:
support_artifacts:
gm_player_information_boundary:
cognitive_load_notes:
strengths:
failure_modes:
adopt:
adapt:
avoid_or_reject:
validation_needed:
recheck_condition:
```

룰북 설명 구조는 메커닉과 별도로 비교한다.

- 게임의 약속/판타지를 먼저 보여주는가.
- TRPG의 대화 구조와 역할을 먼저 설명하는가.
- 실제 플레이 예시·리플레이·만화 등으로 추상 규칙을 먼저 시연하는가.
- 최소 판정 루프를 캐릭터 생성보다 먼저 가르치는가, 혹은 강한 캐릭터 판타지를 먼저 제공하는가.
- 캐릭터 생성에서 바로 필요한 규칙만 점진적으로 공개하는가.
- 개념이 `처음 등장 → 예시 → 심화 → reference`로 어떻게 이동하는가.
- 전투를 별도 미니게임으로 늦게 분리하는가, 공통 갈등 규칙으로 통합하는가.
- GM 규칙이 조언인지 실제 절차/제약인지.
- Basic/Advanced, Player/GM, Quickstart/Core/Reference를 분리하는가.
- 표·카드·요약 시트·예시·전투/관계/단서/세력 시트가 실제 플레이 중 참조 비용을 줄이는가.
- designer SRD/data schema의 순서를 신규 플레이어용 teaching order로 오인하지 않는가.

공용 패턴 후보는 **조건부**다.

- `FICTION_FIRST_TRIGGER_CONTRACT`: fiction-triggered system에서만 허구의 선언→규칙 trigger→결과→허구의 loop를 명확히 한다. 모든 TRPG에 Move trigger를 강제하지 않는다.
- `FICTIONAL_PERMISSION_BEFORE_MODIFIER`: 태그·면모·장비·종족·능력이 어떤 행동을 가능하게 하는지 먼저 정하고 수치 보정은 그 다음에 둔다.
- `CORE_INFORMATION_MUST_NOT_BE_SINGLE_ROLL_GATED`: 조사형 게임에서 진행 필수 정보가 단 한 번의 실패 판정으로 영구 봉쇄되지 않게 한다.
- `RISK_AND_EFFECT_ARE_DISTINCT`: 장르에 유효할 때 위험의 크기와 목표에 미치는 효과의 크기를 별도 판단한다.
- `SUPPORT_ARTIFACT_IS_PLAY_INTERFACE`: 반복 참조·기록 상태가 룰북 본문보다 시트/카드/요약에서 더 잘 작동하면 별도 인터페이스로 둔다.
- `ROLE_ASYMMETRY_REQUIRES_RECIPROCAL_VALUE`: 비대칭 역할은 각자가 다른 방식으로 핵심 경험에 기여하고 보상을 받을 때만 채택한다.
- `COMPACT_CORE_OPTIONAL_MODULES`: 첫 세션 필수 core와 campaign/advanced option을 분리한다.
- `REFERENCE_SCHEMA_IS_NOT_TEACHING_ORDER`: designer reference/data schema 순서를 player teaching order로 그대로 복제하지 않는다.
- `SRD_RIGHTS_BOUNDARY`: 관찰 가능한 설계 원리와 재사용 가능한 텍스트/표/상표/아트 권리를 분리한다.
- `VTT_IS_PRESENTATION_AND_OPERATION_LAYER`: VTT/ORPG 운영 UX를 룰 엔진과 별도 축으로 평가한다.

## 프로젝트 전용으로 남길 내용

다음은 Base 공용 규칙으로 승격하지 않는다.

- 이클립스 세계관의 차원 균열·각성·길드·세력·수치.
- 이클립스 TRPG의 현재 임시 수치(`2d6`, 기본 능력 수, 면모 수, 스킬 수, 상태 트랙 등).
- 특정 룰북의 표현 문장·세계관·캐릭터·고유 용어·표현물·아트.
- 특정 시스템의 상표·Product Identity.
- 사용자가 제공할 ZIP 파일 자체의 재배포.

Base는 비교 방법과 출처 레이더만 소유하며, 실제 TRPG 프로젝트의 정본 규칙은 해당 프로젝트가 소유한다.

## 적용 조건과 비사용 조건

적용 조건:

- TRPG의 판정·캐릭터 제작·자유작성 능력·전투/갈등·조사·GM 절차·성장·자원 경제·룰북 설명 순서를 결정할 때.
- 한 시스템을 복제하지 않고 서로 다른 설계 해법을 비교해야 할 때.
- 공개 SRD/Quickstart/사용자 제공 룰북에서 재사용 가능한 원리만 추출할 때.
- 룰북/퀵스타트/플레이 시트가 같은 규칙을 서로 다른 순서와 밀도로 가르쳐야 할 때.

비사용 조건:

- 특정 프로젝트의 이미 승인된 규칙을 자동으로 덮어쓰는 authority로 사용하지 않는다.
- 공개 Source 링크가 있다는 이유만으로 라이선스가 같은 것으로 추정하지 않는다.
- 커뮤니티 요약·미러·리뷰만으로 정확한 규칙 텍스트나 라이선스를 확정하지 않는다.
- 플레이테스트 없이 벤치마크 선호도를 재미·밸런스 증거로 승격하지 않는다.
- 비공개/유료 룰북의 원문을 Base에 복제하지 않는다.
- 특정 system family의 장치를 보편 mandatory rule로 승격하지 않는다.

## 반례와 위험

### 최소 3안 비교

| 안 | 장점 | 위험·비용 | 판정 |
| --- | --- | --- | --- |
| A. 기존 `REFERENCE_SOURCE_CATALOG.md`에 링크만 추가 | 변경이 가장 작고 단순함 | 룰별 설계/교육 구조 비교가 Catalog를 비대하게 만들고 재사용성이 낮음 | `REJECT` |
| B. TRPG 전용 신규 Skill 생성 | 자동 라우팅과 절차를 한 곳에 넣기 쉬움 | 기존 game-design/research owner와 책임 중복, Skill 수 증가, 실행 권한 과잉 | `REJECT` |
| C. 기존 game-development knowledge hub 아래 비실행 TRPG Radar 추가 | 공용 Source 정책 재사용, 프로젝트 정본 침범 없음, 룰별 비교 축과 ZIP intake를 한곳에 축적 가능 | 문서가 링크 덤프가 되지 않도록 엄격한 비교 Schema/검증 상태 필요 | `ADOPT` |

주요 위험과 대응:

1. **유명세 편향** — 같은 PbtA/Fate 계열만 늘리지 않고 전통적 crunch, percentile, freeform, OSR, investigation, tactical, micro-RPG 등 서로 다른 해법을 대표로 선정한다.
2. **자유작성 만능화** — 넓은 문장을 쓴 플레이어가 우월해지는 문제를 자유작성 계열끼리 별도 비교한다.
3. **SRD ≠ 학습용 룰북** — GUMSHOE 등 디자인 Reference는 완성된 교육 구조와 구분해 기록한다.
4. **라이선스 혼동** — CC BY, ORC, 자체 라이선스, 무료 열람, 재배포 제한을 별도 필드로 보존한다.
5. **미러/커뮤니티 권위 과장** — 원출처를 역추적하며 원출처 미확인 자료는 `DISCOVERY_ONLY` 또는 `UNVERIFIED_DIRECT_ACCESS`로 유지한다.
6. **문서량 자체를 성과로 착각** — 각 Source가 실제 설계 질문을 바꾸는 `decision_delta`가 없으면 Reference-only로 남긴다.
7. **프로젝트 과적합** — Base에는 이클립스 고유 수치·명칭을 넣지 않고 재사용 가능한 분석 프레임만 둔다.
8. **설명 순서 과적합** — play-flow-first를 기본 후보로 보되 replay-first, setting-consensus-first, character-first 등 장르별 예외를 비교한다.
9. **보조 시트 과잉** — 반복 참조/상태 소유가 없는 정보는 별도 시트로 쪼개지 않는다.

## 영향 범위와 검증

승인된 최소 구현 범위:

- `docs/knowledge/game-development/TRPG_RULE_DESIGN_REFERENCE_RADAR.md` 신규.
- `docs/knowledge/game-development/README.md` 문서 지도에 TRPG Radar 라우팅 한 줄 추가.
- `docs/knowledge/game-development/REFERENCE_SOURCE_CATALOG.md`에는 상세 내용을 복제하지 않고 TRPG Radar가 소유한다는 짧은 routing/index만 추가.
- 필요하면 위 세 문서의 존재/라우팅/권리 경계/프로젝트 고유 값 비유입을 검사하는 focused regression test 1개를 추가한다.
- 신규 Skill/Tool/외부 dependency/과금 없음.

검증 계획:

1. 문서 내부 Source마다 authority/verification/license 상태가 구분되는지 확인.
2. 사용자 고정 5개 링크가 누락되지 않았는지 확인.
3. 적어도 3개 이상 materially distinct 룰 설계 대안이 같은 기준으로 비교되는지 확인.
4. 각 대표 룰에 `핵심 특징 / 해결한 플레이 문제 / 규칙을 풀어낸 방식 / 설명 순서 / support artifact / 장단점 / ADOPT·ADAPT·REJECT`가 존재하는지 확인.
5. ZIP 후속 분석에 `실제 목차 + 개념 first appearance→example→deepening→reference transition`이 포함되는지 확인.
6. 이클립스 고유 수치나 저작권 원문이 Base 공용 규칙으로 유입되지 않았는지 확인.
7. 신규 Skill/Tool/dependency가 생기지 않는지 확인.
8. 최소 5회 full-scope adversarial review 뒤 새 blocking finding 0일 때만 clean exit.

Evidence ceiling:

- 이 BCP는 TRPG 조사·비교 구조, 룰북 teaching-order 분석 축, Source 목록의 공용 유용성을 승인한다.
- 특정 룰이 이클립스에 재미/밸런스상 최적이라는 것을 증명하지 않는다.
- 실제 적용 수치와 조합은 프로젝트별 PoC와 플레이테스트가 필요하다.
- 직접 접근하지 못한 Dropbox/Naver source의 세부 내용은 사용자가 원문/ZIP을 제공하기 전까지 검증되지 않은 상태다.

## 필요한 도구·파일·권한

- 필요 항목: 기존 GitHub 문서, 공개 웹/SRD/Quickstart, 추후 사용자 제공 ZIP.
- 필요한 이유: 룰 메커닉과 교육 구조를 원출처 기준으로 비교하기 위해서다.
- 설치·적용 방법: 신규 설치 없음. 기존 GitHub/Web/파일 분석만 사용한다.
- 설치 후 확인 명령: 해당 없음.
- 최소 권한: Base current-task branch/PR 정상 권한. force push/admin bypass 불필요.
- 추가 금전 비용: `0`.

## 승인과 구현

- 사용자 승인 근거: 2026-08-24 현재 작업 대화에서 사용자가 `base에 trpg 자료로 추가하고. 더 많은 링크를 찾아봐`, `작업계속진행`, 그리고 `룰북 각각 특징과 어떻게 풀어냈는지, 설명은 어떤 순서로 어떻게 진행했는지도 생각해서 정리해줘`라고 명시했다.
- `approval_ref`: `[수정제안서]/BCP-2026-030-trpg-rule-design-reference-radar/PROPOSAL.md#승인과-구현` + 2026-08-24 current task user approval + proposal PR `#651`.
- 승인 범위: 기존 game-development knowledge hub 아래 비실행 TRPG Reference Radar + 최소 routing/index + 필요한 focused regression만 구현한다.
- 승인 제외: 신규 Skill, 신규 Tool/Watchlist/scheduler, 특정 프로젝트 규칙·세계관·수치의 Base 승격, 유료/비공개 룰북 원문 복제, VTT 설치, 외부 dependency 추가.
- 구현 PR: `없음 — 별도 구현 PR에서 진행`
- 롤백: 승인 PR은 proposal/evidence/registry 상태만 되돌린다. 구현 뒤에는 신규 Radar와 README/Catalog routing(+focused test)만 되돌리며 프로젝트 정본은 영향을 받지 않는다.
