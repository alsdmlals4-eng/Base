# GPT 이미지 생성·검수 및 프로젝트 Google Sheets 운영 정책

이 문서는 Base를 적용한 프로젝트에서 **B(프로젝트 Sheet 구조) → C(GPT 이미지 생성·검수 실행 흐름) → A(Base 공용 정책·Skill·라우팅)** 순서로 기획 산출물을 관리하는 공용 책임 원본이다.

## 1. 적용 범위와 권한

- Base 저장소 자체의 Sheet 상태는 `BASE_EXCLUDED`다.
- 유효한 프로젝트 Sheet URL·권한·tab이 확인되면 `PROJECT_SHEET_CONFIGURED`다.
- 정확한 Sheet가 확인되지 않으면 `NOT_CONFIGURED`이며 새 Sheet를 추정 생성하거나 임의 파일을 수정하지 않는다.
- 프로젝트 정본·최신 사용자 승인·실제 구현이 이 정책보다 우선한다.
- GPT 생성 이미지는 승인 전까지 정본·최종 자산·구현 완료 증거가 아니다.
- 생성 이미지는 자동 최종 자산으로 승인하지 않는다.

## 2. B — 프로젝트 Google Sheets 구조

프로젝트 Sheet는 단순 작업 목록이 아니라 게임의 의미 구조와 승인 상태를 한눈에 복원하는 작업면이다.

필수 탭:

```text
00_프로젝트_허브
01_작업순서
02_현재_확정결정
03_근거_라이브러리
04_누락_충돌_감사
10_제품방향
11_세계관
12_핵심루프
13_주요인물
14_조연_세력_관계
20_코어경험_데모목표
30_데모범위_품질기준_제작기반
40_핵심시스템_메인콘텐츠
41_성장_경제
50_메인콘텐츠
51_미니게임                    # 해당 프로젝트만
52_글쓰기_서사                 # 해당 프로젝트만
60_UX_UI_접근성
70_아트_오디오_에셋
71_이미지기획_생성목록
72_이미지검수_승인로그
80_데모_버티컬슬라이스_플레이테스트
90_본제작_출시_사업
98_Base_반영후보
99_변경이력
```

프로젝트의 기존 정본 문서가 이미 같은 책임을 소유하면 Sheet는 해당 경로·Decision ID·상태를 연결하며 독립 정본을 새로 만들지 않는다.

## 3. C — GPT 이미지 생성 실행 흐름

### 3.0 Visual Requirement Gate

프로젝트용 이미지·목업을 생성 목록에 넣기 전에 `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`의 `Visual Requirement Gate`에서 필요성·Delete Test·재사용 후보·역할·우선순위·제작 방식을 먼저 **선정**한다.

- 프로젝트 자산 후보는 가능한 한 `requirement_id`를 가진다. `GENERATE_EXPLORATION` 또는 승인된 `CREATE_CUSTOM` 판정을 이미지 생성 입력으로 사용한다.
- 프로젝트 전체·화면군·캐릭터군처럼 여러 자산을 일괄 생성할 때는 선정되지 않은 후보를 “있으면 좋을 것”이라는 이유만으로 자동 추가하지 않는다.
- Delete Test에서 관찰 가능한 손실이 없거나 기존 텍스트·컴포넌트·프로젝트 자산으로 충분하면 `DEFER/CUT/REUSE`를 우선하고 이미지 생성을 기본값으로 삼지 않는다.
- 사용자가 현재 대화에서 특정 이미지 한 장의 생성·편집을 명시적으로 요청한 경우 그 요청 자체를 **현재 작업의 임시 requirement**로 처리할 수 있다. 다만 그 결과를 프로젝트의 지속 자산 목록·`ASSET_MANIFEST.yml`·승인 상태에 자동 승격하지 않는다.
- `REFERENCE_ONLY`나 `GENERATE_EXPLORATION` 결과는 방향 비교·정보 위계 검토용이며 제품 자산 승인과 분리한다.
- 선정된 `requirement_id`는 이미지 기획·검수 기록, 로컬 vault 후보, 최종 승인·promotion 이후 `ASSET_MANIFEST.yml` 연결까지 추적 가능하게 유지한다.

