# Candidate-first visual · research-to-implementation · autonomous learning design

**Date:** 2026-08-29  
**Status:** USER_APPROVED / IMPLEMENTATION_IN_PROGRESS  
**Scope:** Base 공용 정책과 프로젝트별 충돌 교정

## Goal

다음 네 사용자 목표를 하나의 충돌 없는 실행 모델로 만든다.

1. 필요한 이미지는 기존 프로젝트 내용·시안·승인 Visual을 읽고 candidate를 먼저 제작한 뒤 사용자가 최종 확정한다.
2. 중요한 실제 구현·구조는 최신 공식/1차 자료, 인터넷 벤치마크, 현업 성공·실패 사례와 현재 프로젝트 구현을 함께 확인해 현실성을 판정한다.
3. 빠른 임시 완료보다 장기 총비용·유지보수성·재사용성·완성도를 우선한다.
4. 사용자는 핵심 의미·최종 lock·고위험 변경에만 관여하고 나머지는 자동화·최적화·학습 loop로 이어간다.

## Alternatives

### A. 기존 two-turn 이미지 사전 승인 유지

- 장점: 생성 비용과 방향 오판을 가장 보수적으로 통제한다.
- 단점: 이미 승인된 프로젝트 작업에서도 이미지마다 중단하며 사용자의 반복 개입이 커진다.
- 판정: `REJECT`. 새 사용자 목표와 직접 충돌한다.

### B. 이미지 생성부터 정본·runtime 승격까지 전자동

- 장점: 가장 적은 사용자 개입.
- 단점: 취향·정체성·권리·제품 의미를 AI가 임의 확정하고 잘못된 asset이 자동 확산될 위험이 크다.
- 판정: `REJECT`.

### C. candidate-first + post-generation user lock

- 장점: 기존 시각 정본과 consumer를 기반으로 실물을 먼저 검토하면서도 final direction·canon·runtime promotion은 사용자가 통제한다.
- 단점: 상태 관리와 provenance 기록이 필요하다.
- 판정: `ADOPT`.

선택된 상태 모델:

```text
NEEDED
→ BRIEF_READY
→ GENERATED_CANDIDATE
→ REVIEWED
→ USER_APPROVED
→ CANON_REGISTERED
→ IMPLEMENTED
→ RUNTIME_VERIFIED
```

## Research and implementation design

중요한 구조의 권장 흐름:

```text
current authority and implementation
→ reuse-first
→ current official/primary research
→ industry success/failure/mixed cases
→ >= 3 viable alternatives
→ ADOPT / ADAPT / REJECT
→ implementation feasibility packet
→ actual implementation or exact Codex handoff
→ verification / readback / correction
```

Godot 4.7 공식 Best Practices는 scene 자립성, 느슨한 결합, 단일 책임과 프로젝트 구조의 유지보수성을 강조한다. 따라서 정책은 “문서상 좋은 구조”가 아니라 실제 Scene/Node/Resource/Script와 consumer 경계를 확인하도록 한다.

GitHub 공식 protected-branch 지침은 PR, 최신 HEAD의 required status checks, review와 conversation resolution을 통해 안전한 자동화를 구성할 수 있음을 보여 준다. 따라서 자동화는 main bypass가 아니라 branch/PR/exact-head verification으로 진행한다.

Google SRE의 automation 원칙은 자동화가 force multiplier이지만 잘못된 절차도 증폭할 수 있으므로 well-defined scope, rollback, self-checking system이 필요하다고 설명한다. 따라서 이 정책은 사용자 버튼 반복을 줄이되 핵심 의미·final lock·고위험 행위는 자동 승인하지 않는다.

## Authority design

- Base 장기 작업 원칙은 `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`에 유지한다.
- 새 세부 owner는 `docs/AUTONOMOUS_RESEARCH_IMPLEMENTATION_AND_LEARNING_POLICY.md`다.
- 이미지 생성과 확정은 `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md` 및 `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`가 소유한다.
- 맞춤형 지침은 `templates/custom-instructions.gpt.md`에서 bootstrap만 제공한다.
- 프로젝트 고유 AGENTS가 더 엄격하거나 다른 소비처·권리 Gate를 명시하면 프로젝트 규칙이 우선한다.

## User decision boundary

자동 진행:

- fresh-read, research, reuse search, alternative comparison
- candidate image production
- feasibility packet
- tests/readback/correction
- documentation and learning capture
- remaining-work recalculation

사용자 결정:

- core player experience / product meaning
- major narrative or world canon
- final Visual Direction / asset lock
- irreversible migration/deletion
- external release, security/permission, new cost
- evidence로 우열을 정할 수 없는 취향 선택

## Evidence ceiling

```text
research complete != feasibility proven
feasibility proven != implemented
automated test pass != runtime pass
generated candidate != user approved
user approved != canon registered
canon registered != runtime verified
```

## Rollback

- 모든 repository 변경은 latest completed main에서 만든 isolated branch/PR로 진행한다.
- 기존 open PR은 read-only다.
- 새 정책이 프로젝트 고유 Decision과 충돌하면 Base default가 아니라 프로젝트 owner를 보존하고 local override를 기록한다.
- candidate는 lock 전 정본·runtime에 연결하지 않으므로 시각 방향 rollback 비용을 제한한다.
