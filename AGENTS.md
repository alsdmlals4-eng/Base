# Base 공용 AI 작업 규칙

Base는 여러 게임 프로젝트가 공유하는 **[학습형] [공용]** 규칙·Method·Skill·Template·Case의 원본이다. 프로젝트 저장소는 Base를 그대로 복제하지 않고 자신의 세계관, 수치, 엔진, 실제 경로, 승인 자산과 구현 상태에 맞게 분화·적용·검증한다.

## 1. Base URL 호출 규칙

사용자가 다음처럼 요청하면 먼저 `START_HERE.md`를 읽는다.

> `https://github.com/alsdmlals4-eng/Base 를 전부 살펴보고 참고해서 작업해줘.`

`전부 살펴본다`는 저장소 모든 파일을 무작정 읽는 뜻이 아니다. `START_HERE.md`와 `docs/DOCUMENTATION_MAP.md`로 현재 작업에 필요한 공용 책임 원본 전체를 선별한다.

대상 프로젝트에서는 다음을 함께 확인한다.

```text
프로젝트 AGENTS.md
→ BASE_RULES_VERSION.md
→ START_HERE·Active Context·Documentation Map
→ DEVELOPMENT_GATES·PROJECT_SKILL_MAP
→ 관련 분야 본책·분야 스킬
→ Roadmap·Issue·Goal·Plan
→ 실제 코드·데이터·자산·테스트
→ 필요한 Base Method·Skill·Template·Case
```

저장소 접근 없이 실제 설치·마이그레이션·검수 완료를 주장하지 않는다.

## 2. 작업 유형 라우팅

- 새 프로젝트 또는 운영체계 미설치: `skills/installing-game-project-operating-system/SKILL.md`
- 기존 운영 프로젝트 안전 재배치: `skills/migrating-existing-game-project-structure/SKILL.md`
- 분야별 프로젝트 스킬 생성·통합·학습: `skills/evolving-project-discipline-skills/SKILL.md`
- 분야별 최신 PDF 발행·검수: `skills/publishing-discipline-bibles/SKILL.md`
- Vertical Slice: `skills/designing-vertical-slices/SKILL.md`
- 기획서 책임 구조: `skills/writing-game-design-documents/SKILL.md`
- 외부 AI 결과 검수: `skills/reviewing-external-ai-drafts/SKILL.md`
- 프로젝트 교훈 환류: `skills/promoting-project-knowledge/SKILL.md`

## 3. 우선순위

충돌 시 다음 순서를 따른다.

1. 사용자의 최신 지시
2. 프로젝트 `AGENTS.md`와 보안·엔진 규칙
3. 프로젝트 Active Context·Handoff
4. 승인된 프로젝트 본책과 현재 Issue·Goal·Plan
5. 실제 구현·데이터·테스트 증거
6. 프로젝트에 동기화된 Base 기준
7. Base 원격 원본
8. 과거 대화·초안·추정

실제 파일과 문서가 다르면 차이를 보고한다. 정상 동작 중인 사용자 변경을 임의로 되돌리지 않는다.

## 4. 역할

- 기획·조정 AI: 의도, 플레이어 가치, 대안, 영향 분야, 책임 문서, Acceptance Criteria와 검수 기준을 정리한다.
- 구현 AI: 승인된 범위에서 실제 파일을 변경하고 자동·수동 검증과 문서 갱신을 수행한다.
- 사용자: 방향, 우선순위, 제품 결정, 구현 승인과 최종 결과를 확인한다.
- GitHub: 활성 파일·이력·Issue·PR·자동 검사와 릴리스 증거를 보존한다.

기획 담당은 구현 완료를 추정하지 않고, 구현 담당은 사용자 승인 없이 제품 방향을 확장하지 않는다.

## 5. 프로젝트 지속성 계약

모든 프로젝트는 새 채팅과 새 AI가 과거 대화 없이 저장소만으로 다음을 찾을 수 있어야 한다.

- 프로젝트 목적과 핵심 플레이어 경험
- 현재 개발 단계·다음 게이트·최우선 작업
- 확정·구현·검증·미확정·보류 상태
- 변경하면 안 되는 결정과 보호 경로
- 분야별 책임 본책과 프로젝트 스킬
- 실제 코드·데이터·자산·테스트
- 승인 이미지·실제 캡처·최신 분야 PDF
- 작업 종료 갱신 대상과 Base 환류 경계

Active Context·Handoff는 위 원본을 복제하지 않고 현재 상태와 읽기 순서를 연결하는 라우터로 유지한다.

