# BCP-2026-003 — AI 모델 라우팅·프롬프트 캐싱 비용 최적화

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base`
- 기준 커밋: `a82976a3a42450ea413cdc5d4aebf701678110d8`
- 제출일: `2026-07-31`
- 상태: `SUBMITTED`
- 지식 상태: `패턴 + 검증 필요 수치`
- 추적 Issue: `#113`

## 관찰과 증거

AI 협업 작업은 모든 단계를 동일한 고성능 모델로 처리할 필요가 없다. 파일 목록화·로그 요약·형식 변환처럼 대량이지만 판단 위험이 낮은 작업, 일상적인 코드·문서 분석, 아키텍처·보안·복합 디버깅처럼 실패 비용이 큰 작업은 요구되는 판단 강도가 다르다.

사용자는 Luna를 단순·대량 작업, Terra를 일상 작업, Sol을 고난도 판단에 제한적으로 사용하는 에이전트 스택과 반복 프롬프트의 공통 앞부분을 캐시하는 방식을 Base의 재사용 Skill로 승인했다. 승인 범위와 릴리스 경계는 Issue `#113`에 기록한다.

커뮤니티의 `60~70% 비용 절감` 주장은 작업 구성·재시도·품질 기준에 따라 달라지는 `ANECDOTAL_CASE`다. 사용자 제공 캐시 수치인 `1,024 tokens`, `최소 30분`, `cache write 1.25x`, `cache read 90% 할인`도 provider·모델·시점에 종속될 수 있으므로 공식 문서와 확인일 없이 Base의 영구 상수로 고정하지 않는다.

## 일반화 후보

통합 전문 Skill `optimizing-ai-model-and-prompt-costs`를 추가하고 다음 다섯 mode를 제공한다.

1. `route-model-and-effort`: 작업 난도·품질 위험·재시도 비용을 기준으로 모델과 추론 단계를 추천한다.
2. `design-cacheable-prefix`: 안정된 공용 접두부와 변동 접미부를 분리한다.
3. `estimate-cost`: 입력·출력·캐시 쓰기·읽기·재시도·상위 모델 재작업 비용을 추정한다.
4. `measure-actual-usage`: provider usage·청구 근거·캐시 적중을 기록한다.
5. `recalibrate`: 품질 실패와 재작업을 포함한 순비용으로 라우팅 기준을 조정한다.

사용자가 `[모델 추천]`이라고 말하면 현재 작업에 대해 다음을 먼저 출력한다.

```text
권장 모델:
권장 추론 단계:
선택 이유:
다음 변경 checkpoint:
변경 전 계속하면 생기는 위험:
```

작업 중 모델 변경은 실행 중인 응답이 즉시 교체된다고 주장하지 않는다. 검증 가능한 checkpoint에서 중단하고 사용자가 모델·추론 단계를 변경한 뒤 다음 단계부터 계속한다.

## 프로젝트 전용으로 남길 내용

- 프로젝트별 실제 프롬프트 전문과 비공개 규칙
- 계정별 API 키·요금제·예산·청구 데이터
- 각 프로젝트의 모델 허용 목록과 보안 등급
- 프로젝트 고유 작업 분류·성과 목표·품질 기준
- 특정 공급자 콘솔의 인증·권한·조직 설정

Base에는 공용 분류법, provider profile 형식, 측정식, 실패 조건과 검증 절차만 둔다.

## 적용 조건과 비사용 조건

### 적용 조건

- 여러 모델·추론 단계 중 작업에 맞는 조합을 선택해야 한다.
- 반복되는 시스템 규칙·도구 정의·공용 문맥이 있어 캐시 적중 가능성을 평가해야 한다.
- API/에이전트 비용을 품질 저하 없이 줄여야 한다.
- 실제 사용량과 재시도 비용을 기준으로 모델 라우팅을 재조정해야 한다.
- 사용자가 `[모델 추천]`을 명시했다.

### 비사용 조건

- 모델 선택권이 없는 단일 실행 환경이다.
- 한 번뿐인 짧은 요청으로 캐시 설계 비용이 이득보다 크다.
- 의료·법률·보안·릴리스 판단처럼 검증 책임이 비용보다 우선이며 하향 모델 사용이 허용되지 않는다.
- provider의 캐시 지원·청구 필드를 확인할 수 없다.
- 비밀·개인정보·변동 인증정보를 공통 접두부에 넣어야만 적중하는 구조다.

