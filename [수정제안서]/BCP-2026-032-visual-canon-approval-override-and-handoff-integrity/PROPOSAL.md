# BCP-2026-032 — Visual Canon Approval Override & Handoff Integrity

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/omenward`
- 출처 Decision: `OMW-PLAN-20260825-FRONT-STATE-MINIMAP-SD-FANTASY-01`
- 출처 작업 PR: `alsdmlals4-eng/omenward#210`
- 출처 관찰 commit: `315d5e48b2a2d49f9d9863f3d07b66ba651bf9f7`
- 기준 Base main: `bfdadb87d0d7434c1f6beda1bdd8d33ca5e516bf`
- 제출일: `2026-08-25`
- 상태: `SUBMITTED`
- active Base implementation: `NOT_AUTHORIZED`
- 추가 금전 비용: `0`

## 문제

프로젝트의 시각 정본이 여러 세션에 걸쳐 발전할 때, 최신 사용자 승인보다 오래된 이미지/문서가 더 눈에 띄는 위치에 남으면 다음 세션이 다음 오류를 반복할 수 있다.

1. 오래된 North Star/시안이 현재 정본처럼 읽힌다.
2. 최신 승인 Decision은 텍스트에는 존재하지만 사람이 보는 Project Home/Visual Bible의 첫 화면에는 반영되지 않는다.
3. 승인 이미지는 대화 산출물에만 있고 안정적인 Asset ID/원본 locator/hash가 없다.
4. 새 이미지 생성 전에 실제 승인 이미지를 다시 읽지 않고 prose 요약만으로 스타일을 재구성해 품질/정체성이 드리프트한다.
5. 이미지 승인, runtime 가독성, human usability, 권리 검수가 하나의 `PASS`처럼 뭉개질 수 있다.
6. handoff가 상태 요약만 보존하고 **무엇이 superseded 되었는지**를 명시하지 않아 과거 규칙이 다시 살아난다.

OMENWARD에서 실제로 초반 생성물이 프로젝트 장르/플레이어 역할/기존 시안과 어긋났고, 사용자가 `프로젝트랑 노션에서 시안부터 확인`하도록 교정했다. 이후 최신 승인 Decision을 Notion 최상단 override + 승인 이미지 + repository router + handoff에 동시에 남기자 다음 세션의 복원 경계가 명확해졌다.

상세 evidence:
`[수정제안서]/BCP-2026-032-visual-canon-approval-override-and-handoff-integrity/evidence/OMENWARD_VISUAL_CANON_HANDOFF_LESSONS.md`

## 일반화 후보

새 시각 Skill을 추가하지 않고, 기존 프로젝트 intake/design-document/UI-art/handoff 흐름에 다음 **closeout invariant**를 도입하는 방안을 제안한다.

```text
USER_APPROVES_VISUAL_DIRECTION_OR_REFERENCE
→ assign stable Decision ID + Asset ID
→ persist full-resolution authority asset or durable locator
→ record exact adopted / superseded / reference-only boundaries
→ update repository high-authority visual router/index
→ place current approved visual/override before stale visuals on Notion human surface
→ preserve older visuals as lineage, do not silently delete
→ read back repository + Notion image block + asset locator
→ write new-session handoff that requires refetching approved visual before new generation
→ keep runtime / human / rights evidence ceilings separate
```

Proposed reusable markers:

- `APPROVED_VISUAL_ASSET_REQUIRED_FOR_HANDOFF` — human-approved reference must have a stable Asset ID and durable locator before visual closeout.
- `VISUAL_SUPERSESSION_BOUNDARY_REQUIRED` — ADOPT/RETAIN/SUPERSEDE/REFERENCE_ONLY must be explicit; an older visual remains historical evidence, not silent current truth.
- `HUMAN_SURFACE_CURRENT_OVERRIDE_FIRST` — if legacy visual content is retained on a Notion/Home/Bible page, a current override and approved visual must appear before it.
- `APPROVED_VISUAL_REFETCH_BEFORE_GENERATION` — a new visual-generation session must fetch the approved reference/asset, not reconstruct it only from prose memory.
- `VISUAL_APPROVAL_EVIDENCE_SPLIT` — user approval of visual direction/reference does not imply runtime readability, accessibility, performance, rights, or human usability PASS.
- `VISUAL_HANDOFF_DESTINATION_READBACK` — closeout is incomplete until the human-facing image block and structured locator/Decision are read back.

## 최소 3안 비교

