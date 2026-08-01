# Base v9.4 AI Operations Release Contract

## 1. 목적과 현재 상태

Base v9.4는 released Base v9.3 위의 **검증 완료 호환 계층**이다. 다음 두 승인 범위를 함께 전달하지만 독립 책임으로 유지한다.

- Issue #113 / BCP-2026-003: 모델·추론 단계 라우팅, Prompt caching, 비용 추정·실측·재보정
- Issue #115 / BCP-2026-004 / `DEC-2026-08-01-001`: 지시 권위, Interface-first Prompt, Context 큐레이션, Artifact-first 전달, 게임 UI 모션

현재 기계 신원:

```yaml
release_state: BASE_RELEASED
payload_commit: a728712cb776ec98f4875914a580fcf7d0156593
trusted_evidence_commit: ef1fba11167e4da0b298123b0c85ebd268191a42
registry_sha256: 693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59
```

## 2. 보호 경계

- `base-v9.3.lock.json`, v9.3 payload·evidence·pin을 재작성하지 않는다.
- BCP-2026-003과 BCP-2026-004의 Skill·Method·Reference·Test 책임을 합치지 않는다.
- BCP-2026-004를 위해 새 활성 Skill이나 외부 `ui-skills` 의존성을 추가하지 않는다.
- provider 가격·context·cache 조건은 확인일이 있는 profile로 관리한다.
- 프로젝트 저장소·Google Sheets·Godot 코드·Scene·Resource는 Base release payload 범위 밖이다.

## 3. 릴리스 신원

`base-v9.4.lock.json`이 released v9.4의 Registry raw bytes와 payload/evidence ancestry를 소유한다.

```yaml
artifact_role: BASE_V9_4_RELEASE_CANDIDATE_LOCK
release_line: v9.4.0
release_state: BASE_RELEASED
candidate_release_commit: a728712cb776ec98f4875914a580fcf7d0156593
candidate_release_evidence_commit: ef1fba11167e4da0b298123b0c85ebd268191a42
candidate_registry:
  path: skills/SKILL_REGISTRY.json
  sha256: 693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59
  hash_definition: RAW_FILE_BYTES_SHA256
```

## 4. 완료된 릴리스 단계

```text
1. proposal-only PR #114, #117
2. v9.4 candidate implementation PR #118
3. candidate payload merge `a728712cb776ec98f4875914a580fcf7d0156593`
4. trusted-main evidence PR #120
5. trusted evidence merge `ef1fba11167e4da0b298123b0c85ebd268191a42`
6. pin-finalization PR
```

### Candidate

- proposal 상태를 `APPROVED_FOR_IMPLEMENTATION`으로 전환하고 `approval_ref`와 implementation PR을 연결했다.
- Skill·Method·Reference·Template·Registry·Test·lock을 구현했다.
- exact HEAD에서 required CI와 적대적 검토 P0/P1=0을 확인했다.

### Trusted evidence

- 병합된 payload Commit과 exact Registry identity를 별도 evidence JSON으로 기록했다.
- 실제 실행한 자동 검증과 `NOT_RUN` 제한을 분리했다.
- evidence PR에서는 release pins를 null로 유지했다.

### Pin finalization

- trusted main history의 payload와 evidence ancestry를 검증한 뒤 `BASE_RELEASED`로 전환한다.
- 두 40자 Commit SHA와 Registry identity를 고정한다.
- 과거 v9.3 evidence를 수정하지 않는다.

## 5. 자동 검증

- v9.4 focused contract
- Skill Registry·frontmatter·package integrity
- BCP lifecycle·approval linkage
- released lock schema·Registry raw SHA-256
- payload → evidence → trusted history ancestry
- evidence JSON Schema와 payload·Issue #113/#115·Registry 연결
- reference freshness·Documentation Map·consumer propagation
- full Python regression
- generated artifact consistency
- `git diff --check`
- required `ci-gate`와 `adversarial-gate`
- Ubuntu·Windows publication smoke

## 6. 증거 상한

다음은 Base 릴리스에서 실행하지 않은 상태로 남긴다.

```text
provider billing·cache hit·실제 비용 절감 → NOT_RUN
실제 ChatGPT 모델 자동 전환 → NOT_APPLICABLE
Godot UI 모션·목표 기기 성능 → NOT_RUN
사람 UI 이해·피로 → HUMAN_NOT_RUN
프로젝트 저장·Schema·런타임 회귀 → 프로젝트 적용 단계
```

문서와 자동 Test 통과를 위 항목의 성공 증거로 과장하지 않는다.

## 7. 프로젝트 적용

```yaml
project_adoption: NOT_STARTED
release_dependency: NONE
execution_boundary: SEPARATE_PROJECT_ISSUE_BRANCH_PR
```

프로젝트 적용은 완료된 v9.4 릴리스 단계가 아니라 별도 post-release wave다. 실행 전까지 프로젝트별 감사·PR을 완료로 보고하지 않는다.

릴리스 pin 확정 뒤 다음 순서로 프로젝트별 최신 main·로컬 Base 사본·기획 정본·실제 구현을 감사한다.

1. `Ten-Paces-Hidden-Moves`
2. `Blacksmith`
3. `omenward`
4. `urban-legend`
5. `GRIMOIRE-`
6. `Switchy-Express-Cargo-Puzzle`

각 프로젝트는 독립 Issue·Branch·PR·Decision·검증을 사용한다. 프로젝트 코어·세계관·수치·저장 Schema·승인 자산은 Base 기본값으로 덮어쓰지 않는다.

## 8. 롤백

- pin-finalization 실패: PR을 닫고 candidate payload와 trusted evidence를 보존한 채 이전 verified Base pin을 계속 사용한다.
- pin 이후 결함: 과거 history를 rewrite하지 않고 새 호환 수정 릴리스를 만든다.
- 프로젝트 적용 실패: 해당 프로젝트 PR만 revert하며 Base released identity를 수정하지 않는다.
