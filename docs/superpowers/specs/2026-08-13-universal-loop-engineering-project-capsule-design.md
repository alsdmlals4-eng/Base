# Universal Loop Engineering + Project Execution Capsule Design

Tracking issue: `#321`.

Status: `USER_APPROVED_CONCEPT / WRITTEN_AWAITING_USER_REVIEW / IMPLEMENTATION_NOT_STARTED`.

Base는 하나의 공용 Loop Kernel과 프로젝트별 선언형 Execution Capsule을 사용한다. 기획과 아트 디자인은 Planning Lock·Visual Lock으로 보호하고, 승인 요구사항은 작업·변경·테스트·검증 근거까지 추적한다. Figma는 선택형 Visual provider이며 A3 자동 병합과 Scheduler는 기본 비활성이다.

세부 설계는 같은 이름의 하위 디렉터리 `2026-08-13-universal-loop-engineering-project-capsule/`에서 책임별로 분리한다. 읽기 순서는 `01-goal-and-authority.md`부터 `10-state-and-evidence.md`까지다.

구축 순서: Base #314 → 계약 Schema → 결정론적 Kernel → Capability → Blacksmith 이전 → 서사·데이터 Pilot → 시각·UI Pilot → Multi-Agent/A3/Scheduler 검토.

사용자 검토 후에만 구현 계획으로 전환한다.
