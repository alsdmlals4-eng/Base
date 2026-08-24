# BCP-2026-029 — Cocos AI-native game-engine machine boundary 패턴 흡수

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base` + COCOS 4 / Cocos CLI 공개 기술 벤치마크
- 기준 Base 커밋: `2828a74f60c1ed09546171040f4178c8848ea686`
- 외부 자료 확인일: `2026-08-24`
- 제출일: `2026-08-24`
- 제안 제출 병합: PR `#643`, main `5672fb1bba267b9346c1938be8c5ac7a838256c4`
- 승인 상태 병합: PR `#644`, main `6d884218c4294608c8fe2ca9176420caad4eaae6`
- 구현 병합: PR `#646`, main `db712a9a5ff1269ee2ef7519f297694ae78b8732`
- 상태: `IMPLEMENTED`
- 지식 상태: `공식 원출처 관찰 + 사용자 승인 provider-neutral 패턴 + Base 구현/회귀 검증 완료`
- 선행 Draft 구현 증거: `https://github.com/alsdmlals4-eng/Base/pull/642` — proposal lifecycle 누락을 발견해 merge하지 않고 superseded 처리했다.

## 관찰과 증거

2026-08-24 현재 COCOS 4와 Cocos CLI의 공개 자료에서 다음 machine-facing 구조를 확인했다.

1. COCOS 4는 Cocos Creator에서 결합되어 있던 엔진과 에디터를 분리하고, AI 통합을 위해 cross-platform framework와 editor core component를 CLI tool로 옮겨 engine core capability로 통합하는 방향을 공개한다.
2. Cocos CLI는 명시적 `--project` 경로를 사용하며 `cocos start-mcp-server --project <project-path>`를 제공한다. 전역 `--no-interactive`는 CI/자동화를 위해 제공되고 build에는 `--log-dest`가 있다.
3. Cocos CLI 저장소는 unit/E2E test를 제공하며 CONTRIBUTING 문서는 MCP API schema/tool 변경 뒤 `npm run generate:mcp-types`로 E2E용 type-safe definition을 생성하도록 요구한다.
4. COCOS 4 GitHub Releases의 최신 공개 릴리스는 확인일 기준 `4.0.0-alpha.28`(2026-08-03)이다. 따라서 구조적 학습 가치는 있지만 COCOS 4 자체의 production maturity나 Godot 대체 근거로 확대할 수 없다.

1차 출처:

- https://github.com/cocos/cocos4
- https://github.com/cocos/cocos4/releases
- https://github.com/cocos/cocos-cli
- https://github.com/cocos/cocos-cli/blob/main/docs/en/commands.md
- https://github.com/cocos/cocos-cli/blob/main/docs/en/quick-start.md
- https://github.com/cocos/cocos-cli/blob/main/CONTRIBUTING.md

Base 현행과의 비교 근거:

- `docs/CAPABILITY_COMPOSITION_MAP.md`는 이미 `reusable core → stable CLI/programmatic contract → optional human surface`를 사용한다.
- P06 Godot toolchain은 HiGodot single authoring authority를 유지하며 GUT/Hera의 책임을 분리한다.
- 기존 Godot historical adapter 자료는 project identity, closed schema, evidence와 실제 behavior 검증을 분리해야 한다는 교훈을 이미 갖고 있다.

따라서 외부 엔진을 설치하지 않고도 Cocos에서 관찰한 구조를 기존 Base owner에 더 엄격한 machine boundary로 추상화할 수 있다.

## 일반화 후보

새 Skill이나 새 Tool Hub를 만들지 않고 기존 `BENCHMARKING_REFERENCE_GUIDE`와 `CAPABILITY_COMPOSITION_MAP`에 `AI_GAME_ENGINE_MACHINE_BOUNDARY`를 추가한다.

```text
exact project identity
→ typed operation
→ reusable bounded operation core
   ├─ CLI adapter
   └─ MCP adapter
→ representative behavior E2E
→ Implementation Reality Gate
→ structured execution evidence
```

공용 계약:

