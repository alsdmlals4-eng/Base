# Benchmark-First Modular UI — 파생 Packet 검사 계약

Status: `ACTIVE_SUBORDINATE_CONTRACT`.
Parent: `BENCHMARK_FIRST_MODULAR_UI_PRODUCTION.md`.
Checker: `tools/validate_player_surface_plan.py`.
Evidence ceiling: `STRUCTURE_ONLY_NOT_RUNTIME_OR_USER_APPROVAL`.

## 1. 목적

프로젝트 정본을 대체하지 않고, 승인 범위에서 선언한 화면·행동·상태·이미지 부품·조합 관계의 구조적 누락을 fail-closed로 찾는다. packet은 임시 파생 검토본이다. 사용자 승인 authenticity, 실제 파일·texture·consumer 존재, 버튼 동작, 저장 복원, 인게임 가독성은 native project owner와 runtime evidence가 증명한다.

## 2. Source identity

```yaml
schema_version: 1
artifact_role: DERIVED_REVIEW_PACKET
repository: owner/repo
source_revision: 40-character-lowercase-git-sha
scope_owner: repository locator
approval_ref: approval/decision locator
benchmark_order: EXTERNAL_THEN_PROJECT_FIT
asset_strategy: MODULAR_PARTS_FIRST
```

`repository`는 canonical `owner/repo` identity다. URL·로컬 경로·branch 이름을 넣지 않는다. 각 segment는 영문 소문자·숫자·`_ . -`를 사용할 수 있지만 `.` 또는 `..`만으로 구성할 수 없다. `./.` 등 path traversal처럼 해석될 수 있는 표기는 `SOURCE_IDENTITY`다. 유효한 project identity가 없으면 외부 source와 자기 저장소를 안전하게 비교할 수 없으므로 external benchmark 판정도 fail-closed다.

## 3. 외부 reference

각 reference는 source, evidence_kind, origin, version, observed, apply, reject, verification을 가진다. `SOURCE_CODE` 또는 `PRODUCT_OBSERVATION`이 `origin=EXTERNAL`이고 공개 HTTP(S) locator일 때만 외부 비교 분모를 충족한다. 프로젝트 내부 문서는 `origin=PROJECT` / `INTERNAL_REUSE`로 기록한다.

GitHub source에서 `source_repository`를 쓰면 canonical `owner/repo`이며 URL의 저장소와 일치해야 한다. 자기 저장소, localhost, private/loopback IP, credentials 포함 URL, malformed port, control/whitespace가 있는 locator는 외부 비교 증거가 아니다. 이것은 출처 형식 검사이며 실제 원문 접근·라이선스·연구 시점을 증명하지 않는다.

## 4. Surface·action·state

- `required_surfaces`와 `required_actions`는 승인된 분모에서 독립 투영한다.
- 모든 required surface는 entry에서 도달 가능하고 return/exit 경로가 있어야 한다.
- required action의 source가 도달 가능해야 하며 non-exit target도 return/exit 가능해야 한다.
- `SCREEN / PAGE / TAB / MODAL / DIALOGUE / PANEL / OVERLAY`를 지원한다.
- surface의 모든 `states`는 `state_bindings`를 통해 해당 surface를 대상으로 하는 family/state/method에 연결한다.
- 계획된 consumer는 `PLANNED`, 실제 연결된 consumer만 `IMPLEMENTED`다.

## 5. Native UI와 raster module

`NATIVE_UI` family는 새 bitmap의 소유자가 아니다. raster `module_ids`를 생략하거나 `null` 또는 빈 배열로 둔다. native 상태 표현은 `state_methods`와 실제 Theme/Control owner에 연결한다.

모든 raster module은 하나 이상의 non-native family가 소유해야 한다. family는 module IDs뿐 아니라 사용할 target surfaces를 선언한다. composition에 배치된 `(surface, module_id)`마다 같은 module을 소유하는 non-native family의 `surfaces`에 그 surface가 있어야 한다.

```text
family A: module frame → surfaces [dialogue]
composition: frame → settings
=> RASTER_MODULE_TARGET_UNOWNED: settings/frame
```

전체 프로젝트의 다른 화면에서 module이 한 번 계약되었다는 사실은 새 target의 사용 권한·layout 검수를 대신하지 않는다. 같은 module을 여러 surface에서 재사용하려면 family targets를 명시적으로 확장하거나, 의미·상태가 다른 variant family/assembly를 만든다.

## 6. Composition 완전성

- composition은 target surface, assembly owner, style family, required slots, parts와 approval locator를 가진다.
- 각 required slot은 한 번만 채우고 undeclared slot을 넣지 않는다.
- family가 A/B module을 요구한다면 target마다 **하나의 assembly가 A+B 전체**를 포함해야 한다. 서로 다른 두 부분 assembly의 합집합으로 handoff를 통과하지 않는다.
- module은 compatible style family, integer pixel canvas, normalized anchor, alpha, version, manifest locator와 readiness를 가진다.
- `FRAME` family에는 실제 `FRAME` module과 valid source/slice/padding/stretch/small-size 계약이 필요하다.
- 기능 텍스트·변동 수치·hit target은 이미지에 bake하지 않는다.

## 7. Readiness·승인

```text
NEEDED → BRIEF_READY → GENERATED_CANDIDATE → REVIEWED
→ USER_APPROVED → CANON_REGISTERED → IMPLEMENTED → RUNTIME_VERIFIED
```

`CANDIDATE`는 `GENERATED_CANDIDATE`의 compatibility alias일 뿐 승인 상태가 아니다. handoff는 `USER_APPROVED` 이상만 허용하고 family/module 각각 approval locator를 요구한다. composition approval은 별도다. 높은 readiness를 구조 검사가 확인해도 그 상태의 진실성이나 runtime를 증명하지 않는다.

## 8. CLI 결과

```text
STRUCTURE_VALID      exit 0
STRUCTURE_INVALID    exit 1
INPUT_ERROR          exit 2
```

missing `--packet`, 잘못된 `--gate`, malformed JSON, duplicate key, non-finite number, oversized input 등 parser-level argument error와 input error는 stdout의 ASCII-safe JSON envelope로 기록한다. stderr usage text와 traceback을 완료 증거로 사용하지 않는다. 정상 `--help`는 예외적으로 exit 0의 도움말이다.

## 9. 검증·도입

```text
python <Base>/tools/validate_player_surface_plan.py --packet <derived.json> --gate plan
python <Base>/tools/validate_player_surface_plan.py --packet <derived.json> --gate handoff
```

프로젝트에 이미 같은 의미의 validator가 있으면 그것을 우선한다. 이 checker를 설치했다는 사실만으로 프로젝트 기획, 이미지, 구현, 인게임 캡처 또는 Human 검수가 완료되지 않는다. 프로젝트가 Base를 fresh-read할 때는 자신의 `AGENTS.md`, 채택 contract pin, 실제 owner를 먼저 보존하고 이 계약을 additive workflow reference로만 사용한다.
