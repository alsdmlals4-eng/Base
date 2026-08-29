# 2026-08-29 autonomous research / candidate-first visual policy audit

## Scope

Fresh-read 대상:

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

## External practice check

| Source | Adopted principle | Boundary |
|---|---|---|
| Godot 4.7 Best Practices / Scene organization / Project organization | 실제 Scene·Node·Resource 경계, 단일 책임, 느슨한 결합, 유지 가능한 file/asset organization 확인 | 프로젝트 정본과 실제 구현보다 높은 절대 규칙으로 사용하지 않음 |
| GitHub protected branch and required status check documentation | isolated branch, PR, latest exact-head checks, review/readback | direct main push·bypass 자동화 금지 |
| Google SRE automation guidance | 반복 수동 작업을 줄이고 reusable/self-checking automation으로 전환 | 잘못된 절차를 증폭하지 않도록 bounded scope·rollback·human decision boundary 유지 |

## Repository findings

| Repository | Image candidate policy | Research/feasibility | Long-term/automation | Action |
|---|---|---|---|---|
| Base | assistant-discovered need에 legacy two-turn barrier 존재 | 장기·대안 비교는 강함 | candidate-first와 learning owner 부족 | 공용 owner·image gate·custom template·tests 교정 |
| MylittleBoat | Base 상속, 직접 충돌 없음 | official primary re-read와 adversarial review 있음 | 작은 장기-correct change 원칙 | no change |
| urban-legend | generated result는 자동 final 아님 | official/industry comparison과 feasibility 있음 | repository-only | no change |
| ninja-survival-godot | `user explicitly asks` 전용 문구가 현재 사용자 지시와 충돌 | current research/feasibility gate 있음 | completion loop 있음 | AGENTS visual section 교정 |
| omenward | `USER_AUTHORIZED_AUTONOMOUS_REQUIRED_IMAGES` | Base fresh-read | final lock/runtime promotion 분리 | no change |
| Ten-Paces-Hidden-Moves | candidate 생성 후 final lock | external research + feasibility classification | long-term review loop | no change |
| Blacksmith | consumer 확인 후 user-preauthorized generation | every substantive task research + feasibility | post-generation lock 분리 | no change |
| Coc-Fiction | image-specific conflict 없음 | 서사 정본/검증 중심 | 완료에 stale Notion CURRENT sync 요구 | repository-only completion + research/learning 교정 |
| GRIMOIRE- | `USER_PREAUTHORIZED_GENERATE_CANDIDATE__FINAL_LOCK_ONLY` | external research/feasibility gate | final lock/runtime separation | no change |
| Switchy Express | consumer-first auto candidate | official/industry research + feasibility | long-term quality 명시 | no change |
| Tetris | `AUTO_GENERATE_THEN_USER_LOCK_CONFIRMATION` | mandatory current research + feasibility | exact-head/readback | no change |

## Selected correction

`candidate-first + post-generation user lock`을 공용 default로 채택한다.

```text
GENERATED_CANDIDATE
!= USER_APPROVED
!= CANON_REGISTERED
!= IMPLEMENTED
!= RUNTIME_VERIFIED
```

대량 프로젝트 파일을 일괄 수정하지 않는다. 이미 같은 의미를 가진 프로젝트는 Base drift를 재복제하지 않고 no-change로 보존한다.
