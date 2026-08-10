# 프로젝트 변경 검증

공용 기본 실행·Handoff 기준: `docs/ONE_CLICK_PLAY_HANDOFF_POLICY.md`

## 1. 판정

- 결과: `ACCEPT / ACCEPT_WITH_FOLLOWUP / REVISE / REJECT / UNVERIFIED`
- 기준 브랜치·커밋:
- 변경 주체:
- 검증 환경:

## 2. 승인된 목표·범위와 실제 diff

- 해결할 문제:
- 포함 범위:
- 제외·보호 범위:
- 실제 변경 파일:
- 범위 밖 변경:

## 3. 확인한 책임 원본·파일

| 책임 | 원본·파일 | 확인 결과 |
|---|---|---|
| | | |

## 4. 정적 검사

| 영역 | 검사 | 결과 | 증거 |
|---|---|---|---|
| 코드 | | | |
| 데이터·Schema | | | |
| 문서·참조 | | | |
| 자산·구성 | | | |

## 4.1 가설·요소·다관점 검토

```yaml
hypothesis:
minimum_test_unit:
observation_method:
success_threshold:
failure_threshold:
evidence_decision: KEEP / REVISE / REDUCE / REMOVE / RETEST
```

| 요소 | element_purpose | 입력·출력 | integration_interface | 개별 결과 | 통합 결과 |
|---|---|---|---|---|---|
| | | | | | |

| Lens | APPLIED / NOT_APPLICABLE / BLOCKED_UNVERIFIED | Finding·제외 이유 | 증거 |
|---|---|---|---|
| Simplify | | | |
| Style Guide | | | |
| Domain Review | | | |
| Security/Safety/Trust Boundary | | | |

## 5. 런타임·렌더·빌드 검증

사용자의 기본 실행 시작점에서 먼저 재현한다. 대표 Vertical Slice·Demo 인계는 별도 Scene 선택·편집기 수동 설정 없이 `Project Play`만으로 기대 첫 화면과 실제 gameplay surface에 진입해야 한다.

| 시작점·환경 | 실행 절차 | 기대 결과 | 실제 결과 | 판정 |
|---|---|---|---|---|
| 기본 Project Play | 프로젝트 열기 → Project Play | 기대 첫 화면 → 실제 플레이 → 성공·실패·복귀 | | `PASS / FAIL · RETEST_REQUIRED / NOT_RUN / BLOCKED` |
| | | | | |

- 기본 entrypoint 자동 boot 테스트:
- gameplay HUD·도구·입력 visible/enabled 테스트:
- 성공·실패·재시도·수정·복귀 테스트:
- 플랫폼·validation 전용 entrypoint 회귀:
- 실제 화면·음향·물리 입력 검수:

패키징·export·해시·headless PASS만으로 실제 런타임 PASS를 주장하지 않는다. 사용자가 화면 누락이나 조작 불가를 확인하면 판정은 `FAIL · RETEST_REQUIRED`다.

### 5.1 플레이어 경험 증거 단계와 claim ceiling

| evidence layer | 현재 상태 | 근거·실행 조건 | 이 상태만으로 말할 수 없는 것 |
|---|---|---|---|
| `TECH_EVIDENCE` | PASS / FAIL / NOT_RUN | 코드·데이터·Schema·엔진 실행 | 사용성·재미·몰입 |
| `UI_EVIDENCE` | PASS / FAIL / NOT_RUN | 렌더·입력·포커스·해상도 | 신규 플레이어 이해·기억 |
| `HUMAN_USABILITY_EVIDENCE` | PASS / FAIL / NOT_RUN | 처음 보는 사람의 조작·정보·다음 행동 관찰 | 의도한 감정·보상·기억 |
| `PLAYER_EXPERIENCE_EVIDENCE` | PASS / FAIL / NOT_RUN | 고민·선택·결과·다음 시도 의도의 실제 관찰 | 유지율·판매·장기 시장성 |

- 앞 단계의 `PASS`는 뒤 단계의 `PASS`를 의미하지 않는다.
- 사람 테스트가 실행되지 않았으면 두 사람 증거 상태를 `NOT_RUN`으로 유지한다.
- 작은 내부 테스트도 테스터 조건, 과제·질문, 행동·답변, 표본 한계를 증거에 남긴다.

## 6. Golden Path·Edge·반례·Regression

| 유형 | 시나리오 | 결과 | 증거 |
|---|---|---|---|
| Golden Path | | | |
| Edge | | | |
| 원래 실패 반례 | | | |
| Regression | | | |
| 복구·롤백 | | | |

## 7. 외부 산출물 독립 검수

- 외부 주장:
- 실제 확인 결과:
- 승인 가능:
- 수정 필요:
- 폐기:

## 8. 실패·미실행·남은 위험

- 실패한 검사:
- 실행하지 못한 검사와 이유:
- 남은 위험:
- 차단 여부:

## 9. 필요한 최소 수정

1.
2.
3.

## 10. 롤백·복구

- 롤백 기준:
- 복구 절차:
- 보존해야 할 상태:

## 11. 증거

- 실행 명령:
- 로그·리포트:
- 캡처·렌더:
- 관련 Issue·PR:

## 12. 회고·재사용 경계

- Base 공용 후보:
- 프로젝트 전용:
- 승격하지 않음:
- 반복 검증이 필요한 조건:
