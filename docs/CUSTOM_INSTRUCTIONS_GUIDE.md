# Custom Instructions Guide

이 문서는 ChatGPT, Codex 같은 AI 도구의 맞춤형 지침을 **현재 Base·프로젝트 정본과 충돌하지 않는 bootstrap layer**로 설계하고 유지하는 공용 기준이다.

## 1. 핵심 원칙

맞춤형 지침은 **짧고 안정적이며 장기간 유지되는 행동 기준**만 담는다. 프로젝트 사실이나 Base의 세부 절차를 복제하는 두 번째 정본으로 만들지 않는다.

```text
Custom Instructions
→ stable user/work preferences + authority bootstrap

Memory
→ long-lived preference/context aid

latest user request
→ current task intent

project AGENTS + Active Context + approved contract
→ current project operating authority

Notion / repository
→ domain-specific canon and evidence

adopted Base contract
→ current shared operating rules
```

맞춤설정이나 Memory와 현재 프로젝트 정본이 충돌하면 최신 사용자 지시와 현재 프로젝트/Base authority를 우선한다.

## 2. Stable bootstrap에 넣을 것

다음은 여러 채팅과 프로젝트에서 장기간 재사용되므로 맞춤설정에 적합하다.

- 사용자 역할과 숙련도처럼 장기적으로 안정적인 작업 맥락.
- 기본 언어와 설명 깊이: 예를 들어 초보 개발자가 따라 할 수 있도록 경로·명령·이유·확인 방법을 설명한다는 선호.
- 플레이어 가치, 핵심 경험, 차별점, 판매 포인트처럼 지속적인 기획 판단 기준.
- 비용 경계: 무료·로컬·현재 연결된 도구 우선, 추가 유료비용은 장기 가치가 명확할 때만 제안.
- 이미지 생성·편집처럼 사용자가 명시적 요청을 요구하는 capability boundary.
- 기억·과거 대화를 현재 정본으로 승격하지 않는 규칙.
- 최신 프로젝트 `AGENTS.md`, Active Context, 승인 계약, 분야별 정본, 실제 evidence를 다시 읽는 authority bootstrap.
- `DOMAIN_SPLIT_CANON`처럼 장기적인 정본 분할 원칙.
- 세부 Gate를 복제하지 않고 현재 채택된 Base 규칙을 실제로 읽고 실행한다는 dynamic lookup rule.

## 3. 맞춤설정에 넣지 않을 것

다음은 시간이 지나면 쉽게 stale해지므로 프로젝트/Base 정본에 둔다.

- 현재 프로젝트 진행률, 현재 milestone, 현재 blocker.
- PR·Issue 번호와 open/merged 상태.
- 특정 시스템의 최신 수치, 밸런스 값, 구현 완료 여부.
- 긴 세계관·캐릭터·아이템·콘텐츠 명세.
- 구체적인 코드 파일 전체 목록이나 현재 branch/SHA.
- 일회성 작업 지시와 임시 오류/성공 로그.
- 현재 Base의 세부 Gate 횟수·체크리스트를 독립 authority처럼 복사한 내용.
- 폐기되었거나 migration-only인 도구를 기본 작업면으로 만드는 지시.
- 장기간 유지할 이유가 없는 특정 벤치마크 목록.

Base의 현재 Gate가 최소 대안 수, 적대적 검토 횟수, PR 보호, runtime evidence 등의 세부값을 바꾸더라도 맞춤설정은 다시 복사할 필요가 없어야 한다. **맞춤설정은 current Base contract를 읽는 방법을 소유하고, Base가 실제 절차를 소유한다.**

## 4. 권위와 `DOMAIN_SPLIT_CANON`

프로젝트 작업의 기본 권위는 다음과 같이 해석한다.

```text
latest user instruction
→ project AGENTS/security/engine/data rules
→ Active Context + approved work contract + confirmed decisions
→ registered domain canon + actual code/data/assets/tests/runtime evidence
→ adopted Base contract
→ Base remote
→ external references / memory / past conversation / inference
```

도구별 정본은 하나의 도구에 몰아넣지 않는다.

```text
NOTION_HUMAN_FACING_CANON
→ 사람이 읽고 비교·수정하는 프로젝트 개요·기획·시각 방향·에셋 카탈로그
→ human-editable budget/tier/roster/economy/progression tables
→ Flow / Storyboard / visual relationship surface

REPOSITORY_STRUCTURED_CANON + REPOSITORY_RUNTIME_TRUTH
→ Markdown / JSON / game data / code / scene / resource / config / tests
→ build/runtime evidence

Google Sheets
→ unique unmigrated material이 남은 경우의 migration compatibility only
```

Notion 승인, 이미지 업로드, static mockup, 맞춤설정 문구 자체는 runtime 구현 증거가 아니다.

## 5. ChatGPT 제품 Personalization

제품 설정은 작업 authority와 분리해서 본다.

