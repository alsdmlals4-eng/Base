# BCP-2026-001 — Base 공용 Skill Registry의 선택적 사람용 Map 발행

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base`
- 기준 커밋: `bc0eadca1c5c73ee4d5afd907d620953dbe02590`
- 상태: `SUBMITTED`
- 지식 상태: `관찰`

## 관찰과 증거

프로젝트용 Skill Registry에는 PDF·선택 Markdown/DOCX Map 발행 계약이 있으나 Base 공용 `skills/SKILL_REGISTRY.json`에는 기계 판독 Registry만 있다. AI 라우팅에는 충분하지만 사람이 Base 스킬 책임과 관계를 한눈에 보는 선택 파생본은 없다.

## 일반화 후보

Base Registry에서 사람이 보는 선택 Markdown 또는 PDF Map을 결정적으로 생성하는 기능을 검토한다. Registry는 계속 유일한 책임 원본이어야 한다.

## 적용 조건과 비사용 조건

- 적용: 스킬 수·관계가 늘어 사람이 Registry를 직접 읽기 어려워졌다는 실제 피드백이 반복될 때
- 비사용: 현재 Registry와 Documentation Map만으로 탐색이 충분하거나 발행 유지비가 편익보다 클 때

## 반례와 위험

- 프로젝트용 생성기를 Base에 그대로 재사용하면 불필요한 DOCX/PDF 동기화 비용이 생길 수 있다.
- 사람용 Map이 책임 원본처럼 수동 수정되면 Registry와 충돌한다.

## 영향 범위와 검증

- 예상 영향: `skills/SKILL_REGISTRY.json`, 선택 생성기, Documentation Map, 회귀 테스트
- 검증: 동일 입력 결정성, 수동 변조 탐지, Registry와 생성본 링크·해시 일치
- 롤백: 선택 발행 설정과 생성본만 제거하고 Registry를 유지

## 승인과 구현

- 사용자 승인 근거: `미승인`
- 구현 PR: `없음`
