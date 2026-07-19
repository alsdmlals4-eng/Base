# Markdown·JSON 기획서·스킬·자산·사람용 문서 갱신 매트릭스

> 모든 L1 이상 작업은 주 책임 분야, 영향 분야, 변경 유형, 관련 기획서 ID와 최소 스킬을 선언하고 이 표로 갱신 대상을 판정한다.

## 1. 작업 시작 선언

```yaml
primary_discipline:
affected_disciplines:
change_type:
goal:
user_or_player_value:
scope:
out_of_scope:
protected_paths:
required_design_document_ids:
foundation_skills:
discipline_skills:
asset_impact:
data_impact:
publication_impact:
lifecycle_impact:
acceptance_criteria:
validation:
```

## 2. 공통 갱신 원칙

기획 내용이 바뀌면 다음 순서로 갱신한다.

```text
관련 Markdown 또는 JSON 책임 원본
→ DESIGN_DOCUMENT_REGISTRY.json 상태·경로 확인
→ 실제 코드·데이터·자산·테스트
→ DOCX·PDF·다이어그램 재생성
→ *_PUBLICATION_MANIFEST.json
→ Active Context·Roadmap·Gates
→ 관련 Skill·Learning Log
```

스킬 계약이 바뀌면:

```text
SKILL.md·Learning Log
→ SKILL_REGISTRY.json
→ 필수 PROJECT_SKILL_MAP.pdf + 선택 md/docx/assets
→ SKILL_MAP_PUBLICATION_MANIFEST.json
```

## 3. 변경 유형별 기본 갱신

| 변경 유형 | 주 책임 원본 | 영향 확인 | 공통 갱신 | 사람용 발행 영향 | 필수 증거 |
|---|---|---|---|---|---|
| 프로젝트 방향·대상 플레이어 | 프로젝트 종합·게임 디자인 | 영향 분야 | Active Context·Roadmap·Decision·Gates | 프로젝트 종합과 영향 분야 PDF·선택 파생본 | 사용자 승인 |
| 세계관·명칭·캐릭터 정사 | 설정·내러티브 | 게임·UX·아트·사운드·QA | 용어·참조·Decision | 설정·연관 분야 PDF 문구·이미지 | 참조 검색 |
| 핵심 루프·게임 규칙 | 게임 디자인 | UX·개발·QA·분석·통합검수 | Roadmap·Gates·데이터 계약 | 게임·UX·개발 PDF | 규칙 테스트·플레이 |
| 밸런스·수치 | 게임 디자인·실제 데이터 | 개발·QA·분석 | 근거·데이터 diff | 게임 디자인 PDF | 시뮬레이션·플레이테스트 |
| UI 행동·정보 구조 | UX·UI | 게임·개발·아트·QA | 화면 흐름·Asset ID | UX·게임·아트 PDF | 프로토타입·사용성 |
| 접근성 | UX·UI | 게임·개발·아트·사운드·QA | 설정·폴백·테스트 | UX·사운드·QA PDF | 키보드·색각·자막·모션 |
| 코드·Scene·데이터 구조 | 개발 | 게임·QA·프로덕션 | Active Context·기술 부채 | 개발 PDF | 자동 테스트·실행 |
| 저장·로드·호환성 | 개발 | 게임·QA·프로덕션 | 마이그레이션·릴리스 위험 | 개발·QA PDF | 저장 왕복·호환성 |
| 자산 규격·Import·피벗 | 테크니컬 아트 | 아트·개발·QA | Asset Manifest·기술 규격 | 테크니컬 아트·아트 PDF | Import·엔진 캡처 |
| 캐릭터·환경·UI 그래픽 | 아트 | 게임·UX·테크니컬 아트·QA | Visual Source·Asset Manifest | 승인 이미지 포함 PDF | 승인 자료·실제 화면 비교 |
| 애니메이션·VFX | 아트·테크니컬 아트 | 게임·개발·UX·QA | 이벤트·프레임 계약 | 관련 PDF·캡처 | 타이밍·성능·접근성 |
| BGM·SFX·음성 | 사운드 | 게임·개발·UX·QA | 이벤트 매핑·상태 | 사운드 PDF | 재생·믹싱·반복 |
| 테스트 결과·버그 등급 | QA | 영향 분야 전체 | Active Context·릴리스 게이트 | QA·통합검수 PDF | 로그·재현·수정 확인 |
| 일정·범위·예산·위험 | 프로덕션 | 영향 분야 전체 | Roadmap·Gates·Active Context | 프로덕션 PDF | 승인·의존성·근거 |
| 벤치마킹·유저리서치 | 분석·유저리서치 | 채택 대상 분야 | 출처·Decision | 분석 PDF | 관찰·해석·적용 결론 |
| 문서·구현·자산 불일치 | 통합검수 | 관련 분야 전체 | 불일치·Gate 판정 | 통합검수 PDF | JSON·실제 결과 비교 |
| 개발 게이트 변경 | 프로덕션·통합검수 | 영향 분야 전체 | Gates·Roadmap·Active Context | 영향 분야 PDF 상태 | 진입·종료 기준·증거 |
| 프로젝트 스킬 변경 | 프로젝트 허브·해당 분야 | 관련 분야 | Skill Registry·Learning Log | Skill Map PDF·Manifest·설정한 선택 파생본 | 실제 실행·피드백 |
| 기획 책임 원본 변경 | 해당 분야 | 관련 분야·통합검수 | Design Document Registry | PDF·Manifest·선택 파생본 | 원본 해시·렌더 |
| 승인 이미지 변경 | 해당 분야 | 아트·기술 아트·통합검수 | 책임 원본의 approved visuals·Asset Manifest | 관련 PDF·선택 파생본 | 이미지 해시·캡션·시각 검수 |
| 생성기 변경 | 프로젝트 허브·개발·통합검수 | 모든 활성 발행본 | Generator version | 모든 영향 PDF·Manifest·선택 파생본 | 통합 테스트·전 페이지 렌더 |
| Base 규칙 적용 | 프로젝트 허브 | 관련 분야 | BASE_RULES_VERSION·Map | 영향 발행본 | 기준 커밋·적용 차이 |
| 책임 원본·경로 변경 | 프로젝트 허브 | 참조하는 모든 분야 | 두 Registry·Map·CODEOWNERS | 관련 발행본 | 링크·검색·콜드 스타트 |
| 기존 구조 마이그레이션 | 프로젝트 허브·통합검수 | 모든 영향 분야 | Migration Audit·보존 대조 | 새 책임 원본·PDF·Manifest·선택 파생본 | 변경 전후 정보·참조 보존 |
| 현행→백업·보류·제거 후보 | 원 책임 분야 | 참조 분야 | Lifecycle Map·두 Registry | 발행본 포함 여부 | 보존·재개·제거 조건·승인 |

