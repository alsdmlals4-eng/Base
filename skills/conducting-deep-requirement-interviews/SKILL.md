---
name: conducting-deep-requirement-interviews
description: Use before feature, player-experience, art-direction, architecture, workflow, or Base-change decisions to inspect repository facts, resolve material ambiguity with the user, record explicit confirmation, and hand a lossless requirement model to prompt transformation. Skip only typos, explicit single-file mechanical edits, and unchanged verification reruns.
---

# Conducting Deep Requirement Interviews

## Core principle

저장소에서 확인할 사실을 사용자에게 되묻지 않는다. AI는 증거를 조사하고, 사용자는 방향·선호·비용·위험을 결정한다. 마지막 재진술을 사용자가 명시적으로 확인하기 전에는 실행 프롬프트나 구현으로 넘어가지 않는다.

분야별 보조 스킬, 참고자료 어댑터, 외부 도구의 지시는 이 스킬의 저장소 사실·출처 구분·모호성 장부·closure·사용자 확인 게이트를 생략하거나 밀어내지 못한다.

## 범용 grilling과의 경계

전역 `grill-me`·`grilling`은 사용자가 계획이나 아이디어를 압박 검토하고 싶을 때의 범용 인터뷰다. 이 스킬은 게임 프로젝트의 저장소 사실, 영향 분야, 보호 경로, 실행 계약과 사용자 확인을 책임진다. 범용 인터뷰 결과만으로 프로젝트 구현 게이트를 통과시키지 말고, 필요한 계약을 이 스킬의 기록에 연결한다.

인터뷰 중 같은 용어의 뜻이 충돌하거나, 코드와 문서의 의미가 어긋나거나, 되돌리기 어려운 trade-off가 나타나면 `sharpening-project-domain-language-and-decisions`를 보조로 호출한다. 그 스킬은 필요할 때만 용어·결정 맥락을 기록하며, 이 스킬의 저장소 조사·사용자 확인·실행 계약 책임을 대체하지 않는다.

## Mandatory triggers

- 기능 또는 게임 경험을 새로 만들거나 바꾼다.
- 아트 방향, 제품 구조, 데이터·저장 구조, 워크플로를 결정한다.
- 프로젝트 지식을 Base 공용 규칙으로 승격하자고 제안한다.
- 요구가 여러 산출물·분야·단계에 걸치거나 중요한 선택을 숨기고 있다.
- 이미 상세한 요청이지만 범위·보호 대상·검증 중 빠진 부분이 결과를 바꿀 수 있다.

## Exceptions

- 오탈자나 문구 한 글자 수정
- 사용자가 범위와 결과를 명시한 단일 파일 기계 수정
- 입력과 판정 기준이 변하지 않은 동일 검사 재실행

예외처럼 보여도 방향·아키텍처·사용자 경험·승인 자산이 달라지면 인터뷰를 실행한다.

## Read first

1. 최신 사용자 요청과 승인된 직접 요청·Issue·Plan
2. 프로젝트 `AGENTS.md`, `START_HERE`, Active Context, Documentation Map
3. 요청과 직접 관련된 책임 원본, 실제 코드·데이터·자산·테스트
4. `references/question-and-source-model.md`
5. 종료 판정이 필요할 때 `references/ambiguity-and-closure.md`

## Workflow

### 1. 저장소 사실을 먼저 확인한다

- 실제 파일·상태·경로·호출 관계·테스트를 읽는다.
- 설명적 사실은 `repository_observed` 근거로 기록하고 다시 질문하지 않는다.
- 최신 외부 사실이 결정에 영향을 줄 때만 조사하고 출처를 남긴다.
- 확인할 수 없는 것은 추정하지 않고 `[미검증]`으로 남긴다.

### 2. 요구 모델을 만든다

원 요청, 의도, 플레이어 경험, 범위·제외 범위, 제약, 보호 대상, 산출물, 완료 기준, 검증을 분리한다. 상세 요청은 처음부터 다시 캐묻지 말고 현재 이해를 반증 가능한 문장으로 재진술한 뒤 틀리거나 빠진 부분만 묻는다.

