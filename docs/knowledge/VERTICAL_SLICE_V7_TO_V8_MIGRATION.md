---
document_role: MIGRATION_TRACEABILITY
source_contract: VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7
replacement_execution_prompt: templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md
active_authority: false
implementation_authority: NONE
---

# Vertical Slice 통합 실행문 v7 → v8 마이그레이션

v8은 v7의 상세 정본·인터뷰·Demo-First·GPT→Codex·적대적 검토·완전성 계약을 삭제하지 않고 승계한다.

추가된 책임:

1. B — 세계관·핵심루프·주요인물·조연·핵심시스템·이미지 탭을 포함한 프로젝트 Sheet 구조.
2. C — 기획 중 GPT 시각화와 기획 종료 시 실사용 후보 이미지·목업 생성.
3. A — 이미지 상태·검수·승인·정본·Sheet·자산 원장 동기화와 적대적 검토.

## 활성 권한

```text
최신 사용자 승인
→ 프로젝트 정본·실제 파일·Decision·PR
→ 프로젝트가 고정한 Base main SHA
→ VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md
→ 이 Migration Traceability 기록
```

v7은 `SUPERSEDED_COMPATIBILITY`로 보존하며 새 작업 진입점으로 사용하지 않는다. 프로젝트가 v7을 활성 실행문으로 참조하면 `STALE_PROMPT_CONTRACT`로 판정하고 v8로 전환한다.

## 상태 매핑

| v7 또는 프로젝트 구형 상태 | v8 해석 |
|---|---|
| 별도 짧은 실행문 | 사용하지 않음. v8 한 파일과 저장소 우선 인터뷰로 통합 |
| 임의 Sheet 메모 탭 | 의미 구조 tab과 책임 정본 링크로 재구조화 |
| 생성 이미지 | `GENERATED_EXPLORATION` |
| 사용자 선택 이미지 | 검수 전에는 `APPROVED_CANDIDATE` 이하 |
| 최종 자산 | 권리·규격·실제 화면·자산 원장·적용 검증 뒤 `PROJECT_ASSET_APPROVED` |
| 적용 완료 | 실제 화면 또는 런타임 검증 뒤 `APPLIED_AND_RUNTIME_VERIFIED` |

## 프로젝트 적용 Gate

프로젝트 적용은 다음을 모두 만족해야 완료다.

- Base v8 병합 SHA를 프로젝트가 고정했다.
- 기존 v6·v7 활성 참조가 호환·역사 문맥으로 격리됐다.
- Sheet 상태가 `PROJECT_SHEET_CONFIGURED` 또는 `NOT_CONFIGURED`로 사실대로 기록됐다.
- 세계관·핵심루프·주요인물·조연·핵심시스템·이미지 계획·검수 책임이 프로젝트 정본에 연결됐다.
- 프로젝트 아트·UX·QA Skill 또는 Base adapter가 새 이미지 Mode를 라우팅한다.
- `repository-wide-audit`에서 차단 Finding이 남지 않았다.