- `PROJECT_IDENTITY_BEFORE_OPERATION`: editor window/current directory/port를 추측하지 않고 exact project/ref/version을 먼저 결속한다.
- `SHARED_CORE_FOR_CLI_AND_MCP`: CLI와 MCP가 별도 mutation/business logic을 소유하지 않고 같은 bounded core를 호출한다.
- `SCHEMA_GENERATED_TOOL_SURFACE`: 구현 스택에 실익이 있을 때 하나의 closed schema/type source에서 CLI/MCP type·validator·fixture를 생성하거나 기계 검증해 drift를 막는다.
- `MCP_E2E_BEHAVIOR_CONTRACT`: handshake/tool listing/schema load가 아니라 대표 operation이 실제 project/result/evidence boundary까지 도달하는지 E2E로 검증한다.
- `MCP_CONNECTED_IS_NOT_BEHAVIOR_PASS`: MCP 연결 성공은 transport evidence일 뿐 engine action·persist·target identity·evidence 성공을 증명하지 않는다.
- `NONINTERACTIVE_AUTOMATION_PATH`: 승인된 bounded operation은 가능한 경우 CI/agent용 non-interactive path를 제공하되 기존 승인·보안·보호 path Gate를 우회하지 않는다.
- `STRUCTURED_EXECUTION_EVIDENCE`: exact project/ref, adapter/tool version, typed operation, result, changed/observed artifact, log/evidence location, `NOT_RUN`/`BLOCKED` 상태를 결속한다.
- `ENGINE_AND_WRITER_AUTHORITY_PRESERVED`: 이 패턴은 엔진 선택이나 persistent writer 수를 바꾸지 않는다.

## 프로젝트 전용으로 남길 내용

이번 제안은 특정 게임 프로젝트의 기획·씬·데이터·밸런스·플레이 규칙을 Base에 넣지 않는다.

또한 다음 Cocos 고유 구현은 공용 계약으로 승격하지 않는다.

- COCOS 4 runtime 및 C++ core 구현.
- TypeScript API 자체.
- Cocos CLI/Node toolchain 패키지.
- Cocos MCP server 구현.
- Cocos Wizard/editor UI 또는 extension marketplace.
- Cocos Asset Bundle 구현 세부.

현재 게임 엔진은 **Godot을 유지**한다. 현재 Base의 Godot authoring/test/live-QA owner와 single-writer 경계도 그대로 유지한다.

## 적용 조건과 비사용 조건

적용 조건:

- game engine/editor/QA tool이 사람 외에 CI 또는 AI Agent에서 반복 호출된다.
- 잘못된 project identity, schema drift, transport-only false PASS, 실행 증거 누락이 실제 위험이다.
- 기존 machine-facing interface를 유지하면서 adapter 간 의미를 통일할 필요가 있다.

비사용 조건:

- 일회성 수동 작업으로 별도 schema/codegen/E2E 계층의 유지비가 가치보다 큰 경우.
- 기존 도구가 이미 exact identity + typed operation + behavior E2E + evidence를 충족하면 새 wrapper를 만들지 않고 그대로 재사용한다.
- MCP가 필요하지 않은 작업에는 MCP를 추가하지 않는다. CLI 또는 기존 programmatic adapter만으로 충분하면 그 표면을 유지한다.
- 단지 외부 엔진에서 좋은 패턴을 발견했다는 이유만으로 해당 엔진/CLI/SDK를 dependency로 설치하지 않는다.

## 반례와 위험

### 최소 3안 비교

| 안 | 장점 | 위험·비용 | 판정 |
| --- | --- | --- | --- |
| A. COCOS 4로 엔진 이전 | Cocos의 최신 machine-facing 구조를 직접 사용 | 현재 Alpha, 기존 Godot 코드/도구/지식 이전비용, 제품 위험 증가 | `REJECT` |
| B. Cocos CLI/MCP를 별도 Godot bridge처럼 추가 | 외부 패턴을 빠르게 체험 | Cocos/Node/TS dependency 증가, Godot authoring authority 중복 가능, 공급망·유지비 증가 | `REJECT` |
| C. provider-neutral 계약만 기존 Base owner에 흡수 | Godot과 single-writer 유지, 비용 0, 여러 tool에 재사용 가능 | 문서 규칙만으로는 개별 tool behavior PASS를 보장하지 않으므로 후속 실제 E2E 필요 | `ADOPT` |

주요 반례·위험:

1. Cocos 한 사례에서 본 API를 그대로 보편 법칙으로 복제하면 과적합된다. 따라서 provider-specific syntax가 아니라 identity/core/schema/E2E/evidence 불변식만 승격한다.
2. `SCHEMA_GENERATED_TOOL_SURFACE`를 무조건 code generation으로 강제하면 작은 도구에서는 오히려 유지비가 늘어난다. generation은 실익이 있을 때만 쓰고 schema/type drift 방지 자체를 필수로 둔다.
3. MCP를 AI 친화성의 필수 조건으로 오해하면 불필요한 server/transport가 늘어난다. MCP는 adapter 중 하나이며 CLI/programmatic path가 충분하면 추가하지 않는다.
4. 외부 Alpha 제품의 방향성을 production readiness로 오인할 수 있다. COCOS 4 자체의 adoption과 pattern extraction을 분리한다.
5. 기존 HiGodot authoring authority와 충돌하는 두 번째 writer가 생기면 즉시 reject한다.