## 반례와 위험

- Luna로 분류한 작업에 숨은 설계 판단이 포함되면 결과 누락과 Sol 재작업으로 총비용이 증가할 수 있다.
- Terra 초안을 Sol이 매번 전면 재작성하면 스택 분리가 아니라 중복 실행이다.
- 긴 공통 접두부를 유지하려고 stale 규칙을 반복하면 캐시 적중률은 높아져도 결과 품질과 안전성이 저하된다.
- 캐시 임계값·TTL·할인율을 상수화하면 provider 변경 뒤 잘못된 비용 결정을 내릴 수 있다.
- 캐시된 텍스트에 비밀·개인정보가 포함되면 보안·데이터 거버넌스 위험이 생긴다.
- 커뮤니티 절감률을 보장값으로 제시하면 실제 청구와 불일치한다.
- 모델명·가용 추론 단계가 제품 surface마다 다를 수 있으므로 존재하지 않는 옵션을 추천할 수 있다.

## 영향 범위와 검증

### 예상 영향

- 신규 전문 Skill 1개와 reference 2개
- Skill Registry·Learning Log·focused test
- 모델 추천 출력 계약과 provider profile 계약
- v9.3 릴리스 증거를 보존하면서 신규 Registry를 소유할 v9.4 후보 릴리스 경계

### 검증 시나리오

1. 단순 로그 요약 → Luna 계열 + 낮은/중간 추론 권장
2. 일반 문서·코드 리뷰 → Terra 계열 + 중간 추론 권장
3. 아키텍처·보안·복합 디버깅 → Sol 계열 + 높은 추론 권장
4. 숨은 고위험 조건이 있는 대량 작업 → 단순 분류를 거부하고 상향 또는 분할
5. 반복 프롬프트 → stable prefix / dynamic suffix 분리
6. provider 수치 미확인 → 값 추정 금지, `UNVERIFIED_PROVIDER_PROFILE`
7. 실제 비용 감소지만 재작업 증가 → 순절감 실패 판정
8. `[모델 추천]` → 권장 모델·추론 단계·이유·checkpoint 출력
9. 비밀 포함 접두부 → 캐시 설계 거부
10. v9.4 후보가 HEAD Registry를 검증하고 released v9.3은 pinned evidence로 검증

실행하지 않은 실제 API 청구·캐시 적중·절감률 검증은 `NOT_RUN`으로 남긴다.

## 필요한 도구·파일·권한

- 필요 항목: Base 저장소 쓰기 권한, GitHub Issue/branch/PR, Python test 실행 환경, provider 공식 문서 조회
- 필요한 이유: BCP와 구현 PR 분리, Registry·release evidence 무결성, 변동 수치 검증
- 설치·적용 방법: Issue `#113`의 단계에 따라 BCP PR → v9.4 candidate PR → evidence PR → pin-finalization PR 순으로 진행
- 설치 후 확인 명령:
  - `python tools/check_base_change_proposals.py --base-ref origin/main`
  - `python tools/check_skill_system_coverage.py`
  - `python tools/check_canonical_reference_freshness.py`
  - `python tools/check_base_v9_integrity.py`
  - `python -m unittest discover -s tests -p 'test_*.py'`
  - `git diff --check`
- 최소 권한: Base repository contents·issues·pull requests 쓰기. Release publish·project repository·Google Sheets 권한은 불필요

## 승인과 구현

- 사용자 승인 근거: Issue `#113`에 2026-07-31 승인 발화와 승인 구조를 기록함. 신규 제안은 검증기 계약에 따라 이 PR에서 `SUBMITTED`로 시작하며, 제안 PR 병합 뒤 구현 branch에서 `APPROVED_FOR_IMPLEMENTATION`으로 전환한다.
- 구현 PR: `없음 — 제안 PR과 분리 예정`
- 구현 범위: Issue `#113`의 In scope와 acceptance criteria
- 제외 범위: 프로젝트 자동 반영, 실제 모델 전환 조작, 검증되지 않은 비용 수치 상수화, v9.3 history rewrite
- 롤백: 제안 PR을 닫거나 BCP를 `DEFERRED`/`REJECTED`로 보존한다. 활성 Base 파일은 이 제안 PR에서 변경하지 않는다.
