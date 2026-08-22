# GPT Custom Instructions Alignment Design

## Status

`APPROVED_DIRECT_REQUEST` — 2026-08-22

## Goal

ChatGPT 맞춤설정을 Base와 프로젝트의 두 번째 정본으로 만들지 않고, **장기간 유지되는 사용자 선호와 최신 정본으로 진입하는 bootstrap 규칙만 보존**하도록 재설계한다.

## Problem

현재 `templates/custom-instructions.gpt.md`와 `docs/CUSTOM_INSTRUCTIONS_GUIDE.md`는 2026-07-10 시점 구조를 전제로 하며 현재 Base와 다음 지점에서 어긋난다.

- GPT 기본 역할에 폐기된 `HTML 대시보드`가 남아 있다.
- 현재 `DOMAIN_SPLIT_CANON` — Notion human-facing canon / repository structured+runtime canon / Google Sheets migration-only — 가 반영되지 않았다.
- 현재 Base가 소유하는 PR 보호, evidence gate, benchmark/alternative/adversarial/reality validation을 맞춤설정이 자체 규칙으로 재복제할 위험이 있다.
- 프로젝트 실제 작업의 권위 순서가 현재 `AGENTS.md`와 다르다.
- `docs/DOCUMENTATION_MAP.md`는 `docs/knowledge/ai/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`를 가리키지만, canonical Method는 현재 `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`에 있다. old path가 없어 과거 참조와 map route가 깨진다.

이 상태에서는 Base가 개선될수록 맞춤설정이 다시 낡고, 과거 규칙이 최신 프로젝트 작업을 오염시킬 수 있다.

## External product evidence

OpenAI의 현재 제품 문서 기준:

- Custom Instructions는 사용자가 ChatGPT 응답에 반영할 지속 지침을 제공하는 기능이며 Plus/Pro 계열에서는 최대 5,000자를 저장할 수 있다.
- Personality는 답변의 스타일과 톤을 조정할 뿐 기능·안전 규칙을 변경하지 않으며 Custom Instructions와 Memory와 함께 작동한다.
- Characteristics는 제공되는 계정에서 brevity/tone/formatting/emoji 등의 스타일을 추가 조정한다.

References:

- https://help.openai.com/en/articles/8096356-chat-preferences-for-chatgpt
- https://help.openai.com/en/articles/11899719
- https://help.openai.com/en/articles/20001038-characteristics-in-chatgpt

## Alternatives

### A. Full Base mirror in Custom Instructions

Base의 현재 PR/검증/벤치마킹/적대적 검토 규칙을 맞춤설정에 복사한다.

**Reject.** 초기 강제력은 높지만 Base가 변경될 때 즉시 drift가 생기며, 같은 정책의 복수 authority를 만든다.

### B. User preference only

한국어, 초보자 설명, 게임 기획 성향처럼 사용자 성향만 맞춤설정에 둔다.

**Reject as sole strategy.** 가장 안정적이지만 새 채팅에서 프로젝트 정본과 Base로 진입하는 routing contract가 약하다.

### C. Stable bootstrap + dynamic canon routing

맞춤설정에는 장기 사용자 선호, 비용/이미지 생성 경계, 권위 순서의 큰 틀, 최신 Base/프로젝트 규칙을 실제로 읽는 bootstrap만 둔다. 세부 Gate와 프로젝트 사실은 현재 정본에서 읽는다.

**Adopt.** drift를 최소화하면서 새 채팅에서도 작업 진입 품질을 유지하고, `DOMAIN_SPLIT_CANON`과 Base의 학습형 구조를 보존한다.

## Design

### Layer 1 — Product personalization

- Base style and tone 권장값: `Professional`.
- Personality는 작업 authority가 아니라 표현 스타일이다.
- Characteristics가 제공되면 낮은 emoji, 높은 formatting/structure, 낮거나 중립적인 brevity를 권장하되 Base policy로 강제하지 않는다.

### Layer 2 — Stable Custom Instructions bootstrap

맞춤설정은 두 책임으로 분리한다.

1. **About the user / stable context**
   - 1인 초보 게임 개발자, Godot/GDScript 중심.
   - 한국어와 실제 따라 할 수 있는 설명 선호.
   - 플레이어 감정·선택·보상·기억·첫인상·차별점·판매 포인트 우선.
   - 추가 유료비용 최소화, 무료·로컬·현재 연결 도구 우선.
   - 명시적 이미지 생성/편집 요청이 있을 때만 이미지 생성.

