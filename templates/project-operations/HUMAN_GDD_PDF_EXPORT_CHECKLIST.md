# Human Detailed GDD PDF Export Checklist

> Status: `PROJECT_TEMPLATE`
> Artifact role: `HUMAN_GDD_PDF_DERIVED_VIEW`
> Canon owner: repository AI planning and implementation specification
> Default output: one downloadable human-facing detailed GDD PDF at a meaningful review gate

## 0. Export identity

```yaml
project:
project_id:
milestone:
document_title:
source_commit:
canon_version:
generated_at:
generator_or_method:
included_scope:
approval_status:
implementation_status:
evidence_ceiling:
unresolved_decisions:
blockers:
output_path: docs/exports/HUMAN_GDD_<milestone>_<source-sha>.pdf
```

### Identity Gate

- [ ] `source_commit`은 검토한 repository의 정확한 40자 commit SHA다.
- [ ] `canon_version`은 AI canon의 현재 version과 일치한다.
- [ ] `included_scope`가 전체 프로젝트인지 특정 Slice인지 명확하다.
- [ ] `implementation_status`와 `evidence_ceiling`이 계획·구현·검증 상태를 과장하지 않는다.
- [ ] 오래된 PDF를 최신 정본으로 오인하지 않도록 표지 또는 첫 페이지에 identity를 표시한다.

## 1. Export timing

다음 Gate에서만 기본 생성한다.

- [ ] `CORE_DIRECTION_AND_SYSTEM_APPROVAL`
- [ ] `PRE_CODEX_IMPLEMENTATION_HANDOFF`
- [ ] `MEANINGFUL_SLICE_OR_VERTICAL_SLICE_COMPLETION`
- [ ] `RELEASE_CANDIDATE_REVIEW`

작은 문구 수정이나 내부 정리마다 PDF를 재생성하지 않는다. 다만 구현 인계·사용자 승인에 쓰는 PDF의 `source_commit`이 현재 canon보다 오래되었다면 재생성한다.

## 2. Required human-facing sections

### A. Project definition and value

- [ ] 한 문장 정의, 장르, 플랫폼, 플레이 상황이 보인다.
- [ ] 플레이어가 무엇을 하고 왜 계속하는지 설명한다.
- [ ] 첫인상, 핵심 감정, 기억에 남을 순간과 판매·차별 포인트가 보인다.
- [ ] 보호해야 할 프로젝트 정체성과 변경 가능한 범위를 구분한다.

### B. Core loop and full flow

- [ ] 핵심 loop를 시작 → 선택 → 처리 → 피드백 → 결과 → 다음 선택 순으로 설명한다.
- [ ] 전체 게임 Flow 또는 현재 포함 범위를 한눈에 볼 수 있다.
- [ ] 화면·씬·상태 전환과 플레이어 행동이 연결되어 있다.
- [ ] 실패·보상·복구 흐름이 빠지지 않았다.

### C. Core systems and content

- [ ] 핵심 시스템마다 플레이어 목적, 입력, 규칙, 결과, 피드백이 있다.
- [ ] 시스템 간 의존성과 데이터 흐름이 보인다.
- [ ] 주요 콘텐츠 종류, 등장·획득 조건, 소비처와 변형 상태가 있다.
- [ ] 진행·경제·성장 구조가 선택과 trade-off 관점으로 설명된다.
- [ ] 기능 수가 아니라 플레이어 판단·감정·보상을 중심으로 설명한다.

### D. UX/UI and visual direction

- [ ] 주요 화면별 목적, 핵심 정보, 조작, 상태와 다음 화면이 있다.
- [ ] default/hover/focus/pressed/disabled/locked/warning/loading/success 상태가 필요한 범위만큼 설명된다.
- [ ] 정보 우선순위, 가독성, 입력 장치와 접근성 제약이 있다.
- [ ] Visual Direction은 실제 화면·씬·게임 오브젝트 소비처와 연결된다.
- [ ] 설명용 시각자료와 runtime asset을 혼동하지 않는다.

### E. Images, audio, VFX and asset implementation

