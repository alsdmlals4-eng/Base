# 변경 요약

- 목표:
- 사용자·플레이어 가치:
- 프로젝트·작업 모드:
- 주 책임 분야:
- 영향 분야:
- 변경 유형:
- 관련 Issue·Plan:
- 기준 Base·프로젝트 커밋:
- 루트 `[기획서]` 경로:

## 범위·보호

- 포함:
- 제외:
- 보호한 결정·동작·데이터·자산·경로:
- `[보류]` 재개 승인:
- 롤백 방법:

## 작업 실행 게이트

- [ ] Intake·Context — 두 Registry·관련 JSON·실제 파일·보호 범위 확인
- [ ] Definition of Ready — 목적·범위·의존성·완료 기준·검증·최소 스킬 확인
- [ ] Planning·Approval — 실제 저장소 기반 Plan과 사용자 승인
- [ ] Implementation — 승인 범위·최소 변경·기존 동작 보호
- [ ] Verification — 자동·수동·실제 경로 검증
- [ ] Documentation·Publication — JSON·Registry·Skill·DOCX/PDF·Manifest 갱신
- [ ] Integration·Completion — 증거·리뷰·콜드 스타트·다음 작업

현재 제품 단계:

다음 Greenlight 영향:

## 상태 판정

| 구분 | 상태 | 증거·경로 |
|---|---|---|
| 기획·방향 승인 |  |  |
| 실제 구현·제작 |  |  |
| 자동 검증 |  |  |
| 수동·실제 플레이 |  |  |
| 시각·오디오·성능 |  |  |
| 사용자 확인 |  |  |
| 미검증·불일치 |  |  |

## Design Document Registry·JSON 본책

- [ ] 활성 `[기획서]`가 저장소 루트에 있음
- [ ] 중첩 현행 기획서 폴더 없음
- [ ] `DESIGN_DOCUMENT_REGISTRY.json` 갱신
- [ ] 주 책임·영향 분야 JSON 갱신
- [ ] 프로젝트 전체와 분야 책임 범위 누락 없음
- [ ] 확정·구현·검증·확인 필요·보류 상태 일치
- [ ] 실제 코드·데이터·자산·테스트 경로 연결
- [ ] 활성 `*_기획서.md`, `DISCIPLINE_BIBLE.md`, `PROJECT_MASTER_PLAN.md`를 만들지 않음

| 문서 ID | 책임 범위 | JSON | 변경 이유 | 실제 증거 |
|---|---|---|---|---|
|  |  |  |  |  |

## 사람용 DOCX/PDF·다이어그램·승인 이미지

- [ ] 영향 없음
- [ ] JSON 변경 시 DOCX·PDF 재생성
- [ ] workflow·status·responsibility 다이어그램 생성
- [ ] 승인 이미지·실제 캡처와 상태 캡션 포함
- [ ] JSON·생성기·출력·자산 SHA-256 Manifest 갱신
- [ ] DOCX 유효성·PDF 헤더 확인
- [ ] PDF 전 페이지 렌더·빈 페이지 검사
- [ ] 한글·표·이미지 잘림·겹침 시각 검수
- [ ] DOCX·PDF를 독립 책임 원본으로 수정하지 않음
- [ ] `NOT_BUILT/STALE/FAILED/CURRENT` 상태 정확

| 문서 ID | DOCX | PDF | diagrams/assets | Manifest | 자동 렌더 | 사람 시각 검수 |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

## Foundation·분야 프로젝트 스킬

- 적용한 Foundation 스킬:
- 적용한 분야 스킬:
- 호출하지 않은 후속 스킬과 조건:
- [ ] `SKILL_REGISTRY.json`의 Trigger·상태·경로 확인
- [ ] 전체 skills 폴더를 기본 로드하지 않음
- [ ] 주 책임 분야 스킬 최대 하나·Foundation 최소 호출
- [ ] 분야 스킬이 관련 JSON·실제 파일·검증을 연결
- [ ] 실패·중요 결정·재사용 가능한 교훈·실제 검증 결과를 Learning Log에 기록
- [ ] 스킬 변경 시 Skill Map DOCX/PDF·assets·Manifest 재생성
- [ ] `PROJECT_SKILL_MAP.md`를 만들지 않음

## 이미지·자산·사운드

- [ ] 영향 없음
- [ ] 기존 승인 이미지 확인
- [ ] 사용자 승인 없이 동일 항목의 새 시안을 만들지 않음
- [ ] Asset ID·캐노니컬 경로·상태 갱신
- [ ] 채택·비채택 요소 기록
- [ ] 콘셉트·실제 캡처 구분
- [ ] 관련 JSON `approved_visuals`와 사람용 문서 갱신
- [ ] 오디오 이벤트·믹싱·검증 상태 구분

## 기존 프로젝트 마이그레이션·수명주기

해당 없으면 `해당 없음`으로 표시한다.

- [ ] 첫 단계에서 Audit only 수행
- [ ] 사용자 승인 전 대규모 삭제·이동·통합 없음
- [ ] 승인 결정·수치·구현·자산·실패·보류 보존
- [ ] 코드·문서·Issue·PR·Registry·PDF·자동화 참조 검색
- [ ] 변경 전후 보존 대조 작성
- [ ] 기존 본책은 JSON 승계·발행·참조 검증 전 제거하지 않음
- [ ] 백업·보류·제거 후보 조건 기록

| 기존 내용 | 기존 위치 | JSON 위치 | 사람용 출력 | 보존·참조 검증 |
|---|---|---|---|---|
|  |  |  |  |  |

## 검증

| 검증 | 명령·절차 | 결과 | 증거 |
|---|---|---|---|
| 포맷·문법·정적 |  |  |  |
| 자동 테스트 |  |  |  |
| 핵심 정상·실패 경로 |  |  |  |
| 저장·호환성 |  |  |  |
| 실제 플레이·시각·오디오·성능 |  |  |  |
| Documentation Governance |  |  |  |
| Skill Routing Governance |  |  |  |
| Design Publication Governance |  |  |  |
| DOCX/PDF 생성·렌더 |  |  |  |
| 콜드 스타트·Health Review |  |  |  |

## Acceptance Criteria

- [ ] 조건 → 행동 → 관찰 결과로 확인 가능
- [ ] 승인된 범위를 만족
- [ ] 제외·보호 범위를 침범하지 않음
- [ ] JSON·Registry·Skill·발행본·실제 결과가 일치

## 미검증·위험·다음 작업

- 미검증:
- 불일치:
- 남은 위험:
- 사용자 확인:
- 다음 작업:
- 선행·재개 조건:
- 다음 작업자가 먼저 읽을 JSON·Registry·Skill:
- Base 환류 후보:
