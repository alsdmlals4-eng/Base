# HiGodot 단일 실행 권위와 안전 운용 정책

## 1. 상태와 책임

```yaml
policy_state: APPROVED_FOR_IMPLEMENTATION
provider: hi-godot/godot-ai
execution_authority: SOLE_GODOT_EXECUTION_AUTHORITY
authority_count: 1
production_readiness: false
```

이 문서는 Base와 이를 채택한 Godot 프로젝트에서 MCP·EditorPlugin·자동화 공급자 선택, HiGodot 작업 위험도, 클라이언트 격리, 로컬 전송, 버전 고정, canary, project regression, rollback의 단일 공용 정본이다. 프로젝트는 이 규칙을 복제하지 않고 `templates/project-operations/HIGODOT_ADOPTION_RECORD.json`에서 실제 버전·Godot 버전·호스트·검증 증거만 기록한다.

## 2. 실행 권위

- `hi-godot/godot-ai`의 Godot AI addon과 MCP 서버만 실제 Godot 편집·실행 요청의 권위다.
- Base custom MCP는 `ARCHIVED_REFERENCE_AFTER_POLICY_EXTRACTION`이며 실행 권위가 아니다.
- Base custom MCP Bridge와 추가 Godot mutation addon은 `STOP_AND_ARCHIVE`다.
- Hera Agent Godot은 설치·활성화하지 않으며 `BENCHMARK_REFERENCE_ONLY`다.
- 한 프로젝트에 HiGodot과 기능이 겹치는 두 번째 MCP, HTTP/WebSocket Bridge, EditorPlugin 또는 CLI mutation authority를 동시에 두지 않는다.
- 과거 Base live-editor Adapter·Schema·Pilot·테스트는 보안·rollback·evidence 학습 자료와 역사적 실행 증거로 보존하지만, HiGodot 채택 프로젝트의 현재 실행 경로가 아니다.

### 저작 권위와 비저작 애드온의 경계

HiGodot의 단일 권위는 Godot 저작·편집 자동화와 mutation 실행 경로에 한정된다. 동일 저작 권위를 가진 두 번째 MCP·EditorPlugin·Bridge·CLI mutation authority는 금지한다.

테스트 프레임워크, 대화·서사 도구, 플랫폼 서비스, 카메라, 아이콘, 자산 제작 보조처럼 역할이 다른 비저작 애드온은 `evaluating-godot-assets-and-plugins-before-creation`의 평가와 프로젝트별 채택 기록을 통과하면 공존할 수 있다. 공존 가능성은 자동 채택을 뜻하지 않으며, 실제 필요·정확한 버전·라이선스·소비 경로·검증·제거 절차가 없으면 설치하지 않는다.

## 3. Existing Solution First Gate

새 MCP·addon·CLI·framework·SDK wrapper·automation server·tool registry·Skill·Skill Mode·공용 실행 계층을 설계하거나 구현하기 전에 다음을 완료한다.

```text
current environment inventory
→ 사용자가 이미 쓰는 도구·addon·MCP·host profile 확인
→ Base와 프로젝트의 기존 구현·dependency·설정 확인
→ 같은 Goal의 open and recently merged PR 확인
→ 유지되는 외부 대안 조사
→ 기능·보안·라이선스·호환성·유지비·전환비 비교
→ REUSE / ABSORB / REFACTOR / ARCHIVE / BUILD_NEW
→ 적대적 검토
→ 사용자에게 판정·근거·미검증 보고
→ 필요한 승인 후 설계·구현
```

필수 인벤토리에는 가능한 범위에서 다음을 포함한다.

- 현재 대화와 인수인계의 확정 결정
- connected MCP와 VS Code/Codex host profile
- `project.godot`의 enabled addon
- package·dependency manifest와 lock
- 개인 설정을 노출하지 않는 범위의 MCP 등록 여부
- Base Skill Registry·프로젝트 adapter·관련 template
- 현재 branch, open and recently merged PR, 중단된 구현
- 사용자가 이미 사용 중이라고 말한 외부 도구

### 판정

```yaml
REUSE: 기존 구현을 주 실행 권위로 사용
ABSORB: 정책·테스트·패턴만 현행 권위에 흡수
REFACTOR: 기존 구현을 제한적으로 수정해 사용
ARCHIVE: 중복되거나 위험한 구현의 활성 권위 제거
BUILD_NEW: 대안으로 충족할 수 없는 최소 범위만 신규 제작
```

`BUILD_NEW`는 다음 중 하나를 증거로 확인하고 사용자가 비교 결과를 본 뒤 승인해야 한다.