| 안 | 장점 | 위험/비용 | 판정 |
| --- | --- | --- | --- |
| A. 승인 시 이미지 파일만 저장 | 가장 단순 | supersession/라우팅/Notion 첫 화면/새 세션 규칙이 없어 stale visual 재발 가능 | `REJECT` |
| B. 모든 과거 visual 문서를 즉시 삭제/전면 재작성 | 현재성은 명확 | 계보·채택 근거 손실, 큰 churn, 다른 owner와 충돌 | `REJECT` |
| C. stable Asset+Decision + current override first + explicit supersession + handoff/readback | 계보를 보존하면서 새 세션 drift를 차단, 기존 authority split과 호환 | 작은 metadata/handoff 비용 | `ADOPT` |

## 프로젝트 전용으로 남길 내용

다음은 Base로 승격하지 않는다.

- OMENWARD의 3개 전선, 전선별 미니맵, 3x3 룰렛.
- Omen Warden, 긴 지휘 깃발, Veil 세계관.
- Fantasy/Magic/SD Tactical Pixel 그림체 명칭과 팔레트.
- OMENWARD Asset/Decision/Notion page/Drive file ID.
- 특정 게임의 UI 배치, 캐릭터 비율, HUD, 전투 화면.

Base에는 **승인된 시각 정본의 보존·supersession·handoff·readback 절차**만 일반화한다.

## 반례 / 비사용 조건

- 단순 throwaway moodboard/아이디어 스케치로 사용자가 승인하지 않은 경우에는 stable canon asset 등록을 강제하지 않는다.
- 코드/데이터만 바뀌고 visual authority가 변하지 않은 작업에는 적용하지 않는다.
- Notion이 없는 프로젝트는 같은 의미를 프로젝트가 선언한 human-facing surface로 대체한다.
- full-resolution binary를 반드시 Git repository에 넣으라는 규칙이 아니다. Repo는 Asset ID/hash/locator를 소유하고, human asset workspace/Drive가 binary를 소유할 수 있다.
- 오래된 visual은 감사/계보 가치가 있으면 삭제하지 않고 `SUPERSEDED`/`REFERENCE_ONLY`로 보존한다.
- 이미지 생성 모델의 prompt를 정본으로 승격하지 않는다.

## 예상 영향 범위

승인 후 구현 후보는 기존 owner에 흡수한다. 신규 독립 Skill을 기본안으로 만들지 않는다.

후보 owner:
- `skills/managing-project-intake-and-work-contract/` — 새 visual 작업 진입 시 approved visual refetch/authority check.
- `skills/managing-design-documents/` — Decision/Asset/Notion human surface sync + readback.
- existing UI/art audit owner — approved reference vs generated candidate comparison.
- handoff/continuation contracts — visual supersession and exact asset locator preservation.

실제 구현 범위와 테스트는 별도 Base 승인 뒤 결정한다. 이 제출은 위 후보 owner를 즉시 수정하지 않는다.

## 검증 제안

승인 후 구현 시 최소 focused regression은 다음을 증명해야 한다.

1. approved visual Decision이 있으면 handoff에 Asset ID/locator/supersession가 존재한다.
2. legacy visual이 남아 있어도 current human-facing surface가 current override를 먼저 노출한다.
3. image approval과 runtime/human/rights evidence가 별도 상태로 유지된다.
4. new-session visual task는 current approved reference readback을 요구한다.
5. Notion 미사용 프로젝트에 과도하게 강제되지 않는다.
6. 프로젝트 고유 미감/자산을 Base canon으로 복제하지 않는다.

## 비용·보안·권리

- 신규 SaaS/dependency/runtime 없음.
- 추가 비용 0.
- binary 저장 위치는 프로젝트 정책을 유지한다.
- 외부/AI 생성 이미지의 권리 검수는 별도 evidence이며 이 제안이 자동 승인하지 않는다.
- signed/temporary Notion URL을 durable authority locator로 고정하지 않는다. durable locator는 Notion page/asset workspace/file ID와 repository metadata를 사용한다.

## 사용자 가치와 장기 적합성

이 제안의 목적은 이미지 제작량을 늘리는 것이 아니라 **한 번 승인한 시각 방향을 다음 채팅에서 다시 잃지 않게 하는 것**이다. 프로젝트가 장기적으로 여러 이미지, Notion Bible, repository spec을 함께 운영할수록 최신 승인과 역사 reference의 구분 비용이 커지므로, 좁은 closeout invariant가 재작업 비용을 줄인다.

## 승인과 구현

- 현재 상태: `SUBMITTED`.
- 사용자 요청: OMENWARD closeout 과정에서 `Base 승격, 문제-교훈 자료도 잘 올려줘`라고 명시.
- 해석: Base 공용 후보로 **제안 제출과 evidence 보존**은 승인됨. active Base owner/Skill/규칙 수정·구현은 별도 `APPROVED_FOR_IMPLEMENTATION` gate가 필요하다.
- 구현 권한: `NOT_AUTHORIZED_IN_THIS_PROPOSAL`.
