---
name: sharpening-project-domain-language-and-decisions
description: Use during an approved project interview or document review when terms are overloaded, terms conflict across sources, code contradicts stated behavior, or a hard-to-reverse decision needs concise, traceable context. Maintain only a lazy project-domain glossary and qualifying decision records; do not duplicate the eleven discipline bibles.
---

# Sharpening Project Domain Language and Decisions

## Purpose and boundary

이 스킬은 외부 `grill-with-docs`/`domain-modeling`의 질문 강화·용어 정제·드문 ADR 기록 원칙을 Base 프로젝트 구조에 맞게 적용한다. 기본 인터뷰나 본책을 대체하지 않는다.

- 요구 사실·영향 분야·사용자 확인·실행 계약은 `conducting-deep-requirement-interviews`가 책임진다.
- 방향·규칙·수치·현재 상태의 현행 원본은 프로젝트 종합 기획서와 11개 분야 본책이다.
- 이 스킬은 용어의 뜻과 되돌리기 어려운 결정의 **맥락 링크**만 유지한다. 본책 내용을 다시 쓰지 않는다.
- 일반적인 브레인스토밍, 단순 동의어, 이미 한 문서 안에서 명확한 표현에는 호출하지 않는다.

## Trigger

다음 중 하나가 확인될 때만 호출한다.

- 같은 단어가 본책·코드·UI·테스트에서 서로 다른 뜻으로 쓰인다.
- 요구 문장이 모호하거나 과도하게 넓어 구현·검증 결과가 달라질 수 있다.
- 코드의 실제 동작이 승인된 문서의 용어 또는 규칙과 충돌한다.
- 사용자 확인을 거친 선택이 되돌리기 어렵고, 맥락이 없으면 나중에 놀라울 수 있으며, 실제 대안 간 trade-off가 있다.

## Read first

1. 현재 인터뷰 기록 또는 승인된 직접 요청·Issue·Plan
2. 프로젝트 `Documentation Map`, `Active Context`, 관련 분야 본책과 실제 코드·데이터·테스트
3. 프로젝트 허브의 `DECISION_LOG.md`
4. 이미 존재한다면 `[기획서]/00_프로젝트_허브/DOMAIN_LANGUAGE.md`

## Workflow

### 1. 충돌을 증거로 분해한다

용어·규칙마다 다음을 구분한다.

- 실제로 관찰한 코드·데이터·테스트·문서 사실
- 사용자만 결정할 수 있는 의미·우선순위·trade-off
- 아직 `[미검증]`인 추정

애매한 말을 그대로 받아들이지 않는다. 경계 사례를 하나 이상 만들고, 다른 단어가 같은 개념을 가리키는지 또는 같은 단어가 다른 개념을 가리키는지 확인한다. 구현을 바꾸는 판단은 이 스킬만으로 확정하지 않고 딥인터뷰의 사용자 확인 게이트로 되돌린다.

### 2. 용어 파일은 필요할 때만 만든다

정리할 canonical 용어가 처음 생길 때만 다음 파일을 만든다.

```text
[기획서]/00_프로젝트_허브/DOMAIN_LANGUAGE.md
```

만든 뒤 `DOCUMENTATION_MAP.md`의 프로젝트 허브 책임 표에 등록한다. 용어 파일을 모든 프로젝트에 미리 설치하지 않으며, `CONTEXT.md`, 별도 root glossary, 외부 스킬의 경로를 복사하지 않는다.

각 항목은 아래 정보만 가진다.

```md
## <Canonical term>

- 정의: 1~2문장으로 현재 프로젝트에서만 유효한 뜻
- 피할 표현: 혼동되는 동의어·구버전 이름
- 책임 원본: <본책 경로 또는 문서 ID>
- 상태: 확정 / [미검증] / [확인 필요]
- 구현 증거: <선택; 실제 코드·데이터·테스트 경로>
```

용어집에는 구현 절차, 전체 규칙, 수치 표, 대안 비교를 복제하지 않는다. 그것들은 책임 본책·실제 데이터·Decision Log에 둔다.

### 3. Decision Log 기록 기준을 엄격히 적용한다

`DECISION_LOG.md`에 기록하는 것은 아래 세 조건이 모두 참일 때뿐이다.

1. 나중에 되돌리기 어렵다.
2. 기록이 없으면 새로운 작업자에게 놀라운 선택이다.
3. 실제로 선택 가능한 대안 사이의 trade-off가 있었다.

기록에는 질문, 결정, 근거, 기각한 대안과 이유, 영향 본책·파일, 재검토 조건을 채운다. 미확정 제안은 기록하지 않는다. 단순 작업 순서, 일회성 구현 메모, 아직 사용자 확인이 없는 선택은 인터뷰 기록·Active Context·`[확인 필요]`에 둔다.

### 4. 책임 원본을 갱신하고 추적성을 확인한다

- canonical 의미가 정해지면 해당 11개 본책 또는 프로젝트 종합 본책도 최소 범위로 갱신한다.
- 용어집의 책임 원본·구현 증거 링크가 실제로 열리는지 확인한다.
- 용어 변경이 UI 문자열, 데이터 키, 저장 형식, 테스트 이름에 영향을 주면 영향 범위와 호환성 검증을 인터뷰·Plan에 남긴다.
- 충돌을 해결하지 못하면 삭제·추정하지 않고 `[확인 필요]`와 재개 조건을 남긴다.

## Output contract

- 필요할 때만 만든 `DOMAIN_LANGUAGE.md`와 Documentation Map 등록
- 세 조건을 모두 통과한 결정만 담은 기존 `DECISION_LOG.md` 항목
- 갱신된 분야 본책 또는 프로젝트 종합 본책
- 실제 경로·사용자 확인·미검증 상태를 구분한 링크

## Failure conditions

- 모든 프로젝트에 빈 용어집 또는 별도 ADR 폴더를 강제로 설치함
- 용어집을 규칙·수치·명세의 두 번째 책임 원본으로 만듦
- 세 조건 중 하나라도 빠진 선택을 Decision Log에 확정 결정으로 기록함
- 코드 관찰 사실을 사용자에게 다시 묻거나, 사용자 결정을 코드 사실처럼 기록함
- 본책·실제 파일·Documentation Map의 연결을 갱신하지 않음

## Validation

- canonical 용어마다 단 하나의 현재 의미와 책임 원본이 있는가?
- 피할 표현과 실제 코드·문서 충돌을 확인했는가?
- Decision Log의 새 항목은 세 조건과 사용자 확인 근거를 모두 만족하는가?
- `DOMAIN_LANGUAGE.md`는 필요할 때만 존재하며, 등록된 링크가 모두 유효한가?
- 11개 본책의 책임을 용어집이나 Decision Log가 침범하지 않았는가?

## Provenance

- Adapted concepts: [mattpocock/skills `grill-with-docs`](https://github.com/mattpocock/skills/tree/ed37663cc5fbef691ddfecd080dff42f7e7e350d/skills/engineering/grill-with-docs) and its `domain-modeling` companion.
- Pinned source, file hashes, retained and intentionally excluded concepts: `skills/GRILL_WITH_DOCS_SOURCE_MANIFEST.json`.