## 6. 작업 단계와 개발 게이트

모든 L1 이상 작업은 다음을 선언한다.

```yaml
primary_discipline:
affected_disciplines:
change_type:
goal:
user_or_player_value:
scope:
out_of_scope:
protected_paths:
foundation_skills:
discipline_skills:
acceptance_criteria:
validation:
```

작업 실행 게이트:

```text
Intake·Context
→ Definition of Ready
→ Planning·Approval
→ Implementation
→ Verification
→ Documentation
→ Integration·Completion
```

세부 기준은 `docs/knowledge/methods/DEVELOPMENT_GATES_METHOD.md`를 따른다.

- Ready 전에는 구현하지 않는다.
- L2 이상은 실제 저장소 조사에 근거한 Plan과 사용자 승인을 우선한다.
- 실행하지 않은 검증은 `[미검증]`으로 기록한다.
- 작업 완료와 프로젝트의 Vertical Slice·Alpha·Beta 게이트 통과를 혼동하지 않는다.

## 7. 요청 수준

- `L0`: 오탈자·명확한 형식 변경
- `L1`: 범위가 명확한 작은 수정
- `L2`: 시스템 선택·여러 파일 또는 분야 영향
- `L3`: 핵심 구조·장기 방향·대형 마이그레이션
- `L4`: 여러 프로젝트에 재사용 가능한 방법

실행 프롬프트는 `목적 → 맥락 → 경험 → 범위 → 제약 → 산출물 → 완료 기준 → 검증`을 포함한다.

## 8. 기존 프로젝트 안전 마이그레이션

기존 프로젝트는 신규 프로젝트처럼 폴더부터 생성하지 않는다.

```text
기존 내용 보존
→ 책임·참조·고유 정보 감사
→ 중복·충돌·누락 분석
→ 변경 전후 보존 대조가 포함된 제안
→ 사용자 승인
→ 승인 범위만 변경
→ 링크·스킬·PDF·콜드 스타트 검증
```

첫 단계에서 금지:

- 파일·폴더 대량 삭제·이동
- 기존 책임 문서 대규모 축약
- 여러 문서를 합친 뒤 원본 제거
- 승인 이미지·자산 제거 또는 임의 교체
- 프로젝트 용어·수치·결정 변경
- `[보류]` 폐기
- Base 구조에 맞춘 강제 개명

상세 절차는 `skills/migrating-existing-game-project-structure/SKILL.md`를 따른다.

## 9. 책임 원본·수명주기·토큰 효율

- 한 질문에는 현행 책임 원본 하나를 둔다.
- 같은 내용을 문서·스킬·PDF에 장문 복사하지 않는다.
- `v2`, `final`, `latest`, 날짜별 활성 복제본을 만들지 않는다.
- 단순 이전 버전은 Git 이력으로 보존한다.
- `[백업]`은 외부 원본·감사·승인 근거처럼 Git 이력만으로 부족할 때만 사용한다.
- `[보류]`에는 이유·재개 조건·관련 책임 원본·선행 작업을 기록한다.
- `[제거 후보]`는 고유 정보·참조·복구·사용자 승인 전 삭제하지 않는다.
- `[백업]`, `[보류]`, `[제거 후보]`, archive·hold·deprecated는 기본 읽기에서 제외한다.
- Documentation Map으로 현재 작업에 필요한 현행 문서와 스킬만 선택한다.

## 10. 분야별 프로젝트 스킬

여러 분야에서 공통 사용하는 절차는 foundation에 한 번만 둔다. 각 분야는 실제 본책·경로·산출물·검증·학습을 가진 독립 프로젝트 스킬로 분화한다.

각 스킬 필수 계약:

- 사용·비사용 조건
- 필수 입력과 먼저 읽을 원본
- foundation 의존성
- 프로젝트 고유 규칙·경로
- 절차와 산출물
- Ready·Done·검증·실패 조건
- Learning Log와 검토 트리거

학습 상태는 `관찰 → 가설 → 패턴 → 검증 → 승격 후보`를 사용한다. 한 번 성공한 방법을 즉시 공용 강제 규칙으로 만들지 않는다.

## 11. 이미지·자산 계약

- 기존 승인 이미지가 있으면 별도 지시 없이 같은 항목의 새 시안을 만들지 않는다.
- 활성 항목에는 캐노니컬 경로 하나만 사용한다.
- 콘셉트·방향 승인·제작 준비·구현·실제 화면 검증을 구분한다.
- 이미지 전체가 아니라 채택 요소와 비채택 요소를 기록한다.
- Asset ID, Visual DNA, 실제 캡처와 교체 상태를 연결한다.
- 등록만 됐고 바이너리가 없으면 `MIGRATION_PENDING`으로 표시한다.

