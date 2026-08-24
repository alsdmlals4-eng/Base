# TRPG Source Scan — 2026-08-24

## 조사 질문

- TRPG 룰북은 **무엇을 재미의 핵심으로 선언**하고, 그 재미를 어떤 규칙·자원·시트·GM 절차로 실제 플레이에 연결하는가?
- 처음 읽는 사람에게 규칙을 **어떤 순서로 설명**하여 `이 게임이 무엇인지 → 캐릭터는 누구인지 → 어떻게 행동하는지 → 실패와 결과가 어떻게 이어지는지 → GM은 무엇을 하는지`를 이해시키는가?
- 룰북 본문과 캐릭터 시트·플레이 서머리·시나리오/전투/관계/단서 관리 시트의 책임을 어떻게 나누는가?
- 공개 관찰 가능한 설계 원리와 실제 재사용 가능한 SRD/텍스트/도표/자산의 권리를 어떻게 분리해야 하는가?

## 판정 범례

- `ADOPT`: 여러 프로젝트에 공용 원리로 직접 유효.
- `ADAPT`: 문제 해결 방식은 유효하지만 장르·복잡도·권리 조건에 맞춰 변형.
- `TEST`: 유망하지만 실제 프로젝트 플레이테스트 전 강제 규칙으로 승격하지 않음.
- `REFERENCE_ONLY`: 관찰·비교용. 고유 규칙/문구/수치/자산은 복제하지 않음.
- `UNVERIFIED_DIRECT`: 링크 존재·주변 출처는 확인했지만 현재 도구에서 원문 직접 읽기 실패.

---

## 1. 사용자가 직접 지정한 한국어 Source

### KTRPG-CYMPUB-001 — 도서출판 초여명

- URL: `https://cympub.kr/`
- source tier: `T2_PROFESSIONAL_PRACTICE / publisher-primary`
- access: `PARTIAL_DIRECT`
- rights: 작품별 상이. 홈페이지 공개 자체를 자유 재사용 권한으로 간주하지 않음.
- 확인 사실:
  - 2023년 페이트 코어 시스템 시리즈 PDF 무료 공개 공지를 유지하고 있으며, 현재 Dropbox 폴더로 연결한다.
  - 던전월드 한국어 공개판은 별도 공개 페이지에서 CC BY 3.0 조건을 명시한다.
  - 초여명 컨벤션 자료에서 30분 데모 플레이를 작품의 분위기와 기본 진행법을 익히는 도구로 사용했고, TRPG 디자인 강의는 시스템/룰, 공백, 책임, 피드백 루프, 감정, 보상, 권위, 집중/구조화된 플레이, 설명의 명료성 등을 디자인 주제로 명시했다.
- 설계상 의미:
  - 룰북 벤치마킹은 수치 비교보다 **플레이어가 무엇을 느끼고 무엇을 반복하는가**를 먼저 봐야 한다.
  - 긴 룰북과 별개로 30분 데모/퀵스타트가 제품의 핵심 감각을 전할 수 있어야 한다.
- disposition: `ADOPT` — source pool + teaching/demo pattern.

### KTRPG-DW-KO-001 — 던전월드 한국어 공개판

- URL: `https://sites.google.com/view/dwtemporary/홈`
- source tier: `T1_PRIMARY_OFFICIAL_TRANSLATION`
- access: `DIRECT`
- rights: 한국어 공개판이 CC BY 3.0 Unported임을 페이지가 명시.
- 특징 / 문제 해결:
  - 플레이를 '대화'로 먼저 정의하고, 허구 속 특정 상황이 규칙을 발동시키며 결과가 다시 대화/허구에 반영되는 구조를 전면에 둔다.
  - 공격 가능 여부도 단순 수치가 아니라 **허구에서 실제로 피해를 줄 수 있는 상황인지**를 먼저 판단한다.
  - GM에게도 강령·원칙·액션이라는 구체적인 규칙을 부여해 'GM 재량'을 무제한 블랙박스로 두지 않는다.
- 룰북 설명 순서:
  1. 서문
  2. **플레이하는 법** — 먼저 대화, 룰의 발동, 능력치/액션의 의미를 설명
  3. **플레이의 예** — 추상 설명 직후 실제 대화 사례
  4. **캐릭터 만들기** — 직업→종족→이름…을 시트 작성 절차로 설명
  5. **액션** — 실제 반복 판정 단위 상세
  6. **직업** — 캐릭터 고유 데이터
  7. **마스터** — GM의 강령·원칙·액션
  8. **첫 세션** — 인쇄물·준비물·준비 정도·즉흥 세계 구축
  9. 국면→세계→괴물→장비→고급/변환/NPC 참고 자료
