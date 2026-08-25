# 2026-08-25 · Handoff resumability / Visual readback / learning-promotion evidence

## Status

- classification: `BASE_PROMOTION_EVIDENCE`
- implementation_authority: `NONE`
- scope: project/session handoff closure quality
- target owners:
  - `docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md`
  - `templates/project-operations/HANDOFF.md`
  - P01/P05 learning owners are recurrence/evidence consumers, not duplicate policy owners

## Problem

여러 프로젝트를 AI 세션 간 이어갈 때 인수인계가 단순 상태 요약으로 끝나면 다음 문제가 반복될 수 있다.

1. 현재 작업이 안전한 checkpoint까지 닫히기 전에 handoff가 작성되어 실제 정본과 handoff가 어긋난다.
2. 새 채팅이 GitHub·Notion만으로 재개하지 못하고 과거 대화의 숨은 맥락에 의존한다.
3. Notion 이미지가 파일명·URL·Asset metadata만 존재하고 실제 Home/Visual 목적지에서 attach/readback되지 않았는데도 전달 완료로 오인한다.
4. 승인 이미지의 용도·현재성·supersession이 불명확해 새 세션이 오래된 시안을 현행 정본처럼 소비한다.
5. 작업 중 발견한 문제와 해결 교훈이 프로젝트 세션에만 남아 다른 프로젝트에서 같은 실패가 반복된다.
6. 반대로 모든 교훈을 즉시 새 Skill/정책으로 만들면 Base canonical owner가 중복되고 routing/context 비용이 커진다.
7. `BASE_PROMOTION_CANDIDATE`를 “승격 검토” 상태만 기록하고 실제 Base write/readback 없이 종료하면 사용자가 요구한 공용 학습 축적이 실행되지 않는다.

## What worked

- Handoff를 `현재 작업 checkpoint → GitHub 정본 재확인 → Notion 정본 재확인 → Active Context 갱신 → Handoff snapshot → fresh-chat 재개 테스트 → Visual delivery audit → 문제/교훈 disposition → Base 기록·readback` 순서의 종료 트랜잭션으로 정의한다.
- 새 채팅 품질을 과거 대화 복사 여부가 아니라 **GitHub + Notion current canon만으로 복원 가능한가**로 판정한다.
- Visual 전달은 `URL/metadata present`와 `upload/attach`, `destination readback`, `attachment/image readback`, `HUMAN_VISIBLE_PASS`, `runtime product asset approval`을 분리한다.
- 문제/교훈은 `PROJECT_ONLY / PART_ONLY / BASE_PROMOTION_CANDIDATE / NO_NEW_REUSABLE_LESSON`로 분류하고, Base 승격은 기존 canonical owner 흡수를 기본값으로 한다.
- `BASE_PROMOTION_CANDIDATE`는 실제 Base learning/evidence write + destination readback을 Handoff READY 조건으로 둔다.
- 같은 owner를 열린 PR이 수정 중이면 해당 PR을 수정·흡수하지 않고 독립 Base evidence/candidate를 실제 기록·readback해 `DEFERRED_BY_CONCURRENT_OWNER`로 남긴다.
- 작업 도중 관련 PR이 병합되면 stale한 `OPEN/DEFERRED` 주장을 그대로 유지하지 않고 최신 main을 다시 읽어 disposition을 교정한다.

## Reusable lesson

**인수인계의 품질은 요약의 길이가 아니라 새 세션의 재현 가능성과 필요한 학습의 실제 writeback으로 검증해야 한다.**

좋은 handoff는 별도 제2정본이 아니라 현재 정본을 닫은 뒤 생성되는 압축 스냅샷이다. 완료 판정에는 다음이 함께 필요하다.

- 현재 bounded work의 안전한 checkpoint
- GitHub runtime/structured truth readback
- Notion human/system truth readback
- 승인 Visual의 실제 목적지 전달·현재성 검증
- 과거 대화 없이 수행하는 fresh-chat cold-start test
- 실제 문제의 원인/해결/증거와 재사용 범위 판정
- 공용 가치가 있는 교훈의 Base evidence/learning 실제 기록과 readback
- handoff 작성 중 main/PR 상태가 바뀌면 최종 receipt 전에 다시 읽는 freshness reconciliation

## Anti-patterns

- handoff를 쓰기 위해 현재 작업을 중간 상태로 버림
- 대화 요약문을 GitHub/Notion보다 높은 정본처럼 사용
- "이미지 링크가 있다"를 "Notion에 승인 이미지가 정상 전달되었다"로 해석
- readback PASS를 human-visible/runtime PASS로 승격
- superseded/rejected Visual을 현재 승인본과 같은 위치에 모호하게 남김
- 모든 실패를 프로젝트 내부 메모로만 보존
- `BASE_PROMOTION_CANDIDATE`를 실제 Base write/readback 없이 proposal 문구만 남김
- 단일 프로젝트 경험만으로 새 광역 Skill을 즉시 생성
- 열린 PR이 소유한 canonical owner를 새 branch에서 흡수·재작성
- handoff 시작 시점의 open/merged 상태를 최종 상태처럼 고정

## Promotion disposition

- `docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md`: 공용 불변 원칙 직접 보강
- `templates/project-operations/HANDOFF.md`: 실행 receipt와 fresh-chat/Visual/lesson Gate 직접 보강
- 이 evidence 파일 자체: Base branch에 실제 기록하고 readback 완료
- P01/P05 Learning Log: PR #681이 작업 중 main에 병합되어 adjacent cold-start/Visual evidence를 이미 기존 owner에 승격했다. 이번 공용 protocol 전문을 또 복제하지 않고 method/template을 owner로 유지한다.
- 별도 신규 broad Skill: `REJECT_DUPLICATE_OWNER`; PR #674가 기존 `maintaining-project-context-and-handoff` Skill을 수정 중이므로 해당 open branch는 계속 read-only 보호한다.

## Concurrent work reconciliation observed on 2026-08-25

- PR #674: **OPEN** · `maintaining-project-context-and-handoff` Skill 및 GPT/Codex role split 수정. 이번 PR은 해당 Skill 파일을 수정하지 않는다.
- PR #693: **OPEN** · visual canon approval/handoff proposal. proposal owner를 수정하지 않는다.
- PR #681: 작업 중 **MERGED** · merge SHA `34bb91257e1e7591b30939f5752aa5c00f627e84`. P01/P05 Learning Log의 adjacent handoff/Visual evidence를 최신 main context로 인정한다.
- PR #695: 이번 branch의 baseline에 이미 **MERGED** · baseline `2ebccd87a0a44af86418da7700993743b2f4fdb3`. Tetris image-work case를 별도 owner로 보존한다.

이번 변경은 open #674/#693을 수정·rebase·merge·close하거나 branch를 흡수하지 않는다. 완료된 #681/#695의 지식은 latest-main readback 대상으로만 소비한다.

## Evidence ceiling

이 문서는 handoff 운영 규칙과 재발 방지 구조의 Base promotion evidence다. 특정 프로젝트 runtime, 특정 Notion 이미지의 현재 human-visible 상태, 모든 프로젝트에서의 반복 재현, 또는 별도 열린 PR의 최종 병합을 증명하지 않는다.

## Revisit condition

- 실제 프로젝트에서 `인수인계 진행`을 수행한 뒤 fresh-chat resume test가 실패할 때
- Notion Visual readback와 사용자 화면 노출이 불일치할 때
- 같은 handoff failure가 두 번째 프로젝트에서 반복될 때
- PR #674/#693이 완료되어 Skill/proposal consumer에 별도 integration 필요성이 생길 때