## 4. 이미지 변경 판정

- [ ] 기존 승인 이미지 확인
- [ ] 새 생성·교체가 명시적 범위인지 확인
- [ ] Asset ID·상태·캐노니컬 경로 확인
- [ ] 채택·비채택 요소 기록
- [ ] 콘셉트·실제 캡처 구분
- [ ] 관련 책임 원본의 승인 이미지 메타데이터 갱신
- [ ] PDF·Manifest와 선언한 선택 파생본을 재생성하거나 `STALE` 표시

## 5. 프로젝트 스킬 판정

- [ ] 공용 절차는 Foundation에 한 번만 존재
- [ ] 분야 스킬이 관련 Markdown/JSON 책임 원본·실제 경로·산출물·검증을 연결
- [ ] Trigger·비사용 조건·실패 조건 존재
- [ ] Learning Log에 결과·실패·피드백 기록
- [ ] Skill Registry 갱신
- [ ] Skill Map PDF·Manifest와 설정한 선택 Markdown/DOCX/다이어그램 재생성
- [ ] 전체 스킬이 아니라 최소 스킬만 선택 가능

## 6. 기획서 발행 판정

- [ ] JSON이 목적·Quality Bar·전체 과정·현재 상태·다음 작업을 포함
- [ ] 승인 이미지·실제 캡처·상태 캡션 포함
- [ ] DOCX·PDF를 독립 원본으로 수정하지 않음
- [ ] 자동 다이어그램 생성
- [ ] DOCX 유효성·PDF 헤더 확인
- [ ] PDF 전 페이지 렌더·빈 페이지 검사
- [ ] JSON·생성기·출력·자산 SHA-256 Manifest 갱신
- [ ] 필요 시 사람 시각 검수
- [ ] `NOT_BUILT/STALE/FAILED/CURRENT` 상태 정확

## 7. 수명주기·마이그레이션 판정

- [ ] `[백업]`은 Git 이력만으로 부족한 보존 사유 존재
- [ ] `[보류]`에 이유·재개 조건·선행 작업 존재
- [ ] `[제거 후보]`는 고유 정보·참조·복구·승인 확인
- [ ] 사용자 승인 전 대량 삭제·이동·통합 없음
- [ ] 변경 전후 보존 대조 누락 없음
- [ ] 기존 본책은 JSON 승계·발행·참조 검증 전 제거하지 않음

## 8. 작업 종료

- [ ] 실제 결과와 승인·구현·검증 상태 일치
- [ ] 관련 Markdown/JSON 책임 원본·Design/Skill/Interview Registry 최신
- [ ] 관련 Skill·Learning Log 최신
- [ ] DOCX·PDF·다이어그램·Manifest 최신
- [ ] Active Context·Roadmap·Gates·Map 최신
- [ ] 자동·수동·시각 검증과 미검증 분리
- [ ] 다음 작업·선행 조건·Handoff 기록
- [ ] 네 Governance Checker 통과
- [ ] 새 AI가 저장소만으로 작업 재개 가능