- 설명 방식에서 배울 점:
  - `개념 → 실제 플레이 예 → 캐릭터 생성 → 반복 규칙 → 역할별 상세 → 첫 세션 절차 → 레퍼런스` 순서가 좋다.
  - 캐릭터 생성 자체를 세계 설정 대화로 취급해 '세계관 설명'과 '캐릭터 제작'이 따로 놀지 않는다.
- disposition: `ADOPT` — `FICTION_FIRST_TRIGGER_CONTRACT`, GM procedure, example-before-reference.

### KTRPG-CLUB-001 — TRPG Club 통합 자료실

- URL: `https://www.trpgclub.com/?p=96`
- source tier: `T2_PUBLISHER_SUPPORT_MATERIAL`
- access: `DIRECT`
- rights: 대부분 상용 작품 지원 자료. `REFERENCE_ONLY` unless per-file license says otherwise.
- 특징 / 문제 해결:
  - 게임별로 캐릭터 시트만 제공하지 않는다. 플레이 서머리, 핸드아웃, 시나리오 시트, 전투 시트, 거점 시트, NPC/에너미 관리, 관계/인연, 조사 시트, 규칙 요약, 지도, 카드 등을 **실제 반복 절차별 support artifact**로 분리한다.
  - 시노비가미는 캐릭터/플레이 요약/비밀 핸드아웃/시나리오/전투 시트를 분리한다.
  - 인세인은 캐릭터/전투/의식/몹/핸드아웃/광기 카드/규칙 요약/색인을 분리한다.
  - 둘이서 수사는 탐정/조수 시트 자체를 나누고, 사건 조사·사전 조사·다툼·아지트·시나리오 제작 체크·규칙 요약을 별도 제공한다.
  - 톱니바퀴탑의 탐공사는 캐릭터, 퀘스트, 플라이트, 비공정, 트로피, 이명, 탐색, 구획, 에너미 등 **캠페인 객체마다 별도 인터페이스**를 제공한다.
- 설명 방식에서 배울 점:
  - 룰북 본문의 장 구성과 **테이블에서 실제로 펼쳐놓는 정보 구조는 동일할 필요가 없다**.
  - 반복적으로 참조하거나 여러 참가자가 동시에 수정하는 상태는 별도 시트/카드로 빼는 편이 낫다.
- disposition: `ADOPT` — `SUPPORT_ARTIFACT_IS_PLAY_INTERFACE`.

### KTRPG-FUTARI-001 — 둘이서 수사

- URL: `https://www.trpgclub.com/?p=2039`
- source tier: `T2_PUBLISHER_PRIMARY_DESCRIPTION`
- access: `DIRECT`; 상세 상용 룰북 원문은 미확인.
- rights: `REFERENCE_ONLY`.
- 핵심 경험:
  - 사건의 핵심을 빠르게 꿰뚫는 **탐정**과 그를 보조하며 관계를 쌓는 **조수**라는 비대칭 버디 플레이.
  - 확장판은 사전 조사 시트와 다툼 규칙처럼 **플레이 전 기대 조율과 관계 변화**를 독립 규칙으로 다룬다.
- 풀어낸 방식:
  - 역할 성능을 완전히 평준화하지 않고 서로 다른 기여를 주어 관계 드라마를 만든다.
  - 사건 조사 시트, 탐정/조수 분리 시트, 관계·다툼 지원 시트로 장르 경험을 시각적으로 분리한다.
- 설명/제품 순서 관찰:
  - 먼저 '탐정+조수로 수수께끼를 푼다'는 약속을 한 문장으로 고정 → 기본 룰/시나리오/리플레이 → 필요 시 관계/괴도/경찰 같은 확장 규칙과 시나리오.
- disposition: `ADAPT` — 역할 비대칭은 reciprocal value와 상호의존이 있을 때만.

### KTRPG-SHINOBIGAMI-001 — 시노비가미