이 Gate는 “무엇을 생성할 것인가”를 결정하며 실제 파일 존재·승인 자산 권위를 새로 소유하지 않는다.

### 3.0A IMAGE_TWO_TURN_HARD_BARRIER

프로젝트용 이미지 생성·편집은 `IMAGE_TWO_TURN_HARD_BARRIER`를 따른다. 이미지가 실제로 필요한지 판단하기 전에 프로젝트 전체 핵심 방향·관련 시스템·기존 승인 Visual/Asset·현재 구현 상태를 읽고 `PROJECT_REVIEW_COMPLETE`를 확보한다.

```text
PROJECT_REVIEW_COMPLETE
→ VISUAL_NEED_DEFINED
→ TEXT_BRIEF_COMPLETE
→ STOP_REQUIRED

[next user message]
→ EXPLICIT_IMAGE_APPROVAL
→ GENERATE_EXACTLY_ONE
→ STOP_REQUIRED

[next user message]
→ APPROVE | REVISE | REJECT
```

- **동일 assistant 응답에서** `TEXT_BRIEF_COMPLETE` 직후 이미지 생성으로 이어가지 않는다. 텍스트 brief를 사용자에게 보여준 응답은 `STOP_REQUIRED`로 끝낸다.
- 다음 사용자 메시지에서 해당 brief의 실제 이미지 제작이 명시적으로 승인된 경우에만 `EXPLICIT_IMAGE_APPROVAL`로 승격한다.
- 한 승인 단위에서는 `GENERATE_EXACTLY_ONE`을 기본으로 하고, 생성 뒤 다시 `STOP_REQUIRED`로 종료한다. 여러 후보를 자동 연속 생성하거나 `이미지 생성 → 사용자 채팅 없이 다음 이미지 생성`으로 이어가지 않는다.
- 이미지가 필요한 화면/에셋이 여러 개여도 프로젝트 전체를 먼저 검토해 우선순위를 정하고, 각 이미지별 brief·승인·생성·검토 상태를 분리한다.
- 사용자가 현재 대화에서 이미 특정 이미지 한 장의 생성을 명시적으로 요청했고 그 이미지의 대상/범위가 충분히 확정되어 있는 경우 그 메시지 자체가 해당 이미지의 `EXPLICIT_IMAGE_APPROVAL`이 될 수 있다. 그러나 프로젝트 전체 자산 일괄 생성, 후속 변형 자동 생성, 새로운 별도 이미지까지 포괄 승인한 것으로 확장하지 않는다.
- 이 barrier는 승인 전 이미지 생성을 막는 대화/기획 Gate이며, 생성 성공·업로드·Notion 배치·runtime 적용·제품 자산 승격의 증거를 대신하지 않는다.

### 3.1 기획 중 시각화

목적은 텍스트 기획의 방향·가독성·구현 가능성을 빠르게 비교하는 것이다.

대표 산출물:

- 세계관 분위기와 장소 톤 보드
- 주요 인물·조연·세력 실루엣과 관계 장면
- 핵심루프·핵심시스템 설명 목업
- UI·카드·상점·전투·대화 화면 목업
- Vertical Slice 대표 장면과 플레이 화면 가설

상태는 `GENERATED_EXPLORATION`이며 제품 자산으로 자동 승격하지 않는다.

### 3.2 기획 종료 시 실사용 후보

기획 승인 뒤 Demo-First Vertical Slice와 소개 자료에 사용할 수 있는 수준의 후보를 만든다.

대표 산출물:

- 대표 키아트·캡슐·배너·썸네일 후보
- 캐릭터 승인 후보와 표정·포즈·상태 시트
- UI 고도화 목업과 실제 화면 합성
- 시스템 소개 이미지·카드·장비·스킬 예시
- 상점 페이지·트레일러·프레스킷용 시각 후보

