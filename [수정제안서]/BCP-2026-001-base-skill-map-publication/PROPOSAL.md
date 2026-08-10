# BCP-2026-001 — Base 공용 Skill Registry의 선택적 사람용 Map 발행

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base`
- 기준 커밋: `bc0eadca1c5c73ee4d5afd907d620953dbe02590`
- 상태: `IMPLEMENTED`
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

- 사용자 승인 근거: 2026-08-10 KST 대화 지시 `좋아 다 승인할게 [연속작업] 진행해`
- 안정적 승인 참조: `[수정제안서]/BCP-2026-001-base-skill-map-publication/PROPOSAL.md#승인과-구현`
- 승인된 최소 구현: Registry를 유일한 정본으로 유지하는 결정적 Markdown Map 생성·검증·Documentation Map 연결. PDF·DOCX·수동 편집 Map·새 ACTIVE Skill은 제외한다.
- 구현 PR: [#264](https://github.com/alsdmlals4-eng/Base/pull/264)

### 구현 closeout — PR #264

- 병합 커밋: `381b66bc3619caf7994b0073108fdcba23b30e96`
- 실제 반영: Registry를 유일한 라우팅 정본으로 유지하는 결정적 Markdown Skill Map 생성·검증, README·Documentation Map 연결, 생성기 회귀 검사를 반영했다.
- 검증 근거: PR #264의 focused registry generator tests, `python tools/build_base_v9_artifacts.py --check`, canonical reference freshness가 성공했다.
- 검증 한계: 실제 프로젝트별 Skill 선택 품질·사람 사용성·런타임 설치 검증은 이 Base 문서 closeout의 범위가 아니다.