- URL: `https://www.trpgclub.com/?p=1860/`
- source tier: `T2_PUBLISHER_PRIMARY_DESCRIPTION`
- access: `DIRECT` for official description/support sheets.
- rights: `REFERENCE_ONLY`.
- 핵심 경험:
  - 닌자의 사명·비밀·조직·인법과 PC 간 적대/관계가 뒤집히는 정보전 + 결전.
  - 지원 핸드아웃 자체가 공개 `사명`과 비공개 `비밀`을 물리적으로 분리한다.
- 룰북 설명 순서가 매우 명확함:
  1. **인물의 서** — 캐릭터 제작
  2. **이치의 서** — 실제 플레이 규칙
  3. **기법의 서** — 인법/배경 데이터
  4. **길의 서** — GM·시나리오·적 데이터
  5. **세계의 서** — 월드 설정
- 설명 방식에서 배울 점:
  - `캐릭터 → 플레이 규칙 → 데이터 → GM → 세계`라는 역할 기반 분할은 플레이 진입을 빠르게 한다.
  - 규칙 파트에서 '암기하지 말고 필요할 때 참조'라고 명시해 reference-first 사용을 전제한다.
  - 세계 설정을 가장 뒤에 놓아 **세계관 숙지 없이도 캐릭터/플레이가 가능한 구조**를 만든다.
- disposition: `ADAPT` — 비밀 정보/핸드아웃이 핵심인 게임에서 정보 권한을 데이터 레벨로 분리.

### KTRPG-INSANE-001 — 인세인

- URL: `https://www.trpgclub.com/?p=338`
- source tier: `T2_PUBLISHER_PRIMARY_DESCRIPTION`
- access: `DIRECT` for official description/support artifacts.
- rights: `REFERENCE_ONLY`.
- 핵심 경험:
  - 다양한 호러 장르를 공통 엔진으로 다루면서 PC의 `비밀`과 `광기`를 외부 괴이만큼 중요한 내부 위협으로 만든다.
- 설명 구조 관찰:
  - **전반부 리플레이 → 후반부 실제 규칙**. 먼저 어떤 공포와 인간관계가 테이블에서 발생하는지 보여준 뒤 규칙으로 해체한다.
  - 통합 자료실에서 캐릭터 시트 / 전투 / 의식 / 몹 / 핸드아웃 / 광기 카드 / 규칙 서머리 / 색인을 분리한다.
- 설명 방식에서 배울 점:
  - 감정·장르 톤이 중요한 게임은 규칙을 앞세우기 전에 **완성된 플레이 감각을 리플레이로 시연**하는 방식이 유효하다.
- disposition: `ADAPT` — replay-first pedagogy, hidden-state artifact separation.

### KTRPG-MAGICA-001 — 마기카로기아

- URL: `https://www.trpgclub.com/?p=467`
- source tier: `T2_PUBLISHER_PRIMARY_DESCRIPTION`
- access: `DIRECT` for product description.
- rights: `REFERENCE_ONLY`.
- 핵심 경험:
  - 위험한 마도서 회수라는 분명한 미션에 캐릭터 과시, 주사위 해프닝, 수읽기/심리전, 뜻밖의 진실, 행동에서 비롯되는 비극을 결합한다.
- 설명 방식 관찰:
  - 제품 소개 단계에서부터 '이 게임으로 무엇을 체험하는가'를 감정/사건 단위 bullet로 먼저 제시한다.
  - 어려워 보이는 심리전·비극에 대해 실제 플레이는 친구들과 편안하게 공동 이야기를 만드는 것이라고 기대치를 보정하고, 앞부분의 만화·소개 페이지로 진입 장벽을 낮춘다.
- disposition: `ADOPT` — rulebook opening에서 feature list보다 **experience promise**를 먼저 명시.

### KTRPG-FATE-KO-DROPBOX-001 — 초여명 Fate Core 공개 PDF 폴더

- URL: `https://www.dropbox.com/scl/fo/ujjpyxy96tem420xotrpy/...`
- source tier: publisher-provided distribution link.
- access: `UNVERIFIED_DIRECT` — 현재 web fetch 실패. 초여명 홈페이지가 '페이트 코어 시스템 시리즈 PDF 무료 공개' 폴더로 직접 연결하는 사실은 확인.
- rights: 공개 배포와 재사용 권한은 별개이므로 Fate 원 SRD의 CC 조건과 개별 번역/편집물 조건을 각각 확인해야 함.
- 현재 사용: 파일 목록/페이지 순서/번역 표현을 확정 근거로 쓰지 않음. Fate 설계 분석은 공식 Fate SRD로 수행.