이 단계도 `APPROVED_CANDIDATE`이며 라이선스·실제 화면·구현·후처리 검증 전에는 `PROJECT_ASSET_APPROVED`가 아니다.

### 3.3 상태 흐름

```text
PLANNED
→ GENERATED_EXPLORATION
→ IN_REVIEW
├─ REVISION_REQUIRED → 재생성·편집 → IN_REVIEW
├─ REJECTED
└─ APPROVED_CANDIDATE
   → 실제 화면·규격·권리·후처리·구현 검수
   → PROJECT_ASSET_APPROVED
   → APPLIED_AND_RUNTIME_VERIFIED
```

### 3.4 프로젝트 로컬 보존소와 자산 승격

프로젝트별 로컬 이미지 보존·Godot 연결의 공용 책임 원본은 `docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md`다.

보존소가 구성된 프로젝트에서는 다음 경계를 사용한다.

```text
GENERATED_EXPLORATION / IN_REVIEW / APPROVED_CANDIDATE
→ .asset-vault/library/                    # local authority
→ sync
→ assets/_vault_local/                     # local only, gitignored, Godot-visible
→ PROJECT_ASSET_APPROVED
→ promote
→ assets/<approved-path>/                  # tracked
→ ASSET_MANIFEST.yml·권리/출처·정본 갱신
→ tracked Scene/Resource 연결
→ APPLIED_AND_RUNTIME_VERIFIED
```

- 승인 전 이미지는 `.asset-vault/`와 `assets/_vault_local/`에서 보존·비교·Godot preview할 수 있지만 tracked 제품 자산으로 자동 생성하지 않는다.
- `PROJECT_ASSET_APPROVED`가 된 후보만 `python tools/project_asset_vault.py promote ...`로 Repo 자산에 승격한다.
- 승격 시 `vault_source_key`, tracked path, 권리·출처, 승인 상태와 사용처를 `ASSET_MANIFEST.yml` 및 관련 provenance 기록에 연결한다.
- tracked Scene/Resource는 `res://assets/_vault_local/...`를 장기 참조하지 않는다. commit/PR 전 `python tools/project_asset_vault.py check --project-root .`로 검사한다.
- 사용자가 로컬 후보를 삭제하면 이후 AI 작업·preview 후보 집합에서 제외하고 자동 부활시키지 않는다. 이미 `PROJECT_ASSET_APPROVED` 후 promote된 tracked 자산은 별도 제품 자산이므로 로컬 후보 삭제만으로 자동 폐기하지 않는다.
- 로컬 vault를 볼 수 없는 원격 작업자는 `VAULT_LOCAL_STATE_UNVERIFIED`를 유지한다.
- ChatGPT 웹 사용은 브라우저 다운로드 + 로컬 watcher가 기본 브리지다. 브라우저 다운로드까지 제거한 zero-click 보존은 로컬 생성/API 프로세스가 vault에 직접 쓰는 경우에만 주장한다.

### 3.5 Primary Use Gate → Reusable Visual Harvest Gate

이미지 작업의 기본 순서는 **`proposal -> user approval -> production -> primary use -> harvest review`**다. 처음부터 모든 결과를 재사용 파츠로 만들지 않고, 승인된 시각안으로 제작한 이미지가 먼저 본래 사용처에서 목적을 달성하게 한다. `primary-use success`와 `reuse promotion`은 별도 판정이며, 재사용성을 이유로 `title-specific identity`, 감정, 정보 위계, 구도를 약화시키지 않는다.

```text
기존 승인 자산 / Figma Visual Bible 조회
→ 이미지·사진 시각안 제안
→ 사용자 승인
→ 이미지 제작
→ Primary Use Gate
→ Reusable Visual Harvest Gate
→ 필요한 요소만 구조화·레이어화·semantic rebuild
→ 재사용 자산·구조 패턴·Visual DNA 축적
→ 다음 작업에서 우선 재사용·변형
```

