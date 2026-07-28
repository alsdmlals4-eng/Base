# Vertical Slice v6 요구사항의 Base 책임 매핑

## 목적

`VERTICAL_SLICE_MASTER_REFERENCE_v6`의 내용을 대형 중복 정본으로 Base에 복사하지 않고, 최신 Base의 Registry route·통합 Skill·지식 reference·Template·Test 구조에 무손실로 배치한다.

## 통합 원칙

- 사용자 최신 지시가 최상위다.
- Base 공용 Skill 본문은 프로젝트에 복제하지 않는다.
- 새 Skill은 기존 Base에 같은 책임이 없을 때만 만든다.
- 이번 변경은 새 Skill·Trigger·Registry 항목을 추가하지 않는다.
- 기존 `designing-vertical-slices` Skill의 책임·mode·Registry 계약은 보존하고, 기존 Skill이 참조하는 `VERTICAL_SLICE_PLAN.md`에서 상세 지식 계약으로 라우팅한다.
- Grill Me·적대적 검토·자산 조사·문서·검증·인수인계는 기존 전문 Skill에 위임한다.
- 전체 v6 본문은 참고 증거이며 Base의 활성 실행 책임은 기존 Skill·지식 reference·확장 Template다.

## Requirement Coverage

| v6 책임 | Base 책임 원본 | 변경 |
|---|---|---|
| 4단계 제품 Gate | `docs/knowledge/vertical-slice/INTEGRATED_DEMO_STAGE_GATES.md` | 신규 지식 reference |
| 과거 `CORE_POC`·`SLICE_VALIDATION` | concept Skill + Gate reference | 최신 사용자 결정으로 별도 Core PoC Gate를 제거하고 내부 `TECHNICAL_SPIKE`·`DEMO_VALIDATION` 호환 해석으로 변경 |
| 프로토타입에서 멈추지 않는 Stage 2 | Gate reference·Vertical Slice Template | 연속 Gate·완료 기준 추가 |
| PC Steam·STOVE·itch.io 패키지 | Gate reference·Vertical Slice Template | 신규 상세 계약 |
| 모바일 Google Play 패키지 | Gate reference·Vertical Slice Template | 신규 상세 계약 |
| Steam 출시 예정 페이지·트레일러·스크린샷 | Gate reference·Template 추적표 | Slice 추적성 추가 |
| STOVE 피드백·핵심 재미 시작점 | Gate reference | 외부 검증 항목 추가 |
| Steam Playtest | 기존 Vertical Slice Skill·Gate reference | 기존 표본·빌드 계약에 플랫폼 항목 추가 |
| 텀블벅 준비도 | Gate reference | 팬덤·리워드·남은 범위 계약 추가 |
| 세부 수치 유예 | `docs/knowledge/vertical-slice/ASSET_MASCOT_AND_TUNING.md`·Template | 상태·Backlog 추가 |
| UI·UX·사운드 콘셉트 우선 | Asset·Mascot reference | 상세 역할 계약 추가 |
| 에셋스토어 우선·없는 경우 생성 | 기존 Godot asset Skill + Asset·Mascot reference | 라우팅 연결 |
| 세계관 마스코트 | Asset·Mascot reference | 역할·제한·Slice 증거 추가 |
| Grill Me 0~3 | `docs/knowledge/vertical-slice/SKILL_ORCHESTRATION_AND_EVIDENCE.md` | 기존 clarify의 조건부 단계 복원 |
| 적대적 검토 5개 렌즈 | Skill orchestration reference + 기존 review Skill | 렌즈와 Finding 라우팅 연결 |
| 많은 Skill의 적절한 사용 | Skill orchestration reference | 단계별 최소 충분 Skill 체인 추가 |
| Superpowers 개발 체인 | Skill orchestration reference | 설치·Trigger 조건부 연결 |
| DeepSeek·외부 AI 격리 | Skill orchestration reference | external-source-review 연결 |
| P0~P3 | Skill orchestration reference·Template | 우선순위 복원 |
| HiGodot 조건부 구조 검증 | Skill orchestration reference | 실제 연결·도구 확인 조건 |
| GitHub·PDF 발행 | Skill orchestration reference | 조건부 프로필로 복원 |
| Skill 실행 증거 | `SKILL_EXECUTION_EVIDENCE.md` | 신규 Template |
| Requirement·Skill·Artifact 완전성 | 지식 reference·Template·test | 3중 감사 추가 |

## 2026-07-28 최신 사용자 결정

- 별도 `CORE_POC` 제품 단계는 사용하지 않는다.
- 첫 통합 플레이 제품은 완성 품질의 `DEMO_FIRST_VERTICAL_SLICE`다.
- 기술 불확실성은 Slice 내부의 제한된 `TECHNICAL_SPIKE`로만 검증한다.
- 과거 v6의 `CORE_POC`·`PROTOTYPE_AND_VERTICAL_SLICE`·`SLICE_VALIDATION` 표기는 각각 내부 Spike·`DEMO_FIRST_VERTICAL_SLICE`·`DEMO_VALIDATION`의 역사·호환 용어다.

## 기존 책임 보존

다음 기존 계약을 제거하거나 재정의하지 않는다.

- Prototype / Vertical Slice / MVP / Demo 구분
- `slice-contract / quality-bar / pipeline-proof / playtest-evidence / decision-gate`
- 접근성·성능 전문 검증 위임
- 선택적 하이라이트의 보유·미보유 정상 완주 사례
- 실제 빌드·표본·행동·자기보고 분리
- 제작 파이프라인의 두 번째 콘텐츠 반복 증명
- `EXPAND / REWORK / REPEAT_SLICE / HOLD / STOP` 판정
- `skills/SKILL_REGISTRY.json`의 단일 `designing-vertical-slices` 항목

## 비채택·변형

- v6 전체를 하나의 활성 Base 문서로 복제하지 않는다. 통합 Skill 구조와 중복 정본을 만들기 때문이다.
- 모든 Skill을 한 번에 로드하지 않는다. 하위 작업별 최소 충분 Skill을 순차 오케스트레이션한다.
- 고정 횟수의 적대적 검토 대신 5개 독립 렌즈를 Gate 위험에 맞춰 적용한다.
- 모든 작업에서 PDF·HiGodot·DeepSeek를 강제하지 않는다. Trigger·도구·발행 정책이 맞을 때만 실행한다.
- 세부 수치 조정은 기획 승인 질문이 아니라 플레이테스트 Backlog로 관리한다.
- 기존 Skill 본문을 바꾸지 않아 Registry·Learning Log companion 계약을 불필요하게 흔들지 않는다.
- 상세 계약을 Skill 패키지 내부의 미연결 reference로 두지 않고, 기존 Skill이 참조하는 Template에서 지식 문서로 라우팅한다.

## 검증

- `tests/test_vertical_slice_v6_contract.py`
- 기존 `tests/test_consolidated_skill_references.py`
- Skill Registry·package integrity·reference freshness·documentation routing CI
- PR Actions의 정적 검증 결과