### KTRPG-COCOFOLIA-GUIDE-001 — `adventurekeeper` Naver blog

- URL: `https://blog.naver.com/adventurekeeper`
- source tier: `T4_COMMUNITY_GUIDE` 후보.
- access: `UNVERIFIED_DIRECT` — robots/cache 제한으로 현재 직접 본문 읽기 실패.
- 주변 색인에서 특정 글 `222005941540`이 코코포리아 정보/가이드로 인용되는 것은 확인.
- 현재 사용:
  - 구체 기능·절차를 이 source의 사실로 확정하지 않는다.
  - VTT/ORPG의 캐릭터 표현, 장면 전환, BGM, 채팅 로그, 매크로/자동화, 핸드아웃 UX를 별도 `PRESENTATION_AND_OPERATION_LAYER`로 조사해야 한다는 discovery source로만 유지.
- disposition: `REFERENCE_ONLY / UNVERIFIED_DIRECT`.

---

## 2. 추가 공식·오픈 시스템 비교

### TRPG-FATE-CONDENSED-001 — Fate Condensed

- URL: `https://fate-srd.com/fate-condensed`
- source tier: `T1_PRIMARY_OFFICIAL_SRD`
- access: `DIRECT`
- rights: Fate SRD는 CC BY 3.0 기반. 상표/로고/별도 자산은 구분.
- 핵심 해결 문제:
  - 캐릭터의 정체성/관계/문제를 숫자 외부의 **Aspect = true fact**로 만들고, Fate Point로 강점과 곤란이 순환하도록 한다.
  - Skill은 넓은 역량, Stunt는 특정 우수성/규칙 예외로 분리한다.
- 설명 순서 관찰:
  1. Introduction — 필요한 도구와 Core 대비 변경점
  2. Getting Started — **setting을 먼저 합의**
  3. Character — Aspect → Skill → Refresh → Stunt → Stress/Consequence → 마무리
  4. Aspects & Fate Points — 이미 캐릭터에서 만난 핵심 개념을 심화
  5. 행동/굴림 → Challenge/Contest/Conflict → Harm → Advancement → GM/옵션 계열
- 설명 방식:
  - 처음부터 설정의 허용 범위를 합의한 뒤 캐릭터를 만든다.
  - 핵심 개념은 생성 단계에서 '필요한 만큼' 소개하고 별도 장에서 다시 깊게 설명하는 **progressive disclosure**.
- disposition: `ADOPT` — truth/effect separation, compact core, progressive disclosure.

### TRPG-BITD-001 — Blades in the Dark SRD

- URL: `https://bladesinthedark.com/`
- source tier: `T1_PRIMARY_OFFICIAL_SRD`
- access: `DIRECT`
- rights: CC-licensed SRD; 구체 라이선스 페이지 재확인 필요.
- 핵심 해결 문제:
  - 플레이어가 행동을 고르고 GM은 **위험(Position)**과 **효과(Effect)**를 별도로 판단해 '어렵다'를 단일 숫자로 뭉개지 않는다.
  - 결과에 불만족하면 Resistance로 대가를 줄이되 Stress를 부담해 플레이어에게 사후 agency를 준다.
  - 복잡한 목표/위험은 Clock으로 진행을 가시화한다.
  - Score→Downtime→Free Play cycle과 Crew를 통해 개인 모험을 캠페인 조직 성장과 연결한다.
- 설명 구조에서 배울 점:
  - 'Game → Players/Characters/Crew' 약속을 먼저 설명한 뒤, core system의 **판단 권한이 누구에게 있는지**를 명시한다.
  - Core System 페이지는 dice 설명과 함께 4종 roll, phase structure까지 한 번에 연결해 '한 번의 판정'과 '캠페인 흐름'을 같은 mental model에 넣는다.
  - Player Kit는 basic procedure / character+crew creation / faction / map / reference를 별도 묶음으로 제공한다.
- disposition: `ADOPT` — risk/effect split, clocks, authority mapping, player kit.

### TRPG-GUMSHOE-001 — GUMSHOE SRD

