# 2026-08-29 autonomous research / candidate-first visual policy audit

## Scope

2026-08-29 KST에 latest completed default branch, root `AGENTS.md`, current authority, live open PR을 대상으로 fresh-read했다.

- `alsdmlals4-eng/Base`
- `MylittleBoat`
- `urban-legend`
- `ninja-survival-godot`
- `omenward`
- `Ten-Paces-Hidden-Moves`
- `Blacksmith`
- `Coc-Fiction`
- `GRIMOIRE-`
- `Switchy-Express-Cargo-Puzzle`
- `Tetris`

Archive-only 또는 이번 게임/서사 작업정책 범위 밖:

- `ninja-survival-unity-archive-Unity-`
- `CodexUsageTray`

## User-approved target

```text
NEEDED_IMAGE
→ current canon / existing approved visual / actual or planned consumer readback
→ bounded image-model candidate first
→ user LOCK / REVISE / REJECT / REFERENCE_ONLY
→ explicit repository promotion
→ implementation
→ runtime verification

MATERIAL_STRUCTURE_OR_IMPLEMENTATION
→ current implementation and reuse readback
→ current official / primary Internet research
→ directly relevant industry success / failure evidence
→ alternatives and long-term total-cost comparison
→ actual project feasibility classification
→ implementation or exact implementation handoff
→ verification and correction

RETAINED_CHANGE
→ actual minimum five full-scope adversarial loops
→ validated finding is corrected or explicitly blocked
→ exact-head regression/readback evidence
```

## External practice check

| Primary source | Adopted principle | Boundary |
|---|---|---|
| Godot 4.7 Best Practices / Applying object-oriented principles in Godot | Scene은 reusable·instantiable object이며 single responsibility·encapsulation을 적용할 수 있다. 실제 Scene·Node·Resource·Script 책임과 consumer를 확인한다. | 프로젝트 정본과 실제 구현보다 높은 절대 규칙으로 사용하지 않는다. Node·scene을 필요 이상으로 분해하지 않는다. |
| GitHub Docs — protected branches / required status checks | isolated branch/PR, exact latest head의 required checks, conversation/readback gate를 사용한다. strict check가 필요하면 base 최신 상태와의 호환도 확인한다. | direct main push, force push, ruleset/admin bypass를 자동화하지 않는다. 과거 Green을 새 head Green으로 재사용하지 않는다. |
| Google SRE Workbook — Eliminating Toil | 반복 작업을 측정하고 ROI·안전장치·human fallback을 갖춘 작은 단계적 자동화로 줄인다. automation은 unsafe state에서 사람에게 fail closed한다. | 자동화 자체가 목표가 아니다. 잘못된 절차의 자동 반복, 과설계, 높은 유지비는 거절한다. |
| Google SRE — Postmortem Culture | 문제·영향·root cause·수정·재발 방지 action을 durable record와 추적 가능한 후속 작업으로 남긴다. | `교훈을 얻었다`는 서술만으로 learning 완료를 주장하지 않는다. owner/test/checker/handoff 중 durable output이 필요하다. |

## Repository findings

