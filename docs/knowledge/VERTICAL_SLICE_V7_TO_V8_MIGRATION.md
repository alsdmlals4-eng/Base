---
document_role: MIGRATION_TRACEABILITY
source_contract: VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7
replacement_execution_prompt: templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md
active_authority: false
implementation_authority: NONE
---

# Vertical Slice 통합 실행문 v7 → v8 마이그레이션

v8은 v7의 상세 정본·인터뷰·Demo-First·GPT→Codex·적대적 검토·완전성 계약을 삭제하지 않고 승계한다.

추가된 책임:

1. B — 세계관·핵심루프·주요인물·조연·핵심시스템·이미지 탭을 포함한 프로젝트 Sheet 구조.
2. C — 기획 중 GPT 시각화와 기획 종료 시 실사용 후보 이미지·목업 생성.
3. A — 이미지 상태·검수·승인·정본·Sheet·자산 원장 동기화와 적대적 검토.

v7은 `SUPERSEDED_COMPATIBILITY`로 보존하며 새 작업 진입점으로 사용하지 않는다. 프로젝트가 v7을 참조하면 `STALE_PROMPT_CONTRACT`로 판정하고 v8로 전환한다.
