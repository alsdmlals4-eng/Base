# BCP-2026-003 — 활성 Skill 수와 목록의 Registry 단일 권한화

## 상태

`SUBMITTED`

승인 전에는 활성 Base 문서·Skill·Test를 변경하지 않는다.

## 출처

- 출처 프로젝트: `alsdmlals4-eng/urban-legend`
- 출처 브랜치: `agent/skill-contract-hardening-20260723`
- 출처 커밋: `5cf92312b53d49d3c2dec38d70c174fc40d4c7ed`
- Base 기준 커밋: `41a20584dd2ee51d917e5c9d7cab6838e1ceba7e`
- 관찰일: 2026-07-23

## 관찰된 문제

Base의 `skills/SKILL_REGISTRY.json`과 `README.md`는 활성 Skill을 25개로 정의한다. 그러나 항상 적용되는 `AGENTS.md`와 단일 운영 모델인 `docs/OPERATING_MODEL.md`의 활성 Skill 표는 13개만 나열하고, 본문에서도 활성 Skill이 13개라고 서술한다.

이 불일치는 다음 실패를 만들 수 있다.

1. 새 프로젝트가 최상위 문서만 읽으면 최신 12개 Skill을 존재하지 않는 것으로 판단한다.
2. 프로젝트가 Registry 25개를 고정해도 Base 설명 원본을 다시 읽을 때 서로 다른 라우팅 결과가 나온다.
3. 활성 Skill 추가·통합 뒤 Registry는 갱신됐지만 사람용 강제 문서의 개수와 목록이 오래된 상태로 남아도 현재 회귀 테스트가 차단하지 못한다.

## 공용화 가능한 원리

활성 Skill의 ID·개수·상태는 `skills/SKILL_REGISTRY.json` 하나가 기계 권한을 가져야 한다. `AGENTS.md`, `README.md`, `docs/OPERATING_MODEL.md`, `docs/DOCUMENTATION_MAP.md`는 역할과 선택 정책을 설명하되 전체 목록과 개수를 독립적으로 유지하지 않거나, 유지하는 경우 Registry와 자동 대조해야 한다.

## 제안 범위

승인 후 별도 구현 PR에서 다음 최소 변경을 검토한다.

1. `AGENTS.md`의 13개 활성 Skill 표와 개수 문구를 최신 Registry와 일치시키거나 Registry·Documentation Map으로 위임한다.
2. `docs/OPERATING_MODEL.md`의 13개 Skill 표와 개수 의미를 최신 Registry와 일치시키거나 책임별 요약으로 축소한다.
3. 활성 Skill 개수·ID·상태를 여러 강제 문서가 독립 원본으로 소유하지 않도록 책임을 명시한다.
4. Registry의 활성 ID 집합과 사람용 문서의 선언이 충돌하면 실패하는 회귀 테스트를 추가한다.
5. 향후 Skill 추가·통합 시 Registry·Documentation Map·Alias·Learning Log·진입 문서의 전파 검사를 유지한다.

## 제외 범위

- 25개 Skill의 책임·mode·trigger 자체 변경
- 프로젝트 분야 Skill 또는 프로젝트 고유 경로 변경
- Skill 수를 줄이기 위한 통합
- 승인되지 않은 Base 활성 문서 즉시 수정
- `urban-legend`의 세계관·수치·저장·코드·데이터 복사

## 반례와 대안

### 대안 A — 모든 문서에 25개 목록 복제

읽기 편의는 높지만 다음 통합 때 같은 drift가 반복될 가능성이 크다. 자동 생성 또는 회귀 테스트 없이는 권장하지 않는다.

### 대안 B — 최상위 문서에서 개수와 전체 목록 제거

Registry와 Documentation Map으로 단일 권한을 만들기 쉬운 방식이다. 다만 새 사용자의 발견성이 떨어지지 않도록 책임별 대표 링크와 읽기 순서는 유지해야 한다.

### 대안 C — 사람용 Map 자동 생성

장기적으로 가장 강하지만 생성기·파생본·검증 계약이 추가된다. 기존 `BCP-2026-001-base-skill-map-publication`과 중복 여부를 먼저 검토해야 한다.

## 권장안

`AGENTS.md`와 `docs/OPERATING_MODEL.md`는 전체 활성 목록의 독립 원본 역할을 내려놓고 Registry·Documentation Map을 연결한다. 사람이 필요한 책임 요약만 유지하며, 개수나 ID를 적는 경우 자동 회귀 테스트로 Registry와 대조한다.

## 검증 계획

승인된 구현 PR에서 다음을 실행한다.

```text
python -m unittest tests/test_base_operating_system.py
python tools/check_skill_package_integrity.py
python tools/check_skill_coverage.py
python tools/check_reference_freshness.py
```

실제 저장소의 정확한 테스트·도구 경로는 구현 전 Base `tests/`, `tools/`, Actions를 다시 감사해 확정한다. 실행하지 않은 검사는 `NOT_RUN`으로 기록한다.

## 롤백

- 사람용 문서 변경은 단일 커밋 또는 독립 커밋으로 분리한다.
- 회귀 테스트가 기존 의도적 요약을 잘못 차단하면 테스트와 문서 역할을 함께 원복한다.
- Registry 자체는 이 제안의 구현 범위에서 변경하지 않는다.

## 프로젝트 전용으로 남기는 내용

- 괴이 기록국의 10개 프로젝트 분야 Skill
- 사건 작성 로컬 Skill
- 오디오→UX 인수인계 경계
- 프로젝트 파일 경로·저장 Schema·실제 검증 결과

## 승인 상태

- `approval_ref`: 없음
- 구현 권한: 없음
- 다음 상태 후보: `UNDER_REVIEW`