- 필수 핵심 기능이 없음
- 차단 보안·플랫폼 결함을 설정, 격리, bounded upstream patch로 해결할 수 없음
- 라이선스가 목적과 충돌함
- 유지가 중단됐거나 현실적으로 사용할 수 없음
- 요구 Godot·OS·클라이언트·성능을 충족하지 못함

“직접 만들면 더 엄격할 수 있다”는 단독 근거로는 `BUILD_NEW`를 허용하지 않는다.

## 4. 작업 위험도

HiGodot의 넓은 기능을 삭제하거나 숨기는 대신 요청 범위, Git 복구, diff, import, test, runtime 증거로 통제한다.

### L0_OBSERVE

Editor/session 상태, Scene hierarchy, Node property, Resource metadata, log, diagnostics, test discovery를 읽는다.

- 정확한 프로젝트와 Editor/session을 먼저 확인한다.
- 필요한 domain만 선택한다.
- 큰 tree·log는 bounded summary로 제한한다.

### L1_REVERSIBLE_WRITE

Node 생성·이름 변경, property 변경, script attach, 일반 Scene·Resource 저장처럼 국소적이고 복구 가능한 변경이다.

- 대상과 기대 결과를 기록한다.
- 실행 뒤 같은 대상 상태를 다시 읽는다.
- changed files와 diff를 검토한다.
- 관련 parse/import/test를 실행한다.

### L2_DESTRUCTIVE_OR_STRUCTURAL_WRITE

다음 기능을 **허용한다**.

- Node deletion
- file creation, modification, move, or deletion
- Scene 구조 재편
- project settings와 input map 변경
- autoload 추가·변경·제거
- Resource 교체
- script와 filesystem의 구조적 변경

필수 Gate:

1. 작업이 사용자가 이름 붙여 승인한 범위 안인지 확인한다.
2. 변경 전 Git status, 대상 Scene·Node·파일·설정을 기록한다.
3. branch, checkpoint commit 또는 정확한 backup으로 rollback 경로를 만든다.
4. 실행 뒤 전체 diff와 예상 밖 파일을 검토한다.
5. Godot import/parse와 영향 테스트를 실행한다.
6. 실제 실행하지 못한 runtime·device·human 검증은 `NOT_RUN`으로 남긴다.

사용자가 명시한 삭제·파일 쓰기는 같은 이름·대상 범위에서 다시 묻지 않는다. 작업 중 새 삭제 대상, 무관한 cleanup 또는 범위 확대가 발견되면 새 승인을 받는다.

### L3_HIGH_IMPACT_CHANGE

대규모 다중 파일 migration, 핵심 Scene·subsystem 삭제, 전역 project settings·autoload·input map 재구성, 저장소 전체 serialized asset rewrite다.

- 작성된 실행 계획
- 변경 전 적대적 검토
- 명시적 사용자 승인
- 격리 branch와 checkpoint commit
- 전체 project regression
- 검증된 rollback

을 모두 요구한다.

## 5. 도구 선택과 Context 제어

HiGodot 도구가 많다는 이유로 전체 schema를 기본 로드하지 않는다.

```text
작업 domain 식별
→ Editor/session readiness 확인
→ one primary domain 선택
→ minimum exact schema 또는 progressive schema discovery
→ 한 bounded operation group 실행
→ 결과 재관찰·검증
→ 이유를 기록한 경우에만 domain 전환
```

- 지원되는 경우 domain rollup과 deferred/progressive schema discovery를 사용한다.
- one primary domain 원칙을 유지한다.
- 실패 뒤 무관한 도구를 연속 추측 호출하지 않는다.
- mutation 재시도 전에 현재 상태를 다시 읽는다.
- 반환된 session, operation ID, Node reference를 사용하고 경로를 추측하지 않는다.
- 전체 Scene tree·log·tool catalog를 Context에 그대로 넣지 않고 필요한 부분만 요약한다.

## 6. 클라이언트 격리

HiGodot 서버가 같은 VS Code host 뒤의 실제 모델을 신뢰성 있게 구분한다고 가정하지 않는다.

```yaml
Godot Authoring:
  intended_client: GPT
  MCP registration: present

Codex CLI:
  intended_client: Codex
  MCP registration: present

DeepSeek Analysis:
  intended_client: DeepSeek
  MCP registration: absent
  credential: absent
  godot_read: false
  godot_write: false
```

- DeepSeek Analysis profile에는 HiGodot MCP를 등록하지 않는다.
- 프로젝트 공용 `.vscode/mcp.json`이나 `.codex/config.toml`을 활성 권위로 commit하지 않는다.
- 개인 host 설정과 credential은 프로젝트 정본·공개 저장소·evidence에 복사하지 않는다.

