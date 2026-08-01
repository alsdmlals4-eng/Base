# BCP-2026-003 — AI 모델 라우팅·프롬프트 캐싱 비용 최적화

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base`
- 기준 커밋: `a82976a3a42450ea413cdc5d4aebf701678110d8`
- 제출일: `2026-07-31`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 지식 상태: `패턴 + 검증 필요 수치`
- 추적 Issue: `#113`

## 관찰과 증거

AI 작업은 판단 위험과 실패 비용이 서로 다르므로 모든 단계를 같은 고비용 모델로 처리할 필요가 없다. 사용자는 Luna를 단순·대량, Terra를 일상 작업, Sol을 고난도 판단에 제한적으로 사용하는 에이전트 스택과 반복 프롬프트의 안정 접두부를 캐시하는 방식을 승인했다.

커뮤니티의 `60~70% 절감`과 사용자 제공 캐시 수치는 공급자·모델·시점·재시도에 따라 달라지는 검증 전 주장이다. 공식 자료와 확인일 없이 Base 영구 상수나 보장값으로 사용하지 않는다.

## 일반화 후보

통합 전문 Skill `optimizing-ai-model-and-prompt-costs`를 추가한다.

1. `route-model-and-effort`: 난도·품질 위험·재시도 비용으로 모델과 추론 단계를 추천한다.
2. `design-cacheable-prefix`: 안정 공용 접두부와 변동 접미부를 분리한다.
3. `estimate-cost`: 입력·출력·캐시 쓰기·읽기·재시도·상위 모델 재작업 비용을 분리한다.
4. `measure-actual-usage`: 공급자 usage·청구 근거·캐시 적중을 기록한다.
5. `recalibrate`: 품질 실패와 재작업을 포함한 순비용으로 기준을 조정한다.

`[모델 추천]` 출력 계약:

```text
권장 모델:
권장 추론 단계:
선택 이유:
다음 변경 checkpoint:
변경 전 계속하면 생기는 위험:
```

실행 중인 응답이 즉시 다른 모델로 교체된다고 주장하지 않는다. 검증 가능한 checkpoint에서 사용자가 설정을 바꾼 뒤 다음 단계부터 계속한다.

## 프로젝트 전용으로 남길 내용

- 프로젝트별 실제 프롬프트 전문과 비공개 운영값
- 계정별 요금·예산·실제 청구 데이터
- 프로젝트별 모델 허용 목록·보안 등급·품질 기준
- 공급자 콘솔과 조직 설정

Base에는 공용 분류법, provider profile 형식, 측정식, 실패 조건과 검증 절차만 둔다.

## 적용 조건과 비사용 조건

### 적용

- 여러 모델·추론 단계 중 작업에 맞는 조합을 선택해야 한다.
- 반복되는 공용 문맥의 캐시 적중 가능성을 평가해야 한다.
- 비용 절감이 품질 저하와 재작업을 만들지 않는지 측정해야 한다.
- 사용자가 `[모델 추천]`을 명시했다.

### 비사용

- 모델 선택권이 없는 환경
- 한 번뿐인 짧은 요청
- 검증 책임이 비용보다 우선해 하향 사용이 금지된 고위험 작업
- 공급자의 캐시 지원·usage 필드를 확인할 수 없는 경우
- 민감하거나 변동되는 인증 정보를 안정 접두부에 포함해야만 하는 구조

## 반례와 위험

- 단순 작업에 숨은 설계 판단이 있으면 하위 모델 결과 누락과 상위 모델 재작업으로 총비용이 증가한다.
- 상위 모델이 매번 초안을 전면 재작성하면 스택 분리가 아니라 중복 실행이다.
- 캐시 적중을 위해 오래된 규칙을 유지하면 품질과 안전성이 저하된다.
- 임계값·TTL·할인율을 상수화하면 공급자 변경 뒤 잘못된 결정을 내린다.
- 커뮤니티 절감률을 보장값으로 제시하면 실제 청구와 불일치한다.
- 제품 surface에 없는 모델·추론 옵션을 추천할 수 있다.

## 영향 범위와 검증

- 신규 전문 Skill 1개와 reference 2개
- Skill Registry·Learning Log·focused test
- provider profile과 `[모델 추천]` 출력 계약
- released v9.3 증거를 보존하는 Base v9.4 후보 경계

필수 시나리오:

1. 단순 로그 요약 → Luna 계열
2. 일반 코드·문서 검토 → Terra 계열
3. 아키텍처·보안·복합 디버깅 → Sol 계열
4. 숨은 고위험 조건 → 하향 분류 거부
5. 반복 Prompt → stable prefix / dynamic suffix
6. 공급자 수치 미확인 → `UNVERIFIED_PROVIDER_PROFILE`
7. 비용 감소와 재작업 증가 → 순절감 실패
8. `[모델 추천]` 출력 계약
9. 민감 정보 포함 접두부 → 캐시 설계 거부
10. v9.4 HEAD Registry와 released v9.3 pinned evidence 동시 검증

실행하지 않은 실제 청구·캐시 적중·절감률 검증은 `NOT_RUN`으로 남긴다.

## 필요한 도구·파일·권한

- GitHub Branch·PR·Actions와 Python 검증 환경
- 검증: BCP checker, Skill coverage, reference freshness, Base integrity, 전체 Python suite, `git diff --check`
- 현재 로컬 실행 환경은 저장소 복제가 차단되어 `NOT_RUN`; GitHub Actions를 실행 증거로 사용한다.

## 승인과 구현

- 사용자 승인 근거: `https://github.com/alsdmlals4-eng/Base/issues/113`
- 제안 상태: `SUBMITTED` — 신규 제안은 제안 PR에서 이 상태로 시작한다.
- 구현 상태 전환: 제안 PR 병합 후 별도 v9.4 구현 PR에서 `APPROVED_FOR_IMPLEMENTATION`과 `approval_ref`를 기록한다.
- 구현 순서: Issue #113과 #115의 독립 책임을 하나의 v9.4 후보 구현 PR에서 별도 Task·Commit·Test로 적용한 뒤 evidence PR과 pin-finalization PR을 진행한다.
- 책임 경계: 모델 라우팅·비용·캐싱의 입력·출력·검증을 지시·컨텍스트·UI 모션 책임과 합치지 않는다.
- 제외: 프로젝트 자동 반영, 실제 모델 전환 조작, 검증되지 않은 수치 상수화, v9.3 history rewrite
- 롤백: 제안 PR을 닫거나 상태를 보존한 채 구현하지 않는다. 활성 Base 파일은 이 제안 PR에서 변경하지 않는다.

## Base v9.4 구현 연결

- approval_ref: `https://github.com/alsdmlals4-eng/Base/issues/113`
- implementation_pr: `https://github.com/alsdmlals4-eng/Base/pull/118`
- 상태 전환 위치: 제안 PR이 아니라 승인된 별도 Base v9.4 구현 PR
- BCP-2026-003과 BCP-2026-004는 같은 후보 PR을 사용하지만 Skill·Method·Reference·Test 책임을 분리한다.