- URL: `https://pelgranepress.com/.../GUMSHOESRDCC-3 20241209.pdf`
- source tier: `T1_PRIMARY_OFFICIAL_SRD`
- access: `DIRECT_PDF`
- rights: CC BY 3.0 version, trademark/setting exclusions 명시.
- 핵심 해결 문제:
  - 추리 게임이 '필수 단서를 못 찾아 멈추는 것'을 방지한다.
  - **Investigative abilities**와 생존/행동용 **General abilities**를 분리하고, Core Clue는 적절한 장소/방법/능력으로 찾으면 자동 제공해 재미를 '단서 발견 여부'보다 **해석·연결·결정**으로 이동시킨다.
- 설명 순서/문서 성격:
  - SRD 스스로 **게임을 가르치는 playable rulebook이 아니라 디자이너용 reference**라고 밝힌다.
  - Introduction 직후 Character concept → Investigative/General abilities → rating/pool distinction으로 설계 chassis를 먼저 제공한다.
  - 완성 룰북에서는 이 텍스트 사이에 setting tone과 실제 예시를 끼워 넣으라고 명시한다.
- disposition: `ADOPT` — `CORE_INFORMATION_MUST_NOT_BE_SINGLE_ROLL_GATED`; SRD와 teaching rulebook의 책임 분리.

### TRPG-YZE-001 — Year Zero Engine SRD

- URL: `https://freeleaguepublishing.com/.../YZE-Standard-Reference-Document.pdf`
- source tier: `T1_PRIMARY_OFFICIAL_SRD`
- access: `DIRECT_PDF`
- rights: 전용 `Year Zero Engine Free Tabletop License v1.0`; SRD 외 자산/브랜드는 미포함.
- 핵심 해결 문제:
  - 배우기 쉬운 core에 필요할 때 선택지를 덧붙이는 구조.
  - push/re-roll을 강하게 허용하되 반드시 비용을 붙여 **위험-보상 선택**을 반복한다.
- 설명 순서:
  1. Introduction — Players/GM 역할 + accessible/fast/risks&rewards 등 엔진의 설계 목표
  2. Player Characters
  3. Skills & Specialties
  4. Combat & Damage
  5. Magic
  6. Travel
- 설명 방식:
  - 세부 수치보다 먼저 '이 엔진은 무엇을 잘하기 위해 존재하는가'를 six core features로 선언한다.
  - 범용 엔진에서도 character→skill→combat→optional domain module 순으로 core-to-module 진행.
- disposition: `ADOPT` — engine design pillars before rule details; risk/reward push as optional pattern.

### TRPG-24XX-001 — 24XX SRD

- URL: `https://jasontocci.itch.io/24xx`, readable mirror `https://24xx-srd.carrd.co/`
- source tier: `T1_PRIMARY_AUTHOR_RELEASE` + mirror for searchable text.
- access: `DIRECT`
- rights: CC BY 4.0.
- 핵심 해결 문제:
  - 극소 규칙량에서 fictional positioning을 유지하고 계산을 최소화.
  - 플레이어는 먼저 행동을 묘사하고, GM은 불가능/추가 단계/비용/위험을 알려주며, 플레이어가 목표·stakes를 수정할 기회를 가진 뒤 **위험 회피가 필요할 때만** 굴린다.
  - skill die 단계와 highest-die 결과로 연산을 줄인다.
- 설명/레이아웃 순서:
  - 한 화면/소책자에서 `RULES | CHARACTERS | GEAR | DETAILS`, 뒤쪽에 setting premise + job tables + GM improv guidance.
  - SRD design note를 player-facing text와 분리해 디자이너가 '무엇을 왜 바꾸는지'까지 보게 한다.
- disposition: `ADOPT` — roll-only-for-risk, editable-stakes-before-roll, microgame information density, designer note separation.

### TRPG-CAIRN-001 — Cairn

- URL: `https://cairnrpg.com/second-edition/players-guide/core-rules/`
- source tier: `T1_PRIMARY_OFFICIAL_RULES`
- access: `DIRECT`
- rights: site text CC BY-SA 4.0.
- 핵심 해결 문제:
  - 탐험에서 신중한 판단·장비·위험 관리를 강조하며 규칙을 극단적으로 단순화.
  - 공격은 자동 명중하고 damage만 굴려 전투 시간을 줄이는 대신 armor, HP, critical damage, scars로 결과를 직접 만든다.
  - inventory slot과 Fatigue를 연결해 피로가 단순 수치가 아니라 **휴대 능력/탐험 선택**을 압박한다.