## 영향 범위와 검증

구현된 최소 범위:

- `docs/CAPABILITY_COMPOSITION_MAP.md`: provider-neutral machine boundary owner.
- `docs/BENCHMARKING_REFERENCE_GUIDE.md`: 외부 engine/tool에서 해당 패턴을 추출하는 routing.
- `docs/knowledge/cases/COCOS_AI_NATIVE_ENGINE_INTERFACE_CASE.md`: dated source observation과 ADOPT/ADAPT/REJECT 사례.
- `docs/operations/base-partitions/learning/P06_LEARNING_LOG.md`: 실제 BCP/RED/GREEN/권위 보존 교훈 checkpoint.
- `tests/test_ai_game_engine_machine_boundary_contract.py`: Godot 유지, Cocos benchmark-only, MCP transport≠behavior PASS 회귀.
- 기존 Base v9 focused CI에 위 회귀 테스트 연결.

구현 검증:

1. 정식 구현 RED Actions run `32696165900`: 승인된 최신 main에서 새 contract 부재로 의도한 실패를 재현했다.
2. GREEN Actions run `32696469871`: Base integrity/release checks와 385 focused tests가 통과했고 기존 환경 skip 1건만 유지됐다.
3. 최종 exact implementation HEAD `176bec7838802b2b7ec8aa01f3e9de4b4bad4978`: Base Partition Contract, Dependency Review, Base v9 Operating Contracts, Game Project Operating System, whole-core regression, publication validation, Windows smoke, `ci-gate`가 모두 PASS했다.
4. 기존 `test_higodot_single_authority_policy`, `test_godot_higodot_gut_hera_toolchain`과 새 machine-boundary 회귀가 함께 통과해 writer/owner 퇴행이 없음을 확인했다.
5. 최종 상태에서 최소 5회 full-scope adversarial review를 완료했고 새 유효 blocking finding 0, 회귀 0으로 pre-merge `CLEAN_REVIEW_EXIT`를 달성했다.
6. PR #646은 exact HEAD `176bec7838802b2b7ec8aa01f3e9de4b4bad4978`에서 squash merge되어 main `db712a9a5ff1269ee2ef7519f297694ae78b8732`가 됐다.

Evidence ceiling:

- 이번 BCP는 Base 공용 machine-boundary 계약과 회귀 구현 완료를 증명한다.
- Cocos runtime 채택, Cocos production readiness, 개별 Godot 프로젝트의 `BEHAVIOR_E2E_VERIFIED`, Godot 프로젝트별 schema/tool adapter 개조 완료는 주장하지 않는다.
- 실제 project/tool adapter를 변경할 때는 해당 프로젝트에서 대표 operation의 exact target/result/evidence E2E를 별도로 실행해야 한다.

## 필요한 도구·파일·권한

- 사용 항목: 기존 GitHub repository 문서·Python unittest·GitHub Actions만 사용.
- 신규 외부 dependency 설치: 없음.
- 추가 금전 비용: `0`.
- 사용 권한: 정상 branch/PR/squash merge 범위만 사용. `--admin`, ruleset bypass, force push 미사용.

## 승인과 구현

- 사용자 승인 근거: 2026-08-24 현재 작업 대화에서 사용자가 **“그렇게하자 / 기술만 흡수하고 godot엔진 계속 쓰는걸로”**라고 명시적으로 방향과 구현을 승인했다.
- `approval_ref`: `[수정제안서]/BCP-2026-029-cocos-ai-game-engine-machine-boundary/PROPOSAL.md#승인과-구현` + 2026-08-24 현재 작업 사용자 승인 + 제출 PR `#643` + 승인 PR `#644`.
- 승인 범위: Cocos의 reusable AI/CLI/MCP/schema/E2E/evidence 기술 원리만 Base 기존 owner에 흡수하고 Godot 엔진·현재 Godot writer/test/QA authority를 유지한다.
- 승인 제외: COCOS runtime/CLI/SDK 설치, Node/TypeScript 신규 dependency, 엔진 이전, 새 Tool Hub, 두 번째 Godot persistent writer, 모든 프로젝트에 MCP 강제 설치.
- 구현 PR: `https://github.com/alsdmlals4-eng/Base/pull/646`
- 구현 merge SHA: `db712a9a5ff1269ee2ef7519f297694ae78b8732`
- 롤백: 구현 contract/case/test/CI entry만 되돌린다. Cocos runtime이나 프로젝트 엔진 이전이 없으므로 프로젝트 migration rollback은 발생하지 않는다.
