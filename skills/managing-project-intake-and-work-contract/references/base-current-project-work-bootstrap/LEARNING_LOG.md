# Base-current project work bootstrap — Learning Log

## 2026-09-02 — Base-current zero-install PM bootstrap

- **상태:** `OBSERVATION`
- **호출 트리거:** 사용자가 프로젝트 저장소를 일괄 수정하지 말고 Base만 교정해, 이후 프로젝트 작업이 최신 Base를 fresh-read하면 PM 체크리스트와 작업 Gate를 바로 사용할 수 있게 하라고 지시했다.
- **Finding:** 병합된 PM Gate는 정확한 완료 판정을 제공했지만 활성 진입 문서가 프로젝트별 adapter pin·wrapper·repository receipt를 선행 조건으로 유지해, Base만 읽은 새 프로젝트 작업이 공용 절차를 실행하기 어려웠다. 공용 CLI와 owner를 추가한 뒤에는 focused·전체 검증이 통과했지만 canonical freshness가 intake Skill 변경에 기존-suite companion과 Skill 학습 기록이 함께 갱신되지 않은 상태를 차단했다.
- **Decision:** 프로젝트 채택 Base release와 프로젝트 정본은 그대로 유지한다. 최신 Base는 비영구 `BASE_CURRENT_OPERATIONAL_BOOTSTRAP` PM/workflow overlay만 제공한다. Receipt는 stdin·임시 파일·기존 프로젝트 owner에서 공급할 수 있고 Base CLI는 대상 프로젝트를 쓰지 않는다. 프로젝트별 wrapper·공용 Skill 복사·빈 receipt 배포·fleet mutation은 만들지 않는다.
- **TDD / 회귀 증거:** `tests/test_base_current_project_work_bootstrap.py`가 owner·CLI·독립 Base/project revision·ephemeral receipt·비변경·closeout HEAD 경계를 직접 검증한다. `tests/test_p08_ai_operations_contract.py`가 해당 공용 경로와 이 학습 기록을 기존 AI 운영 계약의 companion으로 검증한다. 최초 RED run `33585916370`은 owner/CLI/route 부재를 재현했고, 중간 GREEN run `33588082514`는 의존성이 설치된 동일 tree에서 focused 8개와 전체 1772개 테스트를 통과했다. Exact-head required CI·독립 review·merge·postmerge readback은 별도 완료 증거다.
- **Evidence ceiling:** Gate PASS는 supplied receipt와 exact Base/project revision의 기록 일관성만 증명한다. 프로젝트 전체 backlog 완전성, 외부 evidence 진실성, 프로젝트 adopted release 변경, Godot runtime·시각·UX·Human QA 또는 출시 상태를 증명하지 않는다.
- **다음 검토 트리거:** 새 프로젝트 작업이 다시 project-side Base preinstall·wrapper·adapter 갱신 없이는 시작되지 않거나, current Base가 프로젝트 product canon/adopted release를 조용히 교체하거나, ephemeral receipt가 두 번째 상태 정본으로 승격되거나, intake Skill 변경이 기존 companion test·Learning Log 없이 standalone test만 통과할 때.