- 설명 순서(1e SRD와 2e Player Guide에서 공통적으로 읽히는 패턴):
  - Player principles → Character Creation → 생성 테이블/장비 → Core Rules → Magic → Combat → Bestiary/Spells → Rules Summary.
- 설명 방식:
  - 먼저 '어떻게 플레이해야 잘 되는가'라는 player principles를 주고 세부 규칙으로 간다.
  - rules summary를 끝에 두어 reference surface를 명시적으로 제공.
- disposition: `ADAPT` — player principles, inventory-as-pressure, auto-hit only if desired experience fits.

### TRPG-LF-001 — Lasers & Feelings

- URL: `https://johnharper.itch.io/lasers-feelings`
- source tier: `T1_PRIMARY_AUTHOR_RELEASE`
- access: `DIRECT` product page; PDF는 별도 download.
- rights: 2021년부터 CC BY 4.0, commercial hacks 허용.
- 핵심 해결 문제:
  - 1페이지에서 캐릭터 생성, 판정, GM 즉흥 시나리오 생성까지 끝내는 pick-up-and-play.
  - 한 숫자를 논리/기술(Lasers)과 감정/직관(Feelings)의 반대 방향 성공 기준으로 사용해 단 하나의 선택이 캐릭터 성향과 확률을 동시에 정의한다.
- 설명 방식:
  - premise → 즉시 캐릭터 선택 → 한 숫자 → 언제/몇 개 굴리는지 → 결과 → GM용 사건 생성표로 **상태를 만들자마자 사용법을 바로 붙이는** 구조.
- disposition: `ADAPT` — one-page quickstart benchmark; single-stat engine 자체는 프로젝트 적합성 TEST 필요.

### TRPG-IRONS-001 — Ironsworn

- URL: `https://tomkinpress.com/products/ironsworn-digital-edition`
- source tier: `T1_PRIMARY_AUTHOR_RELEASE`
- access: official product/support pages direct; full rulebook free download.
- rights: 별도 라이선스 확인 필요; free download ≠ automatic reuse permission.
- 핵심 해결 문제:
  - GM guided뿐 아니라 co-op/solo까지 같은 engine으로 지원.
  - Vow/Progress/Oracle/Move를 통해 GM이 없더라도 목표·불확실성·진척·새 사건을 생성한다.
  - 별도 Playkit, asset cards, Truths workbook으로 세계/캐릭터/참조 상태를 분리한다.