## 7. 로컬 전송 경계

```yaml
network_mode: LOOPBACK_ONLY
lan: LAN_FORBIDDEN
public_url: PUBLIC_URL_FORBIDDEN
port_forwarding: PORT_FORWARDING_FORBIDDEN
remote_tunnel: REMOTE_TUNNEL_FORBIDDEN
shared_or_public_pc: FORBIDDEN
```

- 로컬 개발 PC와 현재 사용자 계정에서만 실행한다.
- HiGodot의 LAN allow-list나 외부 URL 서버 모드를 사용하지 않는다.
- 공유 계정·공용 PC에서 사용하지 않는다.
- 필요하지 않을 때 Godot addon과 MCP server를 종료하거나 비활성화한다.
- 인증 강화를 위해 두 번째 Base Bridge나 fork를 즉시 만들지 않는다. upstream 개선 또는 bounded patch도 Existing Solution First Gate와 버전 검토를 통과해야 한다.

## 8. 도입 기록

프로젝트별 `HIGODOT_ADOPTION_RECORD.json`은 다음을 소유한다.

- exact release or commit
- Godot version
- Codex·GPT host 등록 상태와 DeepSeek 금지
- network mode
- enabled·unverified domain
- 설치·connection·runtime·regression 상태
- verification evidence
- rollback release or commit
- production readiness

`NOT_CONFIGURED`, `NOT_RUN`, `PARTIAL`, `PASS`, `FAIL`을 구분한다. 연결 성공, tools/list 또는 한 번의 mutation은 production readiness 증거가 아니다.

## 9. 업데이트와 Rollback

자동 무검토 업데이트는 금지한다.

```text
새 release 확인
→ release note·dependency·schema·transport·security diff
→ 호환성·적대적 검토
→ 격리 fixture 설치
→ Godot import와 plugin startup smoke
→ read canary
→ destructive canary와 exact restore
→ 대표 프로젝트 canary
→ project regression
→ 프로젝트별 단계적 적용
→ 이전 package·pin·rollback 증거 유지
```

- exact release or commit을 고정한다.
- 새 버전의 destructive canary는 삭제·파일 쓰기·project settings 변경 후 원복까지 검증한다.
- 최소 한 대표 프로젝트의 project regression 전에는 전체 프로젝트에 확산하지 않는다.
- rollback package와 이전 pin을 보존한다.
- Windows·Android·실제 Editor UI·사람 사용성처럼 실행하지 않은 환경은 `NOT_RUN`이다.

## 10. 기존 자체 구현 처리

```yaml
Base_PR_198:
  disposition: SUPERSEDED_BY_HIGODOT_POLICY_AFTER_EXTRACTION
  merge: false

Base_PR_201:
  disposition: ARCHIVED_REFERENCE_AFTER_POLICY_EXTRACTION
  merge: false

Base_PR_202:
  disposition: STOP_AND_ARCHIVE
  merge: false
```

이 정책이 검토되고 필요한 교훈이 보존되기 전에는 PR을 삭제하지 않는다. PR을 닫거나 branch를 삭제하거나 merge하는 행위는 별도 사용자 결정이다.

## 11. 실패 조건

- 현재 사용 도구·addon·MCP·관련 PR을 확인하지 않고 신규 구현 시작
- disposition·비교 근거·사용자 승인 없이 `BUILD_NEW`
- HiGodot과 겹치는 두 번째 활성 mutation authority
- 사용자가 허용한 Node 삭제·파일 쓰기·project settings 기능을 일괄 금지
- L2/L3 작업에서 rollback·diff·import·test 누락
- DeepSeek profile에 HiGodot 등록 또는 credential 제공
- LAN·public URL·port forwarding·remote tunnel 사용
- floating latest 또는 자동 무검토 업데이트
- connection 성공을 runtime·regression·production readiness로 승격
- 과거 Base Adapter·MCP 파일 존재를 현재 실행 권위로 해석
- HiGodot 단일 권위를 비저작 애드온 전면 금지로 오해해 검증된 테스트·대화·플랫폼 도구까지 배제
- 역할이 다른 애드온이라는 이유만으로 평가·소비 경로·rollback 없이 일괄 설치

## 12. 실행 보고

```yaml
provider: hi-godot/godot-ai
provider_pin:
project_and_editor_identity:
client_profile:
operation_level: L0/L1/L2/L3
primary_domain:
requested_scope:
changed_targets:
git_checkpoint:
rollback:
import_and_parse:
tests:
runtime:
human:
unverified:
production_readiness: false
```
