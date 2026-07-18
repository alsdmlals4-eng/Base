# 작업 시작·개발 게이트·종료 체크리스트

실제 게임 프로젝트 작업에서 사용하는 공용 체크리스트다. 실행하지 않은 자동화·테스트·렌더링·브랜치 보호를 완료로 표시하지 않는다.

## 1. Intake·Context

- [ ] 최신 사용자 지시와 프로젝트 `AGENTS.md`를 확인했다.
- [ ] 활성 `[기획서]`가 저장소 루트에 있는지 확인했다.
- [ ] START_HERE·Active Context·Handoff·Documentation Map을 확인했다.
- [ ] Development Gates·Roadmap·Issue·Plan을 확인했다.
- [ ] `DESIGN_DOCUMENT_REGISTRY.json`과 관련 기획서 JSON을 확인했다.
- [ ] `SKILL_REGISTRY.json`에서 현재 요청에 필요한 최소 스킬만 선택했다.
- [ ] 실제 코드·데이터·자산·테스트·최근 diff를 확인했다.
- [ ] 백업·보류·제거 후보는 기본 읽기에서 제외했다.

## 2. 분야·영향도·스킬 선언

```yaml
primary_discipline:
affected_disciplines:
change_type:
required_design_document_ids:
goal:
user_or_player_value:
scope:
out_of_scope:
protected_paths:
foundation_skills:
discipline_skills:
deferred_skills:
asset_impact:
data_impact:
publication_impact:
lifecycle_impact:
acceptance_criteria:
validation:
```

- [ ] 주 책임 분야 하나와 영향 분야를 지정했다.
- [ ] Skill Trigger·사용·비사용 조건을 확인했다.
- [ ] 전체 skills 폴더를 기본 로드하지 않았다.
- [ ] 주 책임 분야 스킬은 최대 하나다.
- [ ] Foundation 스킬은 필요한 최소 개수다.
- [ ] 발행·검증·Handoff 스킬은 해당 단계에서만 호출한다.
- [ ] `DOCUMENT_UPDATE_MATRIX.md`로 갱신 대상을 판정했다.

## 3. 기존 프로젝트 안전 마이그레이션

운영 중인 프로젝트 구조를 바꾸는 경우:

- [ ] 첫 단계는 Audit only다.
- [ ] 승인 결정·세계관·수치·구현·자산·실패·보류를 보존 대상으로 등록했다.
- [ ] Markdown·JSON·DOCX·PDF·이미지·코드·Issue·Skill·자동화 참조를 조사했다.
- [ ] 기존 원본별 고유 정보와 중복·충돌·위험을 기록했다.
- [ ] JSON 책임 구조와 사람용 발행 구조를 먼저 제안했다.
- [ ] 사용자 승인 전 대량 삭제·이동·통합·강제 개명을 하지 않았다.
- [ ] 변경 전후 보존 대조표를 작성했다.
- [ ] JSON 승계·DOCX/PDF 발행·참조 검증 전 기존 본책을 제거하지 않았다.

## 4. Definition of Ready

- [ ] 프로젝트 방향과 핵심 경험에 기여하는 방식이 명확하다.
- [ ] 포함·제외 범위와 보호 대상이 있다.
- [ ] 선행 결정·의존성·보류 재개 조건이 해결됐다.
- [ ] 관련 Design Document ID·JSON·실제 대상 파일이 확인됐다.
- [ ] 저장·호환성·이관·승인 자산 위험이 있다.
- [ ] 완료 기준이 `조건 → 행동 → 관찰 결과`다.
- [ ] 정상·실패·회귀·사용자 검수 방법이 있다.
- [ ] 관련 스킬과 사람용 발행 영향이 판정됐다.

## 5. Planning·Approval

- [ ] Plan이 실제 저장소 조사 결과를 포함한다.
- [ ] 변경·보호 파일과 상태 소유가 명확하다.
- [ ] 이미지·UI·사운드·데이터·저장 영향이 있다.
- [ ] 실패·취소·폴백·롤백이 있다.
- [ ] JSON·Registry·Skill·Learning Log·DOCX/PDF 갱신 계획이 있다.
- [ ] L2 이상 또는 대형 마이그레이션은 사용자 승인을 받았다.

## 6. 구조화 기획서 JSON

- [ ] 질문별 현행 JSON 책임 원본이 하나다.
- [ ] 프로젝트 전체와 11개 분야 책임이 Registry에서 보존된다.
- [ ] 목적·플레이어 가치·현재 목표가 있다.
- [ ] Quality Bar·금지 방향이 있다.
- [ ] 책임·비책임·분야 간 입력·출력 계약이 있다.
- [ ] 전체 작업 과정이 입력→판단→산출물→검증→다음 게이트로 연결된다.
- [ ] 작업·제품 게이트와 관련 스킬이 연결된다.
- [ ] 확정·구현·검증·확인 필요·보류를 분리했다.
- [ ] 실제 코드·데이터·자산·테스트 경로가 있다.
- [ ] 승인 이미지·실제 캡처에 Asset ID·상태·채택 범위가 있다.
- [ ] 위험·다음 작업·Ready·Done이 있다.
- [ ] 활성 Markdown 기획 본책을 만들지 않았다.

## 7. 프로젝트 스킬과 항상 학습

