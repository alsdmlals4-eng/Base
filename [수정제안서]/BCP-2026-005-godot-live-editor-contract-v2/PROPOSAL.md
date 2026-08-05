# BCP-2026-005 — Godot Live Editor 안전 계약 v2 정규화

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base`
- 기준 커밋: `ea0442ddb7fb9286d093cc96e523fdd74a841c22`
- 최신 구현 기준점: PR #152 HEAD `42e9988a6f4a9f7f2bb433d121d23c785be18fcb`
- 제출일: `2026-08-05`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 지식 상태: `패턴`
- 승인 근거: `https://github.com/alsdmlals4-eng/Base/pull/154#issuecomment-5187157323`

## 관찰과 증거

Draft PR #152는 Godot CLI·EditorPlugin·runtime-debugger 자동화를 프로젝트 소유 adapter로 제한하면서 실제 Godot 4.7.1 격리 Pilot과 CI 증거를 확보했다. 그러나 단일 `operation_class`가 부작용, 멱등성, 승인, 실행 수명, 재시도 위험을 함께 표현해 다음 조합을 정확히 모델링하지 못한다.

- 승인받아야 하는 멱등 mutation
- 장기 read-only 작업
- 승인·장기·멱등 속성을 동시에 가진 작업
- 가역 mutation과 비가역 mutation의 구분

PR #153의 hardening은 수명 축 분리, 의미 validator, 증거 상태 결속의 필요성을 증명했지만 움직인 parent와 분기됐다. PR #154의 승인된 설계는 이 문제를 예외 추가가 아니라 v2 독립 정책 축으로 해결한다.

## 일반화 후보

Base의 Godot 자동화 안전 계약을 다음 원칙으로 정규화한다.

1. `effect_kind`, `idempotency`, `approval_policy`, `execution_mode`, `rollback_policy`를 독립 축으로 둔다.
2. 승인·ledger·task·result를 프로젝트뿐 아니라 automation server, Editor instance, runtime session과 계약 snapshot에 결속한다.
3. Capability는 닫힌 `input_schema`와 `output_schema`를 선언한다.
4. mutation은 관찰 revision/hash와 dirty state precondition을 사용하고 불일치 시 실행 전에 중단한다.
5. LOCAL_HTTP, STDIO, named pipe는 transport 종류별 인증·Origin·session·OS 접근 제약을 기계적으로 검증한다.
6. file-backed PASS 증거는 제한된 경로와 SHA-256을 요구한다.
7. 장기 작업은 protocol-neutral task core를 사용하고 MCP Tasks는 선택 profile로 매핑한다.
8. EditorPlugin 시작 실패는 Godot `--recovery-mode` 복구 경로를 명시한다.

## 프로젝트 전용으로 남길 내용

- 실제 Godot MCP server, EditorPlugin server, runtime bridge 구현
- 특정 프로젝트 Scene·Node·Resource·signal·input 경로
- user project의 test framework와 export pipeline
- Godot 4.7.1 격리 Pilot의 GDScript 구현 및 캡처된 runtime 증거
- 물리 입력 및 사람 사용성 판정

## 적용 조건과 비사용 조건

적용 조건:

- typed Godot capability를 CLI, EditorPlugin 또는 runtime debugger로 실행하는 프로젝트
- 파일·Editor·runtime 상태를 변경하거나 장기 task를 관리하는 자동화
- 승인, 재시도, rollback, 증거 무결성 경계가 필요한 작업

비사용 조건:

- 일반 Godot 자산·plugin 평가만 필요한 경우
- read-only 문서 작성이나 engine과 무관한 일반 Base 작업
- 범용 MCP server 또는 프로덕션 원격 제어를 Base가 직접 소유하려는 경우
- 실제 runtime·project test·human evidence 없이 readiness를 주장하려는 경우

## 반례와 위험

- 정책 축을 분리해도 semantic equality 검증이 없으면 다른 target·catalog의 승인 재사용이 가능하다.
- localhost bind만으로 DNS rebinding이나 session fixation을 막을 수 없다.
- output Schema를 검증하지 않으면 성공 envelope가 잘못된 결과 구조를 숨길 수 있다.
- stale observation을 mutation에 사용하면 사람의 동시 편집을 덮어쓸 수 있다.
- v1과 v2를 동시에 active로 유지하면 선택 권위가 이중화된다.
- runtime Pilot을 같은 change set에 포함하면 static contract와 engine behavior 증거가 혼합될 수 있다.

따라서 v1은 미출시 Draft 이력으로만 보존하고 active v2 파일로 교체하며, runtime Pilot 재구현은 static v2 GREEN 후 별도 단계로 둔다.

## 영향 범위와 검증

예상 영향:

- Godot canonical contract·security·readiness 문서
- capability manifest·operation envelope Schema v2
- project template manifest·adapter·AGENTS fragment
- semantic validator
- Godot contract·routing·freshness·회귀 테스트
- 기존 Pilot 문서의 v2 후속 경계

필수 검증:

- test-only RED commit 후 최소 구현 GREEN
- 정책 조합, target/snapshot binding, transport, output, stale precondition, task, recovery 반례
- 현재 parent+implementation merge ref 전체 CI
- canonical-reference freshness
- Registry blob·Base v9.4.3 release lock 불변
- unresolved MUST_FIX와 review thread 0

## 필요한 도구·파일·권한

- 필요 항목: GitHub branch/PR 쓰기, Python 3.12, `jsonschema==4.26.0`, 기존 Base CI
- 필요한 이유: Schema·semantic validator·회귀 테스트와 exact-head 검증
- 설치·적용 방법: 기존 `.github/validation-requirements.txt`와 required workflow 사용
- 설치 후 확인 명령: `python -m unittest tests.test_godot_live_editor_contract tests.test_godot_live_editor_contract_v2 -v`
- 최소 권한: Base 저장소 feature branch push와 Draft PR 생성; main 직접 push·release lock 수정 권한은 사용하지 않음

## 승인과 구현

- 사용자 승인 근거: `https://github.com/alsdmlals4-eng/Base/pull/154#issuecomment-5187157323`
- 승인 범위: v2 구현 계획 작성과 별도 구현 PR의 TDD 실행
- 제외 범위: 병합, 프로덕션 MCP readiness, user game project 적용, release/Registry 변경
- 구현 PR: `계획 PR 생성 후 연결`
- 롤백: v2 구현 branch/PR을 닫고 PR #152의 현재 v1 Draft 상태로 복귀한다. main과 released Base 파일은 변경하지 않는다.