- 설명 순서(공개 rulebook 목차 확인):
  1. Chapter 1 Basics — playing/fiction/setting/vows/moves/action roll/momentum/progress/harm/stress/assets/oracles/bonds/equipment/**flow of play**
  2. Chapter 2 Character — 캐릭터 세부 + 마지막에 creation summary
  3. Chapter 3 Moves — adventure/relationship/combat/suffer/quest/fate move 사전
  4. 이후 world/campaign/GM-less support 영역
- 설명 방식:
  - **캐릭터 생성 전에 core loop와 flow를 먼저 이해**시키는 구조가 두드러진다.
  - 처음부터 모든 Move 세부를 읽히지 않고 Basics에서 개념→Character→Move Reference로 되돌아온다.
- disposition: `ADOPT` — core loop before creation for unfamiliar engines, playkit/workbook separation, oracle pattern for GM-less/low-prep use.

### TRPG-MOTHERSHIP-001 — Mothership 1e Player's Survival Guide

- URL: `https://www.tuesdayknightgames.com/products/mothership-players-survival-guide`
- source tier: `T1_PRIMARY_PUBLISHER`
- access: product page direct; PDF is officially free.
- rights: free price only 확인. reuse license는 별도 확인 전 `REFERENCE_ONLY`.
- 핵심 해결 문제:
  - d100 roll-under를 기본으로 하고 horror identity를 Stress & Panic에 집중한다.
  - 초기 공개 이후 수천 플레이어 피드백을 반영해 edge case와 불필요한 roll을 제거하고 Panic 전용 d20 등 novice comprehension을 개선했다.
  - 캐릭터 생성 전체를 한 페이지 flow-chart sheet에 담아 시작 마찰을 줄인다.
- 설명/제품 분할:
  - Player's Survival Guide: Character Creation → How to Play → Violent Encounters → Stress & Panic → Shore Leave → Weapons/Equipment.
  - Warden's Operations Manual은 첫 세션 준비/진행/캠페인 준비를 별도 책으로 분리.
  - Monster design/reference와 spaceship rules도 별도 core book으로 분리.
- disposition: `ADOPT` — player/GM/domain book split, character-flowchart, post-playtest edge-case removal.

### TRPG-DND-SRD52-001 — D&D SRD 5.2

- URL: `https://www.dndbeyond.com/srd` / CC PDF
- source tier: `T1_PRIMARY_OFFICIAL_SRD`
- access: `DIRECT_PDF`
- rights: CC BY 4.0.
- 핵심 해결 문제:
  - 전통 d20 장기 캠페인에서 넓은 행동·전투·캐릭터 옵션·주문·몬스터를 표준화.
- 설명 순서(현재 SRD 5.2 contents):
  1. **Playing the Game** — rhythm, six abilities, d20 tests, actions, social/exploration/combat, damage/healing
  2. **Character Creation**
  3. Classes
  4. Character Origins
  5. Feats
  6. Equipment
  7. Spells
  8. Rules Glossary
  9. Gameplay Toolbox
  10. Magic Items
  11. Monsters
- 설명 방식에서 배울 점:
  - 방대한 시스템에서도 '기본 플레이 언어'를 캐릭터 빌드보다 먼저 둔다.
  - 이후 character options와 reference encyclopedia를 분리한다.
- disposition: `ADAPT` — `HOW_PLAY_WORKS_BEFORE_BUILD_OPTIONS`; 옵션량 자체는 경량 프로젝트에 REJECT.

---

## 3. 공통 설명 순서 패턴

### Pattern A — 플레이 언어 먼저

대표: Dungeon World, D&D SRD, Ironsworn Chapter 1.

```text
이 게임은 무엇인가
→ 테이블에서 누가 무엇을 말하는가
→ 언제 룰/주사위가 개입하는가
→ 결과가 무엇을 바꾸는가
→ 캐릭터 생성
→ 상세 행동/데이터
```

장점: 캐릭터 시트의 숫자부터 외우지 않고 '왜 이 항목이 필요한지' 이해한다.

### Pattern B — 플레이 예시 먼저

대표: Dungeon World의 플레이 예, 인세인의 리플레이.

```text
핵심 개념
→ 실제 대화/리플레이
→ 규칙 해체
```

장점: 서사형·장르 감정형 시스템에서 추상 용어의 의미를 빠르게 보여준다.

### Pattern C — 캐릭터→규칙→데이터→GM→세계

대표: 시노비가미.

장점: 플레이어가 '내가 무엇을 만들고 어떤 규칙을 쓰는가'부터 보고, 방대한 setting은 필요할 때 읽는다.

### Pattern D — 설정 합의→캐릭터의 사실→역량→예외 능력→피해/자원

대표: Fate Condensed.

장점: 자유 설정형 게임에서 setting permission과 character permission이 먼저 정해져 rules-lawyering을 줄인다.

### Pattern E — 플레이어 책 / GM 책 / 도메인 레퍼런스 분리

대표: Mothership, TRPG Club support artifact ecosystem.

장점: 모든 참가자에게 모든 정보를 읽히지 않는다. 반복 참조 비용과 spoiler 위험을 줄인다.

### Pattern F — 초압축 core→즉시 시나리오 생성

대표: 24XX, Lasers & Feelings.

장점: one-shot/quickstart에서 준비 시간을 최소화하고 setting data를 'gameable lore table'로 바꾼다.

---

## 4. 공용 TRPG 룰북 작성 권장 순서 후보

모든 게임에 강제하지 않고 `default starting pattern`으로 제안한다.

1. **Player Promise** — 어떤 인물이 되어 무엇을 반복하고 어떤 감정을 느끼는가.
2. **30초/5분 Flow** — 장면에서 `상황 → 의도 → 방법 → 필요 시 판정 → 결과 → 다음 장면`이 어떻게 도는가.
3. **Play Example** — 핵심 판정 1개, 실패/부분성공/성공의 차이가 실제 대화에서 어떻게 보이는가.
4. **Character Creation** — 항목을 채우는 순서와 각 항목이 플레이에서 왜 필요한지.
5. **Core Resolution** — 언제 굴림/룰을 쓰며 누가 위험·효과·결과를 정하는가.
6. **Character Truth / Permission** — 면모·태그·종족·장비·배경이 무엇을 가능하게 하는가.
7. **Special Abilities / Skills** — 수치와 예외 능력, 작성/선택 규칙.
8. **Conflict / Harm / Recovery** — 전투만이 아니라 사회·추격·재난 등 갈등 공통 처리.
9. **Game-Specific Signature Loop** — 조사, 관계, 공포, 자원, 마석, crew, vow 등 '이 게임만의 이유'.
10. **Advancement / Campaign Consequence** — 세션 뒤 무엇이 변하고 다음 선택을 어떻게 만든다.
11. **GM Procedure** — agenda/principles, 판정 요구 기준, 실패 결과, 시나리오 준비, 적/위협 제작.
12. **Quickstart / Sample** — 실제 첫 세션이 가능한 캐릭터·시나리오·요약.
13. **Reference/Data** — 스킬/태그/장비/상태/적/표/색인.
14. **Support Artifacts** — 캐릭터/GM/전투/관계/단서/세력/진척 시트 중 실제 반복 상태만 분리.
15. **Advanced/Optional Modules** — core를 익힌 뒤 추가하는 규칙.

### 예외

- 룰 자체가 낯설고 캐릭터 생성 항목이 core loop를 이해해야 의미가 생기면 Ironsworn처럼 **Core Flow를 Character Creation보다 더 깊게 먼저** 설명한다.
- 장르 감정이 규칙 이해보다 중요하면 인세인처럼 **리플레이/만화/예시를 더 앞에** 둔다.
- 세계관이 캐릭터 권한의 hard constraint이면 Fate처럼 **setting consensus를 creation보다 먼저** 둔다.
- 전통 클래스형에서 캐릭터 판타지가 진입 동력이라면 DW/시노비가미처럼 캐릭터 생성/직업을 비교적 앞에 둔다.

---

## 5. 설계시 반드시 별도로 기록할 질문

```yaml
player_promise:
core_loop:
fictional_permission:
resolution_trigger:
who_sets_stakes:
who_sets_risk:
who_sets_effect:
outcome_bands:
resource_loop:
core_information_policy:
harm_and_recovery:
signature_system:
role_symmetry_or_asymmetry:
advancement_loop:
gm_agenda_and_procedure:
first_session_procedure:
support_artifacts:
quick_reference_surface:
optional_modules:
rights_boundary:
playtest_questions:
```

이 필드가 채워지지 않은 상태에서는 '룰북 목차가 완성됐다'고 판정하지 않는다.

---

## 6. 직접 접근 실패 / 후속 입력

- 초여명 Fate Dropbox 폴더는 publisher link임을 확인했지만 현재 direct file listing 실패. 사용자가 별도 ZIP/원본 파일을 제공하면 **페이지 순서·한국어 설명 방식·도표/시트 역할을 직접 비교**한다.
- `blog.naver.com/adventurekeeper`는 현재 direct crawl 실패. 주변 검색 결과로 코코포리아 가이드 링크임을 식별했지만 **본문 기능 설명을 이 작성자의 원문 사실로 인용하지 않는다**.
- 사용자가 추가로 제공할 룰북 ZIP은 다음 단위로 분석한다:
  1. 파일 목록/판본/언어/출처/권리 메모
  2. 실제 목차 순서
  3. 10페이지 단위가 아니라 **개념이 처음 등장→재설명→레퍼런스화되는 흐름** 추적
  4. 규칙마다 `해결하려는 플레이 문제 / 입력 / 상태 / 절차 / 출력 / 피드백 / 실패조건`
  5. 캐릭터·GM·시나리오·카드·보조 시트의 정보 소유 경계
  6. ADOPT / ADAPT / REJECT / TEST
  7. 이클립스와 Base 공용 원리를 분리

## 7. 현재 결론 ceiling

- 위 자료는 **공용 TRPG 디자인 질문·설명 순서·support artifact 원리**를 Base에 추가할 충분한 다중 사례를 제공한다.
- 특정 판정식(2d6, d20, dice pool), Fate 면모, Blades Clock, GUMSHOE Core Clue 등을 모든 TRPG의 필수 규칙으로 강제할 근거는 아니다.
- 실제 프로젝트 규칙 선택은 해당 프로젝트 Player Promise와 playtest evidence가 최종 authority다.