제작 중 `textless master`, `clean plate`, `transparent source`처럼 비용이 낮고 자연스러운 separation hint는 보존할 수 있다. 그러나 이런 보조 산출물이 본 이미지의 composition·연출·가독성을 지배해서는 안 된다.

Harvest 후보는 다음 분류를 사용한다.

- `REUSE_AS_IS`: 동일 bytes/구조를 독립적으로 다시 사용한다.
- `VARIANT_SEED`: 승인 자산을 상태·색·테마 변형의 기준으로 쓴다.
- `STRUCTURE_PATTERN`: 픽셀이 아니라 layout·hierarchy·interaction 구조를 재사용한다.
- `STYLE_DNA`: palette·shape·material·lighting·camera·spacing 같은 시각 문법을 재사용한다.
- `REBUILD_FOR_REUSE`: crop보다 Figma Component/Variant, Godot Theme/Scene/Resource 등 semantic rebuild가 안전하다.
- `ONE_OFF_KEEP`: 현재 목적에는 중요하지만 공용화 가치가 낮은 hero/narrative/title-specific 표현을 그대로 보존한다.
- `REJECT_REUSE`: 오류·중복·권리·품질·정체성 위험 때문에 재사용하지 않는다.

분리·재구축 방법은 위험이 낮은 순서로 사용한다.

```text
SOURCE_LAYER
→ MASK_CUTOUT
→ MANUAL_OR_SEMANTIC_REBUILD
→ DERIVED_GENERATIVE_RECOVERY
```

`SOURCE_LAYER`는 원래 독립된 source를 사용하고, `MASK_CUTOUT`은 관측된 픽셀만 분리한다. `MANUAL_OR_SEMANTIC_REBUILD`는 특히 UX/UI처럼 상태·확장·현지화·접근성이 필요한 요소에 우선한다. `DERIVED_GENERATIVE_RECOVERY`는 가려진 영역을 생성 복원한 결과이며 원본에서 관측된 사실이 아니라 **derived generated pixels**로 provenance를 분리하고 별도 검수한다.

Harvest 완료나 Figma reuse reference 등록만으로 제품 자산 승인 상태를 올리지 않는다. `Reusable Visual Harvest Gate`는 `PROJECT_ASSET_APPROVED`, `promote`, Figma `04_FINAL`, tracked asset, Godot runtime proof를 자동 생성하거나 대체하지 않는다.

## 4. 이미지 검수 계약

모든 이미지·목업은 다음을 검사한다.

1. 기획·세계관·캐릭터·시스템 정본 일치성
2. 핵심 경험·세일즈포인트 전달력
3. 실제 화면 크기·HUD·VFX·배경 위 가독성
4. 구현 가능성·제작 비용·기술 규격
5. 다른 자산과의 형태·색·재질·광원 일관성
6. 재사용성·편집 가능성·현지화 가능성
7. 손·관절·무기·문자·로고·원근·광원 오류
8. 특정 상업 IP·작가 스타일과의 과도한 유사성
9. 원본·레퍼런스·모델·서비스·버전·프롬프트·생성일 기록
10. 승인자·사용처·GitHub 경로·Sheet row·자산 원장 연결
11. 프로젝트 자산 후보라면 연결 `requirement_id`와 선정 근거가 존재하는지 확인

## 4.1 참조 기반 독립 제작

공용 기준은 `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`다.

발견 레퍼런스는 원본을 약간 바꾸거나 AI로 다시 생성하는 입력이 아니라, 기능·정보 위계·일반 제작 원리를 분석하기 위한 `REFERENCE_TO_ORIGINAL` 입력으로 분류한다.

```yaml
reference_sources:
reference_brief:
forbidden_expression:
final_asset_record:
reference_similarity_status:
```