## 12. 분야별 PDF 계약

- Markdown·구조화 데이터가 편집 가능한 책임 원본이다.
- PDF·HTML·DOCX는 책임 원본과 승인 이미지에서 생성하는 읽기 전용 파생본이다.
- 각 분야 PDF는 단순 요약이 아니라 목적, 전체 과정, 단계별 입력·산출물, 관련 스킬·게이트, 승인 이미지, 구현·검증·보류와 다음 작업을 포함한다.
- PDF를 수동으로 별도 수정하지 않는다.
- Publication Manifest와 입력 해시로 최신성을 추적한다.
- 원본 또는 승인 이미지가 바뀌면 PDF·Manifest 갱신 영향을 확인한다.
- 생성·렌더링을 검증하지 못했으면 `NOT_BUILT`, `STALE` 또는 `[미검증]`으로 표시한다.

상세 절차는 `skills/publishing-discipline-bibles/SKILL.md`를 따른다.

## 13. 구현·리팩터링

- 승인된 범위와 가장 작은 안전한 변경을 사용한다.
- 기능 추가와 대규모 리팩터링을 가능한 한 분리한다.
- 저장 형식, 공개 인터페이스, 게임 규칙, 승인 자산과 사용자 흐름을 승인 없이 바꾸지 않는다.
- 현재 동작과 회귀 검증 방법을 먼저 확보한다.
- 실패·취소·중복 입력·누락 데이터·저장·호환성을 확인한다.
- 범위 밖 개선은 별도 제안으로 분리한다.

## 14. 작업 종료·인수인계·학습 환류

작업은 다음이 끝나야 완료로 보고할 수 있다.

1. 실제 결과와 승인·구현·검증 상태를 분야 본책에 반영한다.
2. Roadmap·Development Gates·Active Context·Handoff를 갱신한다.
3. Documentation Map과 Project Skill Map의 경로를 확인한다.
4. 프로젝트 스킬과 Learning Log를 실제 결과에 맞게 갱신한다.
5. 이미지·자산·PDF Manifest와 파생본 영향을 확인한다.
6. 실행한 검증, 미검증, 남은 위험을 분리한다.
7. 이동·통합·제거 파일의 참조와 보존 대조를 확인한다.
8. 프로젝트 고유 결과와 공용 재사용 원리를 분리한다.
9. 공용 후보는 기존 Base 원본과 중복을 확인해 Method·Skill·Template·Case에 반영한다.
10. 새 AI가 10분 안에 방향·상태·다음 작업·스킬·검증을 찾는지 확인한다.
11. Base 변경 후 프로젝트 `BASE_RULES_VERSION.md` 후속 동기화를 기록한다.

## 15. Base와 프로젝트 경계

### Base — [공용]

- 반복 가능한 판단법·절차·검증 계약
- 적용 조건·실패 조건이 있는 Skill
- 공용 Template·Research·Case

### 프로젝트 — [전용]

- 세계관·캐릭터·게임 규칙·실제 수치
- 엔진·코드·데이터·자산 경로
- 승인 이미지·프롬프트·PDF
- 구현·테스트·Roadmap·Issue·Plan
- Base 공용 절차를 실제 경로에 연결한 프로젝트 스킬
- 공용화 전 관찰·가설

## 16. 로컬과 GitHub

GitHub와 로컬 파일은 자동 양방향 동기화가 아니다.

- 작업 전 원격·로컬 상태를 확인한다.
- 로컬 변경은 검증 후 commit·push한다.
- 원격 변경은 fetch·pull한다.
- 자동화는 검사와 상태 경고에 사용하고 미검증 변경의 자동 push·충돌 자동 해결은 피한다.
- Workflow 파일 존재와 Required Status Check·브랜치 보호 활성 상태를 구분한다.

## 17. 완료 보고

- 주 책임·영향 분야
- 변경 파일과 이유
- 유지한 기존 동작·결정·자산
- 실행한 검증과 결과
- 미검증·불일치·남은 위험
- 본책·게이트·스킬·Manifest·PDF 최신화
- 보존·통합·백업·보류·제거 후보
- 콜드 스타트 결과
- 프로젝트 전용으로 유지한 내용
- Base에 반영한 공용 데이터와 지식 상태
- 후속 동기화와 다음 작업

실행하지 않은 테스트나 확인하지 않은 구현·PDF·브랜치 보호를 완료로 보고하지 않는다.
