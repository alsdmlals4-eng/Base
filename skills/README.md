# Base 실행 Skill Router

이 디렉터리는 여러 게임 프로젝트에서 재사용하는 Base 공용 Skill package를 관리한다. **활성 Skill 목록과 선택 권한은 이 README가 아니라 `skills/SKILL_REGISTRY.json`이 소유한다.**

## 현재 Skill 찾기

```text
skills/SKILL_REGISTRY.json
→ trigger와 비사용 조건 대조
→ automatic-trigger-match
→ 필요한 최소 Skill·Skill Mode 선택
→ skills/<skill-id>/SKILL.md
→ 필요한 reference·script·template·test만 조건부 로드
```

- 기계 권한: `skills/SKILL_REGISTRY.json`
- 사람용 생성 목록: `docs/generated/BASE_ACTIVE_SKILLS.md`
- 통합 전 ID·호환 이름: `skills/LEGACY_SKILL_ALIASES.md`
- 실행 결과·실패·갱신 학습: `skills/SKILL_LEARNING_LOG.md`
- 채택·생성·통합 검증: `docs/AI_SKILL_ADOPTION_GUIDE.md`

Registry 정책은 `load_all_skills: false`, `default_selection: automatic-trigger-match`다. 사용자는 Skill 이름을 선언할 필요가 없으며, trigger가 일치하는 최소 package만 선택한다. 활성 Skill 수와 목록을 이 문서에 수동 복제하지 않는다.

**Skill 수 자체는 목표가 아니다.** `30개`, `40개`, `8개 이상` 같은 고정 개수·경고 임계값을 설계 품질의 대리 지표로 사용하지 않는다. 책임 중복, trigger 겹침, 사용되지 않는 mode, 과도한 context/routing 비용, 독립 input/output/authority/validation boundary의 실제 필요성으로 통합·유지·신규 생성 여부를 판단한다.

### 라우팅 정확도 기본값

Registry의 hard ceiling을 매 요청에서 채우지 않는다. `docs/knowledge/ai/SKILL_ROUTING_PRECISION_GUIDE.md`에 따라 **기본 supporting Skill budget은 1**로 운용하고, 두 번째 supporting Skill은 독립 산출물·독립 검증/권한 경계·hard guard가 실제로 필요한 경우에만 예외적으로 추가한다.

이름·description·trigger가 겹치는 후보는 동시에 실행하지 않는다. Registry metadata로 먼저 작은 후보군을 만든 뒤 동률 후보의 **Skill 본문** `Use when`·`Do not use when`·입력·산출물·검증 경계를 비교해 한 owner로 좁힌다. 기능적으로 같은 책임이 반복되면 새 Skill 추가보다 `REUSE / ABSORB / MERGE`를 우선한다.

## 안정 도메인 진입점

전체 활성 목록은 생성 뷰를 따르되, 사람이 자주 찾는 통합 책임은 안정 라우트로 유지한다.

- 게임 UX/UI 설계·정보 구조·접근성·Godot UI 계약·폴리싱·구현 결과 감사: `auditing-and-refining-ui-art`

## Package 배치

```text
skills/<skill-id>/SKILL.md       필수 실행 계약
skills/<skill-id>/references/    조건부 상세 근거·프로토콜
skills/<skill-id>/scripts/       반복 가능한 검사·보조 실행
skills/<skill-id>/agents/        지원 플랫폼용 발견 metadata
```

공용 자료의 역할별 위치:

- 통합 운영·정책: `docs/`
- 반복 가능한 Method·Guide·Case: `docs/knowledge/`
- 복사 가능한 출력 계약: `templates/`
- 정적·회귀 검증: `tests/`, `tools/`, `.github/workflows/`
- 프로젝트발 공용화 후보: `[수정제안서]/`

## 생성·변경·통합 규칙

1. 먼저 기존 활성 Skill의 Skill Mode로 처리 가능한지 확인한다.
2. 독립 입력·산출물·권한·실패 조건·검증 경계가 있을 때만 새 Skill을 만든다.
3. `SKILL.md` frontmatter의 `name`과 Registry `skill_id`·경로를 일치시킨다.
4. positive trigger, negative trigger, owner, input, output, failure, verification, next step을 Registry와 본문에 연결한다.
5. reference·script·agent metadata는 활성 package 안에 두고 실제 소비 경로를 검증한다.
6. 통합·이름·경로 변경 시 이전 ID는 `skills/LEGACY_SKILL_ALIASES.md`에 연결하고 활성 문서·Template·Test·생성본의 stale 참조를 검사한다.
7. 외부 모델·플러그인 이름은 교체 가능하게 유지하며, 핵심 절차와 검증 계약은 특정 도구가 없어도 이해할 수 있어야 한다.
8. 사용자 승인 전 프로젝트 고유 규칙을 Base 공용 강제 규칙으로 승격하지 않는다.

## 금지

- 전체 `skills/` 기본 로드
- README의 수동 활성 Skill 표를 두 번째 권한으로 사용
- Legacy ID를 새 문서·Registry의 현행 실행 ID로 사용
- Registry에 없는 `SKILL.md` package 또는 `SKILL.md`가 없는 활성 package 유지
- reference·script·agent metadata를 소비자·replacement·rollback 없이 방치
- 파일 수나 길이만을 이유로 안전 규칙·고유 절차·검증 근거 삭제
- Skill 개수 자체를 맞추기 위한 통합·분할·신규 생성

프로젝트 교훈은 먼저 `[수정제안서]`에서 검토하고, 승인된 Base 변경만 별도 구현 PR에서 Registry·Skill·Template·Test·생성본과 함께 갱신한다.

외부 시각 도구는 `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`의 Artifact·정본 경계를 따라 기존 책임 Skill에서 사용한다.

## Base v9.4 AI 운영 진입점

- 모델·추론 단계·Prompt caching·비용 추정·실측 재보정: `optimizing-ai-model-and-prompt-costs`
- 지시 권위·Interface-first Prompt·Context 큐레이션·Artifact 주장 상한: `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`
- 게임 UI 모션·중단·반복·Reduced Motion·도메인 상태 권위: `auditing-and-refining-ui-art` → `references/ui-motion-and-interaction-principles.md`

Luna / Terra / Sol은 논리적 작업 등급이며 실제 provider 옵션의 존재를 보장하지 않는다. BCP-2026-004는 새 활성 Skill을 만들지 않고 기존 intake·simplifying·UI Skill의 책임으로 유지한다.
## BCP-008 선택형 확장

새 활성 Skill을 만들지 않고 기존 책임 안에서만 다음을 선택적으로 사용한다.

- L2 이상 기능은 `FEATURE_SPEC_TRACEABILITY_PACKET.md`로 Decision·Requirement·Acceptance·Task·구현·검증 ID를 연결한다. L0·L1에는 강제하지 않는다.
- 복합 변경의 적대 검토는 `cross-discipline-review-lenses.md`를 필요한 관점만 선택해 사용하며, Lens는 결정을 소유하지 않는다.
- 프로젝트 `DESIGN.md`는 시각 토큰만 소유하고 플레이어 경험·행동·접근성 권위는 `GAME_UX_UI_SYSTEM.md`에 남긴다.
- 외부 Web UI Registry·MCP·컴포넌트 코드는 연결 성공과 조달 승인, 설치, 빌드, 렌더, 접근성, 프로젝트 채택을 분리해 fail-closed로 검증한다.

실제 독립 모델 행동 결과가 없으면 행동 성능은 `NOT_RUN`, 실제 프로젝트 설치·렌더·사람 검증이 없으면 조달 채택은 `BLOCKED_UNVERIFIED`다.