- `reference_brief`에는 프로젝트 목적·정보 구조·일반 형태·재질·광원·가독성 원리만 남긴다.
- `forbidden_expression`에는 식별 가능한 캐릭터, 실루엣·의상·소품 조합, 구도, 로고, UI skin, 특정 작가 스타일을 기록한다.
- 참조 원본은 build·store·trailer·marketing package에 포함하지 않는다.
- 최종 생성물은 별도 `final_asset_record`와 모델·서비스·버전·약관 날짜·입력 권리·프롬프트·후처리를 가진다.
- `reference_similarity_status`가 `PASS`가 아니거나 입력 권리·약관이 미확인이면 `RELEASE_BLOCKED_UNVERIFIED`다.

AI 재생성, image-to-image, 부분 편집 또는 overpaint는 원출처·입력 권리·유사성 검토를 면제하지 않는다.

## 5. 승인·정본·동기화

승인된 이미지 Decision은 다음을 같은 승인 단위에서 갱신한다.

```text
CURRENT_CONFIRMED_DECISIONS
→ 아트·UI·세계관·캐릭터·시스템 책임 원본
→ GitHub Issue·PR·main
→ 71_이미지기획_생성목록
→ 72_이미지검수_승인로그
→ Asset License Ledger·Asset Registry
→ ASSET_RIGHTS_AND_PROVENANCE_RECORD
→ GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK
→ 실제 적용 경로와 런타임 검증
```

보존소가 활성화된 프로젝트에서는 `PROJECT_ASSET_APPROVED → promote → tracked path → ASSET_MANIFEST.yml` 연결도 같은 승인 단위에 포함한다.

Sheet가 `NOT_CONFIGURED`이면 GitHub 정본까지만 갱신하고 상태를 거짓으로 `SHEET_SYNCED` 처리하지 않는다.

## 6. 적대적 검토

각 단계 종료 시 `running-adversarial-review-and-refinement: repository-wide-audit`로 다음을 공격한다.

- Visual Requirement Gate에서 선정되지 않은 프로젝트 자산을 관성적으로 대량 생성했는가
- `IMAGE_TWO_TURN_HARD_BARRIER`를 건너뛰어 동일 assistant 응답에서 brief와 생성이 이어졌는가
- `GENERATE_EXACTLY_ONE` 뒤 자동 후속 이미지를 생성했는가
- 승인 전 생성 이미지가 최종 자산처럼 사용됐는가
- 승인 전 vault 후보가 tracked Repo 자산으로 자동 승격됐는가
- tracked Scene/Resource가 `assets/_vault_local/`을 참조하는가
- 사용자가 제거한 후보를 stale 다운로드/문맥이 다시 살렸는가
- 기획 변경 뒤 이미지·목업이 stale 상태인가
- 이미지 Decision이 문서·Sheet·자산 원장 중 일부에만 있는가
- 세계관·핵심루프·인물·핵심시스템 탭이 비어 있거나 다른 탭에 중복 정본화됐는가
- v7·구형 Prompt·구형 Sheet tab을 활성 경로가 계속 참조하는가
- 원출처·라이선스·유사성 검토가 빠졌는가
- 참조 원본이 제품 package에 남거나 `reference_brief`가 식별 가능한 표현을 유지하는가
- AI 변환을 독립 제작 증거로 오해했는가
- 실제 화면 검수 없이 예쁜 원화만 승인했는가
- Primary Use Gate 전에 재사용 편의를 위해 본 화면 품질·정체성을 희생했는가
- `ONE_OFF_KEEP`가 정상인데도 모든 이미지를 강제로 component/layer library로 승격했는가
- `DERIVED_GENERATIVE_RECOVERY` 픽셀을 원본의 관측 사실로 기록했는가
- Harvest 판정을 `PROJECT_ASSET_APPROVED` 또는 runtime proof로 오해했는가

차단 Finding은 `MUST_FIX`, 권리·출처·약관·유사성 판정 불가는 `RELEASE_BLOCKED_UNVERIFIED`로 기록한다.