| Repository | Fresh finding | Action |
|---|---|---|
| Base | candidate-first·research·automation 초안은 존재했으나 기존 v4.9 capability와 local asset vault route를 회귀시켰고, 최소 5회 실제 adversarial evidence가 회귀 테스트로 강제되지 않았다. 같은 목적의 PR #780/#781/#782도 중복됐다. | #782를 current implementation path로 수렴하고 기존 v4.9 owner를 복구한다. local vault·reference freshness·evidenced review receipt·tests를 추가한다. #780의 강한 review contract만 선별 재사용한다. |
| MylittleBoat | main은 material decision의 official read와 adversarial review를 요구하지만 minimum five actual loops와 candidate-first post-lock 상태 계약이 불완전하다. 같은 목적의 PR #105/#106이 중복됐다. | 더 완전한 current-task PR 한 개로 수렴하고 exact-head verification 후 중복을 종료한다. |
| urban-legend | repository-only와 5회 large-integration review는 있으나 current image owner에 candidate-first/post-lock/local asset state를 명확히 동기화해야 한다. 같은 목적의 PR #341/#342가 중복됐다. root `AGENTS.md`는 별도 PR #231 보호 경로다. | root 보호 경로를 침범하지 않는 더 완전한 current-task PR 한 개로 수렴한다. |
| ninja-survival-godot | research/feasibility와 minimum five loops는 이미 강하다. main의 `Do not generate ... unless the user explicitly asks`가 최신 candidate-first 지시와 직접 충돌한다. PR #131/#133이 중복됐다. | product canon·PR #49를 보호하면서 image gate만 current-task PR 한 개로 교정한다. |
| omenward | `USER_AUTHORIZED_AUTONOMOUS_REQUIRED_IMAGES`, repository-only, final lock/runtime promotion 분리가 이미 존재한다. Phase 2 Issue·RED·provenance gate는 프로젝트 고유 보호 경계다. | no change. Base 일반화로 프로젝트 Phase 2 gate를 제거하지 않는다. |
| Ten-Paces-Hidden-Moves | 생성 전 별도 승인 없이 candidate 후 final lock, current research/feasibility, every-task review와 material five loops가 존재한다. | no change. |
| Blacksmith | consumer requirement 뒤 user-preauthorized generation, current research, implementation feasibility, adversarial loop와 explicit promotion이 존재한다. | no change. |
| Coc-Fiction | 게임 runtime이 아닌 서사 프로젝트다. main completion이 아직 Notion CURRENT write/readback을 요구하고, current research·장기 automation·actual five-loop evidence 계약이 없다. | repository-only completion, 서사에 맞는 research/feasibility, actual adversarial receipt와 durable learning을 별도 PR로 교정한다. Godot 규칙은 적용하지 않는다. |
| GRIMOIRE- | `USER_PREAUTHORIZED_GENERATE_CANDIDATE__FINAL_LOCK_ONLY`, repository-only, external research/feasibility, material five loops가 존재한다. | no change. |
| Switchy-Express-Cargo-Puzzle | consumer-first candidate, official/industry research, actual Godot feasibility, five full loops와 long-term quality가 존재한다. | no change. |
| Tetris | planning candidate-first, runtime exact consumer requirement, targeted official research, feasibility classification, five loops와 exact-head readback이 존재한다. | no change. |

## Selected correction architecture

### Adopt

- Base는 공용 default와 evidence schema만 소유한다.
- 프로젝트는 고유 approval·engine·consumer·product gate를 유지한다.
- candidate 생성, user lock, repository promotion, implementation, runtime verification을 분리한다.
- material retained change는 claim-only review가 아니라 actual five-loop receipt와 correction evidence를 요구한다.
- 기존 capability를 삭제하는 wholesale rewrite보다 current owner에 최소 delta를 적용한다.

### Adapt

- Google SRE식 automation 원칙을 1인 개발 규모에 맞춰 `bounded safe continuation + human fallback + durable repository learning`으로 축소 적용한다.
- Godot best practice는 실제 프로젝트의 Scene/Node/Resource/Script feasibility checklist로 적용하되 프로젝트 고유 구조를 덮지 않는다.

### Reject

- per-image routine preapproval
- candidate를 final asset/runtime proof로 자동 승격
- 문서상 feasible을 실제 구현 가능으로 과장
- 사용자 관여 최소화를 core meaning·high-risk approval 제거로 해석
- `5회 검토했다`는 문구만 남기는 claim-only review
- 새 정책 도입을 이유로 기존 v4.9 recovery/Skill/Codex/local-vault capability를 삭제
- 모든 프로젝트 `AGENTS.md`의 일괄 재작성

## Evidence ceiling

이 audit는 repository policy·static contract evidence다. 이미지 생성, Godot runtime, Human UX, device/export, release evidence는 `NOT_RUN`이며 이 문서로 승격하지 않는다.
