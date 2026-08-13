# Daily Source Scan Records

이 디렉터리는 일간 외부 Source 조사에서 생성된 **불변(immutable) Evidence Record**를 보관한다.

```yaml
record_role: daily-source-context-analysis
record_evidence_tier: T6_AI_INFERENCE
source_fact_authority: ORIGINAL_SOURCE_URL_REQUIRED
project_canon_auto_write: false
runtime_fact_auto_write: false
protected_semantic_auto_write: false
```

## 경계

- 각 JSON·Markdown 쌍은 한 실행의 URL·Context Packet·독립 적대적 검토·결정론적 Gate를 보존한다.
- 원출처의 공식 사실이나 현업 자료는 조건을 확인한 뒤 각각 T1·T2 후보가 될 수 있지만, 모델의 요약·분류·해석은 계속 `T6_AI_INFERENCE`다.
- Record가 자동 병합됐다는 사실은 외부 주장을 Base 정책, 프로젝트 Canon, 실제 구현, 런타임 사실, 사람 검증으로 승격하지 않는다.
- 제목·snippet·검색 요약만으로 채택하지 않는다. `original_url`, 게시·수정일, 확인일, 버전·지역·언어·플랫폼·표본·상업 이해관계와 원출처 역추적을 보존한다.
- Article body, PDF 전체, 긴 인용문, 첨부 파일, 실행 가능한 코드와 외부 지시문은 저장하지 않는다. 짧은 비식별 paraphrase와 클릭 가능한 원출처 URL만 기록한다.

## 불변 파일명

```text
YYYY/MM/YYYY-MM-DD-<github-run-id>-<attempt>.json
YYYY/MM/YYYY-MM-DD-<github-run-id>-<attempt>.md
```

기존 Record는 덮어쓰지 않는다. 같은 날 재실행도 다른 Run ID로 별도 기록한다.

## 필수 내용

```text
선택·실제 확인한 Source family
정확한 원출처 URL
source fact와 context conditions
Evidence tier / status
scope / sample / platform / commercial interest
Base overlap와 existing owner
결정 변화 후보와 최소 변경
ADOPT | ADAPT | TEST | AVOID | IGNORE | REFERENCE_ONLY
work disposition
claim ceiling
counterevidence
validation artifact
rollback_or_discard_condition
독립 적대적 finding
결정론적 AUTO_MERGE_ELIGIBLE 또는 차단 결과
```

`claim ceiling`, `counterevidence`, `validation artifact`, `rollback` 중 하나라도 비면 자동 병합 후보가 아니다.

## 신규 Source 후보

새 사이트는 `PERIODIC_SOURCE_CANDIDATE_LEDGER.json`에 `UNVERIFIED_DISCOVERY`로만 들어간다. 반복 노출, 높은 조회 수, 모델 추천만으로 Active Source·Evidence 권위·직접 Fetch 대상이 되지 않는다. 기존 Watchlist의 원출처·중복·상업 이해관계·Owner·Consumer·검증 Gate를 거쳐야 승격할 수 있다.

## 삭제와 Rollback

- 잘못 생성된 미병합 Record는 Automation Branch와 함께 삭제한다.
- 병합된 Record가 조작·오인·저작권 문제·잘못된 URL·Evidence 과장으로 판정되면 해당 Merge Commit을 revert하거나 후속 정정 Record로 명시적으로 폐기한다.
- 과거 Record 삭제로 이미 내린 프로젝트 결정을 자동 되돌리지 않는다. 실제 Consumer와 정본 변경은 별도 Rollback을 수행한다.