2. **Response / work behavior**
   - 최신 사용자 지시와 현재 프로젝트 정본을 우선한다.
   - 기억·과거 대화를 현재 프로젝트 사실로 승격하지 않는다.
   - 프로젝트 작업 전 최신 `AGENTS.md`, Active Context, 승인 계약, 분야별 정본과 실제 evidence를 확인한다.
   - `DOMAIN_SPLIT_CANON`에 따라 Notion과 repository의 소유 도메인을 구분한다.
   - L1 이상 작업의 상세 benchmark/alternative/adversarial/reality/PR Gate는 숫자와 절차를 복제하지 않고 **현재 채택된 Base 규칙을 실제로 읽고 실행**한다.
   - 현재 세션의 연결 Tool로 확인·수행할 수 있는 작업을 추정이나 불필요한 handoff로 대체하지 않는다.
   - 작은 선택은 안전한 권장안으로 연속 진행하고, 새로운 핵심 기획 결정·정본 충돌·위험 권한·큰 범위 확대만 사용자 결정으로 올린다.

### Layer 3 — Dynamic authority

구체적인 프로젝트 사실과 작업 절차는 맞춤설정이 소유하지 않는다.

```text
latest user instruction
→ project AGENTS/security/engine/data rules
→ Active Context + approved work contract
→ registered domain canon + actual code/data/assets/tests/runtime evidence
→ adopted Base contract
→ Base remote
→ external references / memory / past conversation / inference
```

`DOMAIN_SPLIT_CANON`:

```text
Notion
→ human-facing project overview / planning / visual direction / asset catalog / human-editable tables / Flow / Storyboard

Repository
→ Markdown / JSON / game data / code / scene / resource / config / tests / runtime truth

Google Sheets
→ migration compatibility only when unique unmigrated material remains
```

### Human / AI surface boundary

Notion Project Home은 사람에게 필요한 핵심 이해를 우선한다. Prompt, Hash, internal ID, Implementation Path 등 machine metadata는 AI/System surface에서 유지하고 기본 Human Home에 노출하지 않는다.

### Memory boundary

Memory는 장기 사용자 선호와 재사용 가치가 높은 개인 작업 성향을 보조한다. 현재 진행도, PR 번호, 구현 완료 여부, 시스템 최신 수치, 일회성 작업 상태, 교체된 도구 정책은 프로젝트 정본을 대체하지 않는다.

### AI instruction Method compatibility

`docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`가 canonical owner다. 과거 `docs/knowledge/ai/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md` 참조를 모두 즉시 찾아 고치는 대신 old path에 **content duplication이 없는 `COMPATIBILITY_ALIAS_ONLY` router**를 둔다.

```text
old path
→ COMPATIBILITY_ALIAS_ONLY
→ canonical game-development Method
```

Alias는 Method 내용을 복사하지 않고 canonical path와 custom-instructions guide를 안내한다. 이 방식은 과거 참조를 깨지 않으면서 복수 authority를 만들지 않는다.

## Files

- Modify `templates/custom-instructions.gpt.md`
  - 두 책임 영역을 copy-paste 가능한 형태로 제공한다.
  - deprecated HTML/dashboard 및 stale fixed-route를 제거한다.
- Modify `docs/CUSTOM_INSTRUCTIONS_GUIDE.md`
  - stable bootstrap vs dynamic canon 경계를 명시한다.
  - Product Personalization / Memory / Base routing 관계를 설명한다.
- Create `docs/knowledge/ai/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`
  - `COMPATIBILITY_ALIAS_ONLY` router로 canonical Method와 custom-instructions guide를 연결한다.
- Leave `templates/custom-instructions.codex.md` unchanged in this change.
  - Codex template의 별도 stale-read audit은 독립 범위로 남긴다. GPT 설정 교정과 묶어 역할 범위를 불필요하게 확대하지 않는다.

## Acceptance criteria

1. GPT template에 `HTML 대시보드`, Google Sheets 기본 workspace, 과거 고정 read-order가 current behavior로 남지 않는다.
2. GPT template이 `DOMAIN_SPLIT_CANON`과 최신 authority routing을 설명한다.
3. L1 상세 Gate를 custom instructions에 복제하지 않고 current Base contract를 다시 읽도록 한다.
4. Guide가 stable/volatile 정보 경계를 명확히 설명한다.
5. `docs/DOCUMENTATION_MAP.md`가 가리키는 old AI instruction path가 compatibility alias로 실제 resolve되고, alias는 canonical content를 복제하지 않는다.
6. canonical Method는 `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md` 하나로 유지된다.
7. 변경 브랜치의 diff와 destination readback을 검증한다.
8. PR merge 뒤 main에서 GPT template, guide, compatibility alias와 canonical target을 다시 읽어 반영을 확인한다.
