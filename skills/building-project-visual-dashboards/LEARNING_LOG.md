# Building Project Visual Dashboards Learning Log

## 2026-08-19 — standalone HTML dashboard retirement

- **Status:** `SUPERSEDED_BY_NOTION_WORKSPACE`.
- **Trigger:** 사용자가 프로젝트 기획·상태·시각 관계를 위한 별도 HTML/local surface를 더 이상 사용하지 않고 Notion을 사람용 기본 작업면으로 확정했다.
- **Finding:** 이 Skill의 가치 중 복잡한 관계 시각화, 상태·위험 표시, 구현 증거와 정본 분리 원리는 유효하지만, standalone HTML/CSS/JavaScript surface 자체는 Notion Project Home·Core System·Visual Map과 중복되어 컨텍스트와 동기화 비용을 만든다.
- **Decision:** 새 HTML을 생성하는 동작은 폐기하고 기존 Skill ID는 일시적 compatibility locator로만 유지한다. 유효 목적은 `NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`, repository structured/runtime truth, `REPOSITORY_NATIVE_QA_EVIDENCE`로 라우팅한다.
- **Protection:** historical dashboard를 자동으로 current canon으로 승격하지 않으며, 고유 데이터가 있으면 `DEPRECATED_SURFACE_ABSORB_THEN_DELETE`로 먼저 이관·readback한다.
- **Validation:** `tests/test_bca_visual_sheet_workflow.py`, canonical-reference freshness, exact-head PR CI가 replacement route와 retired execution boundary를 검증한다.
- **Next trigger:** Registry/consumer inventory에서 material consumer가 0이 되면 compatibility Skill package와 Registry entry 자체를 함께 삭제한다.
