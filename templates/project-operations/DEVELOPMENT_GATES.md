# [프로젝트명] 개발 게이트

- 책임: 프로젝트 허브·프로덕션·통합검수
- 마지막 검토일:
- 기준 커밋:
- 현재 제품 단계:
- 다음 Greenlight:

> 게이트는 체크리스트 작성 여부가 아니라 관찰 가능한 결과와 증거로 통과한다. 실행하지 않은 검증은 `[미검증]`으로 표시한다.

## 1. 작업 실행 게이트

### 1.1 Intake·Context Gate

- [ ] 최신 사용자 지시를 확인했다.
- [ ] 프로젝트 AGENTS·START_HERE·Documentation Map을 확인했다.
- [ ] 관련 분야 본책과 프로젝트 스킬을 확인했다.
- [ ] 실제 코드·데이터·자산·테스트를 확인했다.
- [ ] `[백업]`, `[보류]`, `[미검증]`의 관련 정보를 확인했다.

```yaml
problem:
user_or_player_value:
primary_discipline:
affected_disciplines:
change_type:
current_truth_sources:
protected_decisions_and_paths:
unknowns:
```

### 1.2 Definition of Ready

- [ ] 목적과 플레이어·사용자 가치가 명확하다.
- [ ] 포함·제외 범위가 분리됐다.
- [ ] 선행 조건과 의존성이 해결됐거나 표시됐다.
- [ ] 책임 원본과 영향 분야가 지정됐다.
- [ ] 기존 동작·저장·인터페이스·승인 자산 보호 범위를 확인했다.
- [ ] 저장·호환성·이관 위험을 기록했다.
- [ ] 완료 기준이 `조건 → 행동 → 관찰 결과`다.
- [ ] 자동·수동·사용자 검수 방법이 있다.
- [ ] Base 공용 스킬과 프로젝트 스킬을 연결했다.
- [ ] 보류 재개가 필요한 경우 승인이 있다.

Ready 판정: `통과 / 실패 / 확인 필요`

### 1.3 Planning·Approval Gate

| 항목 | 내용 | 상태·증거 |
|---|---|---|
| 현재 구조 조사 |  |  |
| 변경 파일 |  |  |
| 보호 파일 |  |  |
| 데이터·상태 소유 |  |  |
| 이미지·사운드·UI 영향 |  |  |
| 마이그레이션·호환성 |  |  |
| 실패·폴백 |  |  |
| Acceptance Criteria |  |  |
| 검증 계획 |  |  |
| 문서·스킬·Manifest 갱신 |  |  |
| 롤백 |  |  |
| 구현 승인 |  |  |

### 1.4 Implementation Gate

- [ ] 승인 Plan 범위만 변경했다.
- [ ] 기능 추가와 대규모 리팩터링을 분리했다.
- [ ] 기존 데이터·인터페이스·사용자 흐름을 보호했다.
- [ ] 보류 항목을 승인 없이 구현하지 않았다.
- [ ] 기존 승인 이미지의 임의 대체 시안을 만들지 않았다.
- [ ] 가장 작은 검증 가능한 변경 단위를 사용했다.

### 1.5 Verification Gate

| 순서 | 검증 | 명령·방법 | 결과 | 증거 | 미검증 이유 |
|---:|---|---|---|---|---|
| 1 | 포맷·문법·정적 검사 |  |  |  |  |
| 2 | 자동 테스트 |  |  |  |  |
| 3 | 핵심 정상 경로 |  |  |  |  |
| 4 | 실패·취소·중복·누락 |  |  |  |  |
| 5 | 저장·호환성 |  |  |  |  |
| 6 | 실제 화면·플레이·오디오·성능 |  |  |  |  |
| 7 | diff·승인 범위 |  |  |  |  |
| 8 | 사용자 수동 검수 |  |  |  |  |

### 1.6 Documentation Gate

- [ ] 관련 분야 본책
- [ ] Roadmap·제품 게이트
- [ ] Documentation Map
- [ ] Active Context·Handoff
- [ ] Decision Log·Changelog
- [ ] 프로젝트 스킬·Learning Log
- [ ] Visual Source·Asset Manifest
- [ ] 테스트 문서
- [ ] PDF·Publication Manifest
- [ ] README·Issue·Goal·Plan
- [ ] Base version·후속 동기화

### 1.7 Integration·Completion Gate

- [ ] 승인 범위가 실제 파일에 반영됐다.
- [ ] Acceptance Criteria를 증거로 판정했다.
- [ ] 자동·수동 검증 결과가 있다.
- [ ] 본책·상태·Manifest·PDF가 최신이다.
- [ ] 미검증·불일치·위험을 분리했다.
- [ ] 이동·제거 파일의 잔여 참조가 없다.
- [ ] 새 작업자가 결과와 다음 작업을 찾을 수 있다.
- [ ] PR 필수 검사·리뷰가 통과했다.
- [ ] 프로젝트 교훈과 Base 환류 후보를 분리했다.

완료 판정:

```yaml
implementation: complete/partial/not_started
verification: complete/partial/not_run
user_review: approved/pending/not_required
documentation: current/stale/partial
final_status:
```

## 2. 제품 마일스톤 게이트

| 단계 | 목표 | 진입 조건 | 종료 기준 | Quality Bar | 증거 | 상태 |
|---|---|---|---|---|---|---|
| Concept | 게임 약속과 대상 플레이어 |  |  |  |  |  |
| Prototype | 재미·조작·기술 가설 |  |  |  |  |  |
| Graybox | 공간·규칙·동선 |  |  |  |  |  |
| First Playable | 핵심 루프 완주 |  |  |  |  |  |
| Vertical Slice | 목표 품질·파이프라인 |  |  |  |  |  |
| Production | 본격 제작 Greenlight |  |  |  |  |  |
| Alpha | 주요 기능·전체 진행 연결 |  |  |  |  |  |
| Feature Complete | 주요 기능 완료 |  |  |  |  |  |
| Content Complete | 출시 콘텐츠 완료 |  |  |  |  |  |
| Beta | 품질·밸런스·최적화 |  |  |  |  |  |
| Release Candidate | 출시 후보 |  |  |  |  |  |

## 3. 현재 게이트 기록

```md
## [게이트명]
- 대상:
- 진입 조건:
- 종료 기준:
- Quality Bar:
- 필수 증거:
- 통과:
- 실패:
- 미검증:
- 승인자:
- 승인일·기준 커밋:
- 다음 단계:
- 남은 위험:
```

## 4. Content Lock·Code Freeze

- Content Lock 예정·적용 조건:
- Code Freeze 예정·적용 조건:
- 허용 예외:
- 예외 승인자:
- 현재 상태:
