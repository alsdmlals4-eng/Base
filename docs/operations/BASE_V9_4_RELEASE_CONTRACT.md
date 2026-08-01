# Base v9.4 AI Operations Release Contract

## 1. 목적

Base v9.4는 released Base v9.3 위의 호환 후보 계층이다. 다음 두 승인 범위를 함께 전달하지만 독립 책임으로 유지한다.

- Issue #113 / BCP-2026-003: 모델·추론 단계 라우팅, Prompt caching, 비용 추정·실측·재보정
- Issue #115 / BCP-2026-004 / `DEC-2026-08-01-001`: 지시 권위, Interface-first Prompt, Context 큐레이션, Artifact-first 전달, 게임 UI 모션

## 2. 보호 경계

- `base-v9.3.lock.json`, v9.3 payload·evidence·pin을 재작성하지 않는다.
- BCP-2026-003과 BCP-2026-004의 Skill·Method·Reference·Test 책임을 합치지 않는다.
- BCP-2026-004를 위해 새 활성 Skill이나 외부 `ui-skills` 의존성을 추가하지 않는다.
- provider 가격·context·cache 조건은 확인일이 있는 profile로 관리한다.
- 프로젝트 저장소·Google Sheets·Godot 코드·Scene·Resource는 후보 PR 범위 밖이다.

## 3. 후보 신원

`base-v9.4.lock.json`이 현재 v9.4 후보 Registry raw bytes를 소유한다.

```yaml
artifact_role: BASE_V9_4_RELEASE_CANDIDATE_LOCK
release_line: v9.4.0
release_state: RELEASE_CANDIDATE
candidate_release_commit: null
candidate_release_evidence_commit: null
candidate_registry:
  path: skills/SKILL_REGISTRY.json
  sha256: RAW_FILE_BYTES_SHA256
```

후보 PR은 자신의 payload Commit이나 evidence Commit을 미리 적지 않는다.

## 4. 단계

```text
1. proposal-only PR #114, #117
2. v9.4 candidate implementation PR #118
3. candidate payload merge to trusted main
4. separate trusted-main evidence PR
5. separate pin-finalization PR
6. six project adoption audits and PRs
```

### Candidate

- proposal 상태를 `APPROVED_FOR_IMPLEMENTATION`으로 전환하고 `approval_ref`와 implementation PR을 연결한다.
- Skill·Method·Reference·Template·Registry·Test·lock을 구현한다.
- exact HEAD에서 required CI와 적대적 검토 P0/P1=0을 확인한다.

### Trusted evidence

- 병합된 payload Commit과 exact Registry identity를 기록한다.
- candidate lock의 release pins는 여전히 null이다.
- 실제 실행한 자동 검증과 `NOT_RUN` 제한을 분리한다.

### Pin finalization

- trusted main history에 payload와 evidence가 모두 존재한 뒤 `BASE_RELEASED`로 전환한다.
- 두 40자 Commit SHA와 Registry identity를 고정한다.
- 과거 v9.3 evidence를 수정하지 않는다.

## 5. 자동 검증

- v9.4 focused contract
- Skill Registry·frontmatter·package integrity
- BCP lifecycle·approval linkage
- candidate lock schema·Registry raw SHA-256
- reference freshness·Documentation Map·consumer propagation
- full Python regression
- generated artifact consistency
- `git diff --check`
- required `ci-gate`와 `adversarial-gate`

## 6. 증거 상한

Base 후보에서 다음은 실행하지 않은 상태로 남긴다.

```text
provider billing·cache hit·실제 비용 절감 → NOT_RUN
실제 ChatGPT 모델 자동 전환 → NOT_APPLICABLE
Godot UI 모션·목표 기기 성능 → NOT_RUN
사람 UI 이해·피로 → HUMAN_NOT_RUN
프로젝트 저장·Schema·런타임 회귀 → 프로젝트 적용 단계
```

문서와 자동 Test 통과를 위 항목의 성공 증거로 과장하지 않는다.

## 7. 프로젝트 적용

릴리스 pin 확정 뒤 다음 순서로 프로젝트별 최신 main·로컬 Base 사본·기획 정본·실제 구현을 감사한다.

1. `Ten-Paces-Hidden-Moves`
2. `Blacksmith`
3. `omenward`
4. `urban-legend`
5. `GRIMOIRE-`
6. `Switchy-Express-Cargo-Puzzle`

각 프로젝트는 독립 Issue·Branch·PR·Decision·검증을 사용한다. 프로젝트 코어·세계관·수치·저장 Schema·승인 자산은 Base 기본값으로 덮어쓰지 않는다.

## 8. 롤백

- candidate 실패: PR #118을 닫거나 revert하고 released v9.3을 계속 사용한다.
- evidence 실패: evidence PR을 닫고 candidate payload를 수정 릴리스로 교정한다.
- pin 이후 결함: 과거 history를 rewrite하지 않고 새 호환 수정 릴리스를 만든다.