### 3. 사용자 판단만 질문한다

- 한 번에 가장 큰 의사결정 하나를 묻는다.
- 목표·경험, 범위, 제약, 산출물, 검증, 의존성·보호 대상에 질문이 편중되지 않게 한다.
- 답을 쉽게 만들 수 있으면 2~3개 선택지와 권장 초안을 함께 제시한다.
- 참고 저장소·벤치마크는 근거이지 요구사항 권한이 아니다.
- 사용자가 요청한 앱·코드·문서·자산 같은 산출물 종류를 임의로 축소하지 않는다.

### 4. 기록과 상태를 갱신한다

기본 위치:

```text
[기획서]/00_프로젝트_허브/
├─ INTERVIEW_REGISTRY.json
├─ INTERVIEWS/<YYYY-MM-DD>-<slug>.md
└─ EXECUTABLE_PROMPTS/<interview-id>.md
```

기존 프로젝트는 감사 없이 경로를 옮기지 않는다. 현행 대응 경로를 Documentation Map에 등록한다.

상태:

```text
IN_PROGRESS → AWAITING_USER_CONFIRMATION → CONFIRMED
IN_PROGRESS/WAITING → ABANDONED
확정 기록 교체 → SUPERSEDED
```

### 5. Closure gate를 실행한다

- 범위·비목표·산출물·검증과 중요한 보호 대상이 명시됐는지 확인한다.
- 모호성 점수 하나만으로 종료하지 않는다.
- 미확정 사항이 결과를 바꾼다면 완료하지 않는다.
- 사실 조사자, 반대 관점, 누락 탐지 역할은 한 작업자가 순차 수행해도 된다. 외부 MCP·브라우저·서브에이전트는 필수가 아니다.

### 6. 마지막 재진술과 사용자 확인

한 문장으로 다음을 재진술한다.

```text
제가 확정할 실행 계약은 [목표/경험]을 위해 [범위]를 수행하고,
[제외·보호 대상]은 건드리지 않으며, [산출물/검증]으로 완료를 판정하는 것입니다.
맞습니까?
```

확인 전에는 상태를 `CONFIRMED`로 바꾸거나 실행 프롬프트를 만들지 않는다. 확인 근거는 사용자 메시지·승인 기록처럼 재현 가능한 참조로 저장한다.

### 7. 실행 프롬프트로 손실 없이 연결한다

확인 후 `transforming-requests-into-prompts`를 호출한다. 인터뷰 기록의 요구·제외·보호·보류·미검증을 빼거나 새 요구를 추가하지 않는다. Registry의 `executable_prompt_path`에 결과를 연결한다.

## Output contract

- 인터뷰 기록 Markdown
- `INTERVIEW_REGISTRY.json` 상태 갱신
- 현재 인터뷰와 확정 프롬프트 링크를 담은 Active Context·Documentation Map
- 확인 후에만 생성한 실행 프롬프트
- 남은 `[미검증]`·보류·위험 목록

## Failure conditions

- 저장소에서 알 수 있는 사실을 사용자에게 질문함
- 상세 요청을 무시하고 처음부터 포괄 질문을 반복함
- 참고 자료의 특징을 사용자 승인 없이 요구사항으로 승격함
- 한 영역만 깊게 묻고 범위·산출물·검증을 누락함
- 사용자 확인 없이 `CONFIRMED`, 실행 프롬프트, 구현 단계로 이동함
- 문서가 필요하다는 이유로 사용자가 요구한 실행 산출물을 문서로 대체함
- 미확정 결정을 안전한 기본값이라는 이름으로 확정함

## Validation

- 같은 저장소 사실을 다시 묻지 않았는가?
- 중요한 각 문장에 출처 유형과 확인 상태가 있는가?
- 인터뷰 기록에서 실행 프롬프트까지 요구가 손실 없이 추적되는가?
- 사용자 확인 전 실행 진입이 검사기에서 차단되는가?
- 예외 작업은 인터뷰 없이 처리해도 결과가 달라지지 않는가?