- [ ] 공용 절차는 Foundation에 한 번만 있다.
- [ ] 분야 스킬이 관련 JSON·실제 경로·산출물·검증을 연결한다.
- [ ] Trigger·비사용 조건·Ready·Done·실패 조건이 있다.
- [ ] 활성 스킬은 `load_by_default=false`다.
- [ ] 실패·중요 결정·재사용 가능한 교훈·실제 검증 결과를 Learning Log에 기록했다.
- [ ] 성공·부분 성공·실패·미검증·예외·사용자 피드백을 기록했다.
- [ ] 과다 호출·누락 스킬·검증을 기록했다.
- [ ] 스킬 변경 필요 여부와 변경하지 않는 이유를 기록했다.
- [ ] 지식 상태를 관찰·가설·패턴·검증·승격 후보로 구분했다.
- [ ] Skill Registry 변경 시 Skill Map DOCX/PDF·assets·Manifest를 재생성했다.
- [ ] `PROJECT_SKILL_MAP.md`를 만들지 않았다.

## 8. 이미지·자산·사운드

- [ ] 기존 승인 이미지가 있는 항목에 임의 새 시안을 만들지 않았다.
- [ ] Asset ID·캐노니컬 경로·상태가 일치한다.
- [ ] 콘셉트·승인·제작 준비·구현·시각 검증을 구분했다.
- [ ] 채택·비채택 요소를 JSON에 기록했다.
- [ ] 실제 캡처와 콘셉트를 구분했다.
- [ ] Import·피벗·해상도·프레임·성능 예산을 확인했다.
- [ ] 오디오 제작·이벤트 연결·믹싱·검증 상태를 구분했다.

## 9. Implementation

- [ ] 승인 Plan에 직접 관련된 파일만 변경했다.
- [ ] 가장 작은 검증 가능한 변경을 사용했다.
- [ ] 기능 추가와 대규모 리팩터링을 분리했다.
- [ ] 저장 형식·공개 인터페이스·사용자 흐름을 승인 없이 변경하지 않았다.
- [ ] 보류 항목을 별도 승인 없이 구현하지 않았다.
- [ ] 범위 밖 개선은 별도 제안으로 분리했다.

## 10. Verification

- [ ] 포맷·문법·타입·정적 검사
- [ ] 관련 자동 테스트
- [ ] 핵심 정상 경로
- [ ] 실패·취소·중복 입력·누락 데이터
- [ ] 저장·불러오기·호환성
- [ ] 실제 화면·플레이·오디오·성능·접근성
- [ ] diff가 승인 범위를 벗어나지 않음
- [ ] 실행하지 못한 검증은 `[미검증]`

## 11. 사람용 DOCX/PDF·다이어그램 발행

- [ ] `DESIGN_DOCUMENT_REGISTRY.json`의 활성 문서를 확인했다.
- [ ] JSON 변경 후 `build_design_documents.py`를 실행했다.
- [ ] workflow·status·responsibility 다이어그램을 생성했다.
- [ ] 승인 이미지·실제 캡처를 포함했다.
- [ ] DOCX가 유효한 OOXML 파일이다.
- [ ] PDF가 실제 PDF다.
- [ ] PDF 전 페이지를 PNG로 렌더했다.
- [ ] 빈 페이지·한글 깨짐·표·문장·이미지 잘림·겹침을 확인했다.
- [ ] JSON·생성기·출력·다이어그램·승인 이미지 SHA-256 Manifest가 최신이다.
- [ ] DOCX·PDF를 독립 책임 원본으로 수동 수정하지 않았다.
- [ ] 미생성·오래됨·실패를 `NOT_BUILT/STALE/FAILED`로 정확히 표시했다.

## 12. Documentation·Publication Gate

같은 작업에서 확인:

- [ ] 관련 기획서 JSON·Design Document Registry
- [ ] Skill Registry·Skill·Learning Log
- [ ] Skill Map DOCX/PDF·assets·Manifest
- [ ] 기획서 DOCX/PDF·assets·Manifest
- [ ] Roadmap·Development Gates
- [ ] Active Context·Handoff·Documentation Map
- [ ] Decision Log·Changelog
- [ ] Visual Source·Asset Manifest
- [ ] Issue·Goal·Plan·README

## 13. GitHub Governance

- [ ] `check_documentation_governance.py`
- [ ] `check_skill_routing_governance.py`
- [ ] `check_design_document_publications.py`
- [ ] DOCX/PDF 실제 생성 통합 테스트
- [ ] 정상·실패 회귀 테스트
- [ ] GitHub Actions 실제 실행 성공
- [ ] Required Status Check·CODEOWNERS·브랜치 보호 실제 활성 상태 확인

## 14. Integration·Completion

- [ ] Acceptance Criteria 증거가 있다.
- [ ] 승인·구현·검증·사용자 확인 상태를 분리했다.
- [ ] JSON·두 Registry·Skill·발행본이 최신이다.
- [ ] 미검증·불일치·위험을 기록했다.
- [ ] 이동·제거 후 잔여 참조가 없다.
- [ ] PR Required Checks와 리뷰가 통과했다.
- [ ] 다음 작업·선행 조건·Handoff가 있다.
- [ ] 새 AI가 저장소만으로 방향·상태·JSON·사람용 PDF·스킬·검증을 찾는다.
- [ ] 프로젝트 전용 교훈과 Base 환류 후보를 분리했다.

## 15. 완료 보고

```md
## 결과
- 주 책임·영향 분야:
- 변경한 JSON·실제 파일·스킬:
- 생성한 DOCX·PDF·다이어그램·Manifest:
- 유지한 결정·동작·자산:
- 실행한 검증:
- 사람 시각 검수:
- 미검증·불일치·위험:
- 보존·백업·보류·제거 후보:
- 콜드 스타트 결과:
- Learning Log·Base 환류:
- 다음 작업:
```
