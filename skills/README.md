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

프로젝트 교훈은 먼저 `[수정제안서]`에서 검토하고, 승인된 Base 변경만 별도 구현 PR에서 Registry·Skill·Template·Test·생성본과 함께 갱신한다.