- [ ] 실제 게임 소비처별 필요한 asset family를 보여준다.
- [ ] 캐릭터·적·UI·환경·효과의 필요한 방향·행동·상태·변형을 빠뜨리지 않는다.
- [ ] 승인된 asset과 candidate/reference/rejected asset을 구분한다.
- [ ] asset의 구현 경로와 상태를 사람이 이해할 수 있는 수준으로 설명한다.
- [ ] 사운드·VFX trigger와 플레이어 피드백 역할을 설명한다.

### F. Implementation method

- [ ] 각 핵심 시스템이 Godot에서 어떤 데이터·상태·씬·노드 책임으로 구현되는지 원리 수준에서 설명한다.
- [ ] AI canon의 의미 계약을 보존하되, 검증되지 않은 구체 코드 존재를 주장하지 않는다.
- [ ] 저장·불러오기, 입력, UI wiring, asset integration, 테스트 경로를 포함한다.
- [ ] 구현 완료·테스트 PASS·runtime PASS·UX PASS를 분리한다.

### G. Decisions, risks and remaining work

- [ ] 중요한 승인 결정과 superseded 결정이 구분된다.
- [ ] unresolved decision, blocker, risk와 재검토 조건이 있다.
- [ ] 명시적 제외 범위가 있다.
- [ ] 현재 남은 필수 작업과 다음 단일 마일스톤이 보인다.

## 3. Visual material quality

- [ ] 표·Flow·상태도·asset preview가 본문의 판단을 실제로 돕는다.
- [ ] 해상도, 축척, 캡션과 글자 크기가 PDF에서 읽을 수 있다.
- [ ] 이미지가 잘리거나 비율이 왜곡되지 않는다.
- [ ] 색에만 의존하지 않고 라벨·형태·패턴 등 의미 중복을 제공한다.
- [ ] source/reference 이미지의 권리·출처 상태가 필요한 범위에서 표시된다.
- [ ] 구현 증거 스크린샷은 프로젝트/build/commit identity와 연결된다.

## 4. Canon and drift Gate

```text
repository canon at source_commit
→ generate HUMAN_GDD_PDF_DERIVED_VIEW
→ render/readback every page
→ compare key decisions, systems, asset states and evidence ceiling
→ user review
→ approved changes return to repository canon
→ regenerate only when the next meaningful Gate requires it
```

- [ ] PDF는 정본이 아니라 파생 검토본이다.
- [ ] PDF에서 발견한 수정 사항은 repository canon에 반영했다.
- [ ] PDF에만 존재하는 신규 결정·수치·asset approval이 없다.
- [ ] source commit 이후 중요 정본 변경이 있다면 `STALE_DERIVED_VIEW`로 표시한다.
- [ ] AI canon과 PDF가 충돌하면 repository canon을 확인하고 PDF를 수정·재생성한다.

## 5. Render and readback verification

- [ ] PDF가 정상적으로 열리고 총 페이지 수를 확인했다.
- [ ] 모든 페이지를 렌더링해 빈 페이지, 겹침, 잘림, 깨진 글꼴·문자를 확인했다.
- [ ] 표, Flow, 이미지, 각주와 링크가 의도대로 배치됐다.
- [ ] 목차와 페이지 번호가 실제 위치와 일치한다.
- [ ] 문서 파일 크기와 이미지 품질의 균형을 확인했다.
- [ ] 다운로드 가능한 최종 파일 경로를 확인했다.

## 6. Evidence ceiling

PDF가 보여줄 수 있는 것과 없는 것을 명시한다.

```yaml
planning_canon_readback: PASS | FAIL | BLOCKED | NOT_RUN
pdf_render_readback: PASS | FAIL | BLOCKED | NOT_RUN
asset_manifest_readback: PASS | FAIL | BLOCKED | NOT_RUN
automated_tests: PASS | FAIL | BLOCKED | NOT_RUN
runtime_verification: PASS | FAIL | BLOCKED | NOT_RUN
play_ux_verification: PASS | FAIL | BLOCKED | NOT_RUN
release_readiness: PASS | FAIL | BLOCKED | NOT_RUN
```

정적 문서와 PDF render PASS는 runtime, 실제 플레이, UX 또는 출시 준비 PASS가 아니다.

## 7. Final export record

```yaml
output_path:
file_name:
sha256:
page_count:
source_commit:
render_readback_result:
reviewed_sections:
known_limits:
user_review_state:
repository_changes_from_review:
superseded_pdf:
rollback_or_regeneration_route:
```
