# BCP-2026-008 — 에이전트 명세·디자인·외부 UI 조달 책임의 선택적 통합

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base`
- 기준 커밋: `c7e678c928d08e736694319184f090ee87009efc`
- 제출일: `2026-08-06`
- 상태: `SUBMITTED`
- 지식 상태: `패턴`
- 제안 작성 승인: `2026-08-06 사용자 메시지 "진행해"`
- 구현 승인 근거: `미승인`

## 관찰과 증거

사용자가 제시한 Superpowers, Spec Kit, BMAD, DESIGN.md, shadcn/ui MCP, taste-skill, getdesign.md를 공식 저장소·공식 문서와 Base 현행 책임 원본에 대조했다. 상세 조사와 출처는 `evidence/EXTERNAL_TOOL_RESEARCH.md`, Base 중복·공백 판정은 `evidence/BASE_GAP_AND_BOUNDARY_ANALYSIS.md`에 기록한다.

Base에는 이미 다음 책임이 존재한다.

1. `managing-project-intake-and-work-contract`: 사용자 의도·사실 조사·실행 계약·Grill Me·작업 분해·순서화
2. `managing-design-documents`: 단일 책임 원본·Decision·문서 생명주기·발행
3. `running-adversarial-review-and-refinement`: 공격·비판 검증·승인 finding 최소 수정·회귀 재검사
4. `reviewing-and-validating-project-changes`: 계약·정적·런타임·접근성·성능·회귀 증거
5. `auditing-and-refining-ui-art`: 경험·정보 구조·디자인 시스템·Godot UI·접근성·폴리싱·렌더 감사
6. `evolving-project-discipline-skills`: consolidation-first Skill 경계 판단과 행동 평가

따라서 외부 프레임워크를 각각 새 활성 Skill로 복제하면 주 책임 분야 하나 원칙, 단일 정본, 최소 Skill 로딩, 제안/구현 분리와 충돌한다. 반면 다음 네 공백은 기존 책임을 보강할 가치가 있다.

- L2 이상에서 `Decision → Requirement → Acceptance → Task → Implementation → Verification`을 동일 ID로 대조하는 명세 추적성 패킷
- BMAD의 Named Agent를 복제하지 않고 제품·UX·아키텍처·구현·QA·문서 관점으로 공격하는 교차 분야 검토 Lens
- 프로젝트별 시각 토큰과 근거를 기계 판독 가능한 선택형 `DESIGN.md`로 관리하는 Adapter
- shadcn Registry·MCP 등 외부 코드 조달과 taste-skill/getdesign 계열 참고 자료를 출처·라이선스·보안·접근성·anti-generic 검수로 제한하는 Gate

## 일반화 후보

### 1. 신규 활성 Skill 없이 기존 책임에 흡수한다

```yaml
new_active_skill: false
registry_change_expected: false
integration_owners:
  traceability:
    - managing-project-intake-and-work-contract
    - managing-design-documents
    - reviewing-and-validating-project-changes
  cross_discipline_review:
    - running-adversarial-review-and-refinement
  design_md_adapter:
    - auditing-and-refining-ui-art
  external_ui_procurement:
    - auditing-and-refining-ui-art
```

독립 입력·산출물·권한·검증 경계가 실제 Pilot에서 증명되지 않는 한 새 Skill을 만들지 않는다. 구현 중 예상과 달리 독립 경계가 발견되면 같은 구현 PR에서 임의로 Registry를 변경하지 않고 후속 BCP로 분리한다.

### 2. L2 이상 명세 추적성 패킷

```text
Decision ID
→ Requirement ID
→ Acceptance Criteria ID
→ Task ID
→ Implementation Path
→ Verification ID
→ CONVERGED / GAP / BLOCKED_UNVERIFIED
```

작은 L0·L1 변경에는 강제하지 않는다. 기존 Decision·Issue·Plan·책임 원본을 대체하는 별도 정본이 아니라, 서로 다른 산출물 사이의 연결과 누락을 검사하는 얇은 Packet으로 둔다.

### 3. 교차 분야 검토 Lens

```text
제품·플레이어 가치
UX·접근성
아키텍처·상태 소유권
구현·성능·플랫폼
QA·회귀·출시
문서·추적성·인수인계
```

Lens는 결정을 소유하거나 독립 정본을 만들지 않는다. 각 Finding은 증거, 영향 Requirement, severity, 제안, 기존 owner Skill을 기록하고 기존 적대적 검토 상태 모델로 통합한다.

### 4. 프로젝트 선택형 DESIGN.md Adapter

```text
GAME_UX_UI_SYSTEM
→ 경험·흐름·정보·입력·상태·접근성·Godot 소유권

프로젝트 DESIGN.md
→ 색·타이포그래피·간격·형태·깊이·시각 컴포넌트 토큰·Do/Don't
```

`DESIGN.md`는 Base 루트 공용 브랜드 파일이 아니라 각 프로젝트가 선택적으로 설치하는 시각 언어 원본이다. Google Labs 형식이 현재 `alpha`이므로 `format_version`, `source_commit_or_release`, `last_verified_at`, 변환 대상과 검증 상태를 명시한다.

### 5. 외부 UI 조달·anti-generic Gate

```text
요구·기존 시스템 조사
→ 출처·버전·commit·hash·license
→ 파일·dependency·권한·shell·secret 영향
→ 기존 코드와 겹침·교체 범위
→ 접근성·런타임·플랫폼 적합성
→ 프로젝트 DESIGN.md·UX 계약에 맞춘 변환
→ 실제 렌더·입력·회귀
→ 승인·롤백
```

shadcn MCP 연결이나 Registry 검색 성공은 설치 승인 또는 품질 통과가 아니다. taste-skill의 고정 취향·특정 Web stack 선호는 공용 규칙으로 복제하지 않고, Design Read·밀도·모션·반복 패턴·실제 렌더 preflight만 프로젝트 의도 기반 Lens로 변환한다.

## 프로젝트 전용으로 남길 내용

- 프로젝트별 색·폰트·간격·radius·elevation·모션 값
- 실제 Godot Theme·Scene·Resource 또는 Web CSS·컴포넌트 경로
- 채택한 외부 Registry·컴포넌트·정확한 버전·라이선스·hash
- 브랜드·장르·플레이어·플랫폼에 따른 Design Read와 예외
- 프로젝트별 Requirement·Task·검증 ID
- 실제 렌더·실기기·사람 이해·접근성·성능 결과
- 유명 브랜드의 로고·상표·사진·고유 일러스트·저작물

## 적용 조건과 비사용 조건

### 적용

- L2 이상 기능에서 요구·작업·구현·검증이 여러 파일이나 산출물에 분산된다.
- 다분야 작업에서 한 관점만으로 중요한 실패를 놓칠 가능성이 높다.
- 프로젝트에 반복 사용되는 시각 토큰·컴포넌트 규칙이 존재한다.
- 외부 UI Registry·MCP·코드 Template·브랜드 참고 자료를 도입하려 한다.
- 구현 결과가 기능적으로 동작하지만 generic AI 패턴·시각 drift·접근성 회귀 위험이 있다.

### 비사용

- L0 오탈자나 단일 기계 수정에 추적성 Packet을 강제한다.
- 여러 Named Agent가 같은 결정을 독립적으로 소유하게 한다.
- `DESIGN.md`가 UX 흐름·상태 소유권·게임 규칙을 대체한다.
- Base 루트에 모든 프로젝트가 공유할 단일 시각 브랜드를 고정한다.
- shadcn/ui 또는 외부 Registry를 Godot UI 구현으로 오인한다.
- taste-skill의 특정 폰트·아이콘·Tailwind·React 선호를 Base 전역 규칙으로 복사한다.
- getdesign.md 분석을 해당 브랜드의 공식 Design System으로 표시하거나 고유 자산을 복제한다.
- 외부 Workflow가 실행할 shell·network·secret 접근을 검토하지 않고 자동 실행한다.

## 반례와 위험

1. **문서 과잉**: L2 이상에만 Packet을 적용하고 작은 작업은 기존 계약 Section에서 끝낸다.
2. **이중 정본**: Packet은 연결표이고 분야 상세는 기존 책임 원본만 소유한다.
3. **역할 분산**: Lens는 Finding만 생산하며 결정·수정은 기존 owner와 사용자 승인에 남긴다.
4. **alpha 형식 drift**: DESIGN.md 형식을 exact release 또는 commit으로 고정하고 자동 갱신하지 않는다.
5. **공급망 위험**: Registry·MCP에서 받은 파일·dependency·script·secret 요구를 설치 전에 읽고 기록한다.
6. **라이선스 혼동**: 도구 라이선스와 Registry item·폰트·아이콘·브랜드 자산 라이선스를 별도로 검증한다.
7. **미감의 규칙화**: anti-generic Finding은 프로젝트 의도·접근성·실제 렌더 증거가 없으면 취향으로 기각한다.
8. **Web 편향**: Godot와 Web Adapter를 분리하고 외부 컴포넌트 코드를 엔진 중립 원리로 과장하지 않는다.
9. **검증 과장**: 문서 lint·Schema 통과를 런타임·사람 이해·실기기 통과로 승격하지 않는다.
10. **기존 BCP 중복**: BCP-2026-004의 지시·컨텍스트·UI 모션 책임을 대체하지 않고 명세 추적성·시각 토큰·외부 조달 경계만 추가한다.

## 영향 범위와 검증

### 승인 후 예상 구현 영향

- `skills/managing-project-intake-and-work-contract/SKILL.md`
- `skills/managing-design-documents/SKILL.md`
- `skills/reviewing-and-validating-project-changes/SKILL.md`
- `skills/running-adversarial-review-and-refinement/SKILL.md`
- `skills/running-adversarial-review-and-refinement/references/cross-discipline-review-lenses.md`
- `skills/auditing-and-refining-ui-art/SKILL.md`
- `skills/auditing-and-refining-ui-art/references/design-md-project-adapter.md`
- `skills/auditing-and-refining-ui-art/references/external-ui-procurement-and-anti-generic-quality.md`
- `templates/planning/FEATURE_SPEC_TRACEABILITY_PACKET.md`
- `templates/planning/PROJECT_DESIGN_MD_TEMPLATE.md`
- 관련 Documentation Map·Learning Log·focused test·reference freshness 소비자

### 필수 검증

- 새 활성 Skill 0개와 `skills/SKILL_REGISTRY.json` byte-identical 확인
- L0/L1 non-selection과 L2/L3 selection 사례
- Packet이 별도 정본으로 승격되지 않는지 검사
- Lens Finding이 기존 owner로 라우팅되는지 검사
- DESIGN.md와 GAME_UX_UI_SYSTEM 책임 충돌 검사
- alpha version·source identity·provenance 누락 fail-closed
- 외부 Registry의 license·hash·dependency·script·secret·rollback 필드 검사
- Godot/Web 경계와 실제 렌더·입력·접근성 증거 상한 검사
- `git diff --check`, focused pytest, reference freshness, full Python suite
- 실행하지 않은 외부 MCP·Registry 설치·런타임·사람 검증은 `NOT_RUN`

## 필요한 도구·파일·권한

- 필요 항목: GitHub Branch·PR·Actions, Python 검증 환경, 공식 문서 Web 조회
- 필요한 이유: 제안/구현 분리, 출처 검증, Schema·문서·회귀 검사
- 설치·적용 방법: 제안 단계에는 외부 CLI·MCP를 설치하지 않는다. 승인 구현 Pilot에서 필요한 경우 exact version과 최소 권한을 별도 기록한다.
- 설치 후 확인 명령: 구현 계획의 각 Task와 해당 PR에서 확정한다.
- 최소 권한: Base contents·pull requests 쓰기; 외부 Registry는 기본 읽기 전용
- 현재 실행 상태: 외부 MCP·Spec Kit CLI·BMAD installer·DESIGN.md CLI·taste-skill 설치 `NOT_RUN`

## 승인과 구현

- 사용자 승인 근거: `미승인`
- 현재 단계: 제안 전용 Draft PR
- 구현 PR: `없음`
- 승인 전 금지: 활성 Skill·Reference·Template·Tool·Schema·Test·Registry 변경
- 승인 조건: 이 제안의 네 책임 경계, 비사용 조건, 예상 영향, 검증·롤백을 사용자가 명시적으로 승인
- 구현 방식: 최신 main에서 새 격리 Branch를 만들고 `IMPLEMENTATION_PLAN.md`의 TDD 순서로 별도 Draft PR 작성
- 롤백: 제안 PR을 닫거나 되돌리고 Registry 항목을 제거한다. 활성 Base 파일은 이 제안 PR에서 변경하지 않는다.
