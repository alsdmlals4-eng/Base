# Skill 실행 계획·증거 기록

## 작업

- 프로젝트:
- 요청:
- 제품 단계:
- Work Mode:
- 실행 프로필:
- 기준 Branch·Commit:

## Skill 실행 계획

| 순서 | Skill | Mode | Trigger | 사용 이유 | 예상 산출물 | 검증 방법 |
|---:|---|---|---|---|---|---|

## Skill 실행 결과

| 순서 | Skill | Mode | 상태 | 실제 입력 | 실제 산출물 | 증거 경로·빌드·Commit | 누락·차단 |
|---:|---|---|---|---|---|---|---|

상태:

- `EXECUTED_AND_EVIDENCED`
- `EXECUTED_UNVERIFIED`
- `ROUTED_NOT_NEEDED`
- `NOT_AVAILABLE`
- `BLOCKED`
- `FALLBACK_USED`

## 과잉·누락 검사

- [ ] Trigger와 무관한 Skill을 호출하지 않았다.
- [ ] 같은 책임을 여러 Skill이 중복 판정하지 않았다.
- [ ] Skill 문서를 읽은 것과 실제 실행을 구분했다.
- [ ] 실행하지 않은 도구·테스트·렌더를 PASS로 보고하지 않았다.
- [ ] Grill Me와 적대적 검토 외에 현재 Gate의 핵심 설계·구현·검증 Skill이 포함됐다.
- [ ] 관련 없는 Skill은 호출하지 않고 `ROUTED_NOT_NEEDED`로 분리했다.

## Gate별 Coverage

### Requirement Coverage

- 누락:
- 조치:

### Skill Coverage

- 누락:
- 조치:

### Artifact Coverage

- 누락:
- 조치:

## Learning Log 판정

- 기록 필요: YES / NO
- 근거:
- Learning Log 경로:
- Base 변경 제안 필요: YES / NO