- 이 작업 방식의 기본 Base style and tone 권장값은 **Professional**이다. 정제된 구조와 정확한 표현이 문서·검수·기술 설명에 적합하다.
- Personality는 응답의 스타일과 톤을 조정할 뿐 프로젝트 정본, 도구 권한, 안전 규칙, 실제 실행 증거를 바꾸지 않는다.
- Characteristics가 계정에 제공되면 formatting/structure를 높이고 emoji는 낮게, brevity는 낮거나 중립으로 두는 편이 장문 검수·초보자 설명에 적합하다. 기능 제공 여부와 UI는 OpenAI 제품에서 바뀔 수 있으므로 강제 Base contract로 취급하지 않는다.
- Custom Instructions 제품 제한도 변할 수 있다. 2026-08-22 OpenAI Help 기준 Plus/Pro 계열의 저장 한도는 최대 5,000자지만, 실제 적용 전 현재 공식 Help를 재확인한다.

현재 제품 근거:

- https://help.openai.com/en/articles/8096356-chat-preferences-for-chatgpt
- https://help.openai.com/en/articles/11899719
- https://help.openai.com/en/articles/20001038-characteristics-in-chatgpt

## 6. ChatGPT 맞춤설정 기준

ChatGPT용 공용 원본은 `templates/custom-instructions.gpt.md`다.

템플릿은 두 책임을 분리한다.

1. **ChatGPT가 알아야 할 안정적 사용자 맥락**
2. **ChatGPT가 최신 정본으로 진입하고 작업하는 방법**

UI가 두 입력란을 제공하면 각각 넣고, 단일 입력란이면 같은 순서로 합친다. 프로젝트별 실제 작업에서는 템플릿에 프로젝트명·현재 상태를 계속 덧붙이지 말고 해당 프로젝트의 현재 `AGENTS.md`와 정본을 읽는다.

ChatGPT가 현재 세션에서 GitHub, Notion, 웹, 연결 도구 등으로 필요한 evidence를 직접 확인하거나 작업할 수 있으면 실제 Tool 실행을 우선한다. 수행 가능한 일을 단순히 다른 AI에게 넘기거나 기억으로 추정하지 않는다. 반대로 filesystem/runtime/build 권위가 없는 작업은 완료했다고 주장하지 않는다.

## 7. Memory 기준

Memory는 맞춤설정을 보조하지만 프로젝트 정본은 아니다.

### 유지 가치가 높은 예

- 장기적인 개발 숙련도와 선호 설명 방식.
- 주 개발 엔진/언어처럼 오래 유지되는 기본 환경.
- 비용 정책처럼 반복적으로 영향을 주는 선호.
- 플레이어 경험을 우선하는 기획 성향.

### 프로젝트에서 다시 확인해야 하는 예

- 현재 구현 상태와 다음 작업.
- PR/Issue 상태.
- 특정 시스템 최신 수치.
- 승인 자산의 최신 버전.
- 최근 변경된 도구 정책.
- 이미 종료된 일회성 작업 결과.

현재 프로젝트 사실을 말할 때는 Memory가 아니라 프로젝트 정본을 readback한다.

## 8. Codex 및 다른 실행 도구

Codex용 bootstrap 원본은 `templates/custom-instructions.codex.md`다. 해당 템플릿도 프로젝트 `AGENTS.md`와 최신 실행 계약보다 높은 authority가 아니다.

GPT와 Codex의 책임을 영구적으로 `기획 전용` / `구현 전용`처럼 과도하게 고정하지 않는다. 현재 세션이 실제 Tool과 권위를 가지고 수행할 수 있는 범위를 먼저 보고, 별도 executor가 필요한 경우에만 handoff한다.

Codex 템플릿 자체의 상세 read-order와 stale-path 감사는 GPT 맞춤설정 변경과 독립된 변경 범위로 수행한다.

## 9. 유지보수와 drift 검수

Base의 큰 운영 구조, 기본 project surface, domain canon, 비용 정책, executor 역할이 변경될 때 다음을 확인한다.

1. `templates/custom-instructions.gpt.md`가 새 정본과 충돌하는 고정 사실을 갖고 있는가?
2. 맞춤설정에 복사된 세부 Gate 때문에 Base 변경이 이중 수정 작업이 되었는가?
3. deprecated/migration-only tool이 active/default route로 남았는가?
4. Memory나 과거 대화가 프로젝트 정본보다 높은 것처럼 표현되었는가?
5. 새 채팅이 프로젝트 이름과 현재 상태를 모르더라도 저장소/Notion의 current authority로 스스로 진입할 수 있는가?

하나라도 실패하면 프로젝트 사실을 더 추가하기보다 **bootstrap을 줄이고 current authority routing을 강화**하는 방향을 우선한다.

## 10. 파일 변경 설명 규칙

AI가 파일을 생성, 수정, 삭제, 이동, 이름 변경할 때는 변경 이유, 연결되는 문서/코드, 다른 작업자에 미치는 영향, 참조 갱신, 후속 동기화와 rollback을 확인한다. 사용자의 정상 변경을 덮어쓰거나 범위 밖 리팩터링을 하지 않는다.

## 11. 실제 지침 템플릿

- ChatGPT: `templates/custom-instructions.gpt.md`
- Codex: `templates/custom-instructions.codex.md`
- 프로젝트 최상위 작업 규칙 예시: `templates/AGENTS.project.md`
