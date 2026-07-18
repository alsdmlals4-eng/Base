# 문서·스킬·자산·PDF 갱신 매트릭스

> 모든 L1 이상 작업은 `주 책임 분야`, `영향 분야`, `변경 유형`, `foundation 스킬`, `분야 스킬`을 먼저 선언하고 이 표로 필수 갱신 대상을 판정한다.

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
required_docs:
foundation_skills:
discipline_skills:
asset_impact:
data_impact:
pdf_impact:
lifecycle_impact:
acceptance_criteria:
validation:
```

## 2. 변경 유형별 기본 갱신

| 변경 유형 | 주 책임 본책 | 필수 영향 확인 | 공통 갱신 | 프로젝트 스킬·PDF 영향 | 필수 증거 |
|---|---|---|---|---|---|
| 프로젝트 방향·대상 플레이어 | 프로젝트 허브·게임 디자인 | 모든 분야 | 방향서, Active Context, Roadmap, Decision Log, Changelog, Development Gates | 영향 분야 스킬의 목적·Quality Bar; 모든 분야 PDF 요약·상태 | 사용자 승인 |
| 세계관·명칭·캐릭터 정사 | 설정·내러티브 | 게임, UX, 아트, 사운드, QA | Documentation Map, Changelog | 설정·내러티브 스킬; 관련 PDF 문구·이미지 캡션 | 용어·참조 검색 |
| 핵심 루프·게임 규칙 | 게임 디자인 | UX, 개발, QA, 분석, 통합검수 | Active Context, Roadmap, Gates, Changelog | 게임 디자인·검증 스킬; 게임·UX·개발 PDF | 규칙 명세·테스트 계획 |
| 밸런스·수치 | 게임 디자인 | 개발, QA, 분석 | 데이터 원본, Decision Log 또는 근거 | 밸런스 스킬·Learning Log; 게임 PDF 데이터 기준 | 데이터 diff·시뮬레이션·플레이테스트 |
| UI 행동·정보 구조 | UX·UI·접근성 | 게임, 개발, 아트, QA, 통합검수 | 화면 흐름, Active Context | UX 스킬; UX·게임·아트 PDF와 승인 이미지 | 프로토타입·사용성 검증 |
| 접근성 | UX·UI·접근성 | 게임, 개발, 아트, 사운드, QA | 관련 설정·폴백·테스트 | 접근성 스킬; UX·사운드·QA PDF | 키보드·색각·자막·모션 검증 |
| 코드·Scene·데이터 구조 | 개발·엔지니어링 | 게임, QA, 프로덕션 | 개발 본책, Active Context, 기술 부채 | 개발 스킬·Learning Log; 개발 PDF·실제 경로 | 자동 테스트·실행 결과 |
| AI·전투·결정론 | 개발·엔지니어링 | 게임, QA, 분석 | 데이터·아키텍처·테스트 명세 | 개발·게임·QA 스킬; 관련 PDF | 재현 시드·회귀 테스트 |
| 저장·로드·호환성 | 개발·엔지니어링 | 게임, QA, 프로덕션 | 마이그레이션·릴리스 위험 | 개발·QA 스킬; 개발·QA PDF | 저장 왕복·구버전 호환 |
| 자산 규격·Import·피벗 | 테크니컬 아트 | 아트, 개발, QA | Asset Manifest, 기술 규격 | 테크니컬 아트 스킬; 기술 아트·아트 PDF | Import 결과·엔진 캡처 |
| 캐릭터·환경·건물·UI 그래픽 | 아트 | 게임, UX, 테크니컬 아트, QA | Visual Source, Asset Manifest | 아트 스킬·Learning Log; 승인 이미지 포함 PDF 재생성 | 승인 이미지·실제 화면 비교 |
| 애니메이션·VFX | 아트·테크니컬 아트 | 게임, 개발, UX, QA | 이벤트·프레임 계약 | 아트·테크니컬 아트 스킬; PDF·캡처 | 판정 타이밍·성능·접근성 |
| BGM·SFX·음성 | 사운드 | 게임, 개발, UX, QA | 이벤트 매핑·오디오 상태 | 사운드 스킬; 사운드 PDF | 실제 재생·믹싱·반복 검증 |
| 테스트 결과·버그 등급 | QA | 영향 분야 전체 | Active Context, 릴리스 게이트 | QA·통합검수 스킬; QA PDF | 로그·재현·수정 확인 |
| 일정·범위·예산·위험 | 프로덕션·PM | 영향 분야 전체 | Roadmap, Gates, Active Context, Changelog | 프로덕션 스킬; 프로덕션 PDF | 승인·의존성·근거; 미정 수치 금지 |
| 벤치마킹·SWOT·유저리서치 | 분석·유저리서치 | 채택 대상 분야 | 조사 보고서; 채택 시 Decision Log·본책 | 분석 스킬·Learning Log; 분석 PDF | 출처·관찰·해석·적용 결론 |
| 문서·구현·자산 불일치 | 통합검수 | 관련 분야 전체 | 불일치 기록, Active Context, Gate 판정 | 통합검수 스킬; 통합검수 PDF | 책임 원본·실제 결과 비교 |
| 개발 게이트 변경 | 프로젝트 허브·프로덕션·통합검수 | 영향 분야 전체 | Development Gates, Roadmap, Active Context | foundation gate 스킬; 모든 영향 분야 PDF 상태 | 진입·종료 기준과 증거 |
| 프로젝트 스킬 변경 | 프로젝트 허브·해당 분야 | 관련 분야 | Project Skill Map, 본책, Active Context | Skill·Learning Log; PDF의 관련 스킬 섹션 | 실제 실행·검증·피드백 |
| 분야 PDF 원본·승인 이미지 변경 | 해당 분야 | 프로젝트 허브·통합검수 | Publication Manifest, Changelog | publishing skill; PDF 재생성·시각 검수 | 입력 해시·PDF 헤더·렌더링 |
| Base 규칙·스킬 적용 | 프로젝트 허브 | 관련 분야 | BASE_RULES_VERSION, Changelog, Documentation Map | Project Skill Map·프로젝트 스킬 확장; PDF 공용 기준 | 기준 커밋·적용 차이 |
| 책임 원본·경로 변경 | 프로젝트 허브 | 참조하는 모든 분야 | Documentation Map, README, 링크, 자동 검사 설정 | Project Skill Map·PDF Manifest·CODEOWNERS | 링크·검색·콜드 스타트 |
| 기존 프로젝트 구조 마이그레이션 | 프로젝트 허브·통합검수 | 모든 영향 분야 | Migration Audit, 보존 대조, Documentation Map, Changelog | 모든 이동 분야 스킬·PDF·Manifest | 변경 전후 정보·참조 보존 |
| 현행→백업·보류·제거 후보 변경 | 프로젝트 허브·원 책임 분야 | 참조 분야 | Lifecycle Map, Documentation Map, Changelog | 스킬 지도·PDF 포함 여부 | 보존 이유·재개/제거 조건·승인 |

## 3. 이미지 변경 추가 판정

- [ ] 기존 승인 이미지가 있는지 확인했다.
- [ ] 새 시안 생성이 명시적 요청 또는 교체 승인 범위인가?
- [ ] 이미지 전체가 아니라 채택·비채택 요소를 기록했다.
- [ ] 캐노니컬 경로를 유지하거나 변경 근거를 기록했다.
- [ ] Asset Manifest 상태와 실제 파일 존재가 일치한다.
- [ ] Visual DNA가 갱신됐다.
- [ ] 콘셉트와 실제 캡처·골든 스크린샷을 구분했다.
- [ ] 영향 분야 PDF와 Publication Manifest를 갱신했거나 `STALE`로 표시했다.

## 4. 개발 게이트 추가 판정

### 작업 실행 게이트

- [ ] Intake·Context
- [ ] Definition of Ready
- [ ] Planning·Approval
- [ ] Implementation
- [ ] Verification
- [ ] Documentation
- [ ] Integration·Completion

### 제품 단계

| 게이트 변경 | 필수 확인 |
|---|---|
| Concept | 대상 플레이어, 핵심 약속, 금지 방향 |
| Prototype | 가설, 폐기 가능 범위, 관찰 기준 |
| Graybox | 공간·동선·규칙·가독성 |
| First Playable | 핵심 루프의 처음부터 끝까지 연결 |
| Vertical Slice | 목표 품질, 대표 경험, 아트·사운드·UX·제작 파이프라인 |
| Production | 파이프라인 처리량, 자산 예산, 일정·비용 위험 |
| Alpha | 주요 기능 연결, 전체 진행, 저장·복귀 |
| Feature Complete | 계획 기능 누락, 범위 고정 |
| Content Complete | 출시 콘텐츠·현지화·자산 상태 |
| Beta | 회귀·성능·밸런스·접근성·릴리스 위험 |
| Release Candidate | 치명적 버그, 플랫폼·배포·법무·복구 계획 |

## 5. 프로젝트 스킬 추가 판정

- [ ] 공용 절차는 foundation에 한 번만 존재한다.
- [ ] 분야 스킬이 본책·실제 경로·산출물·검증을 연결한다.
- [ ] 사용·비사용 조건과 실패 조건이 있다.
- [ ] Learning Log에 결과·실패·사용자 피드백을 기록했다.
- [ ] 지식 상태를 관찰·가설·패턴·검증·승격 후보로 구분했다.
- [ ] 새 채팅이 필요한 스킬만 선택할 수 있도록 Project Skill Map을 갱신했다.

## 6. PDF 추가 판정

- [ ] 분야 목적부터 전체 작업 과정·현재 상태·다음 작업을 포함한다.
- [ ] 승인 이미지·실제 캡처·상태 캡션이 있다.
- [ ] 책임 Markdown과 수치·용어·상태가 일치한다.
- [ ] Publication Manifest 입력·출력·해시를 갱신했다.
- [ ] PDF 헤더·목차·링크·표·이미지·한글 렌더링을 확인했다.
- [ ] 미생성·오래됨·실패 상태를 `NOT_BUILT/STALE/FAILED`로 표시했다.

## 7. 수명주기·마이그레이션 추가 판정

- [ ] `[백업]`은 Git 이력만으로 부족한 보존 사유가 있다.
- [ ] `[보류]`에 이유·재개 조건·책임 원본·선행 작업이 있다.
- [ ] `[제거 후보]`는 고유 정보·참조·복구·승인을 확인했다.
- [ ] 사용자 승인 전 대규모 삭제·이동·통합을 하지 않았다.
- [ ] 변경 전후 보존 대조에서 누락이 없다.
- [ ] 코드·Issue·PR·PDF·자동화의 참조를 갱신했다.

## 8. 작업 종료 체크

- [ ] 실제 결과와 본책의 확정·구현·검증 상태가 일치한다.
- [ ] 주 책임·영향 분야 본책과 협업 계약을 확인했다.
- [ ] Development Gates와 Roadmap을 확인했다.
- [ ] Project Skill Map·분야 스킬·Learning Log를 확인했다.
- [ ] Active Context·Handoff·Documentation Map·Changelog를 확인했다.
- [ ] Decision Log가 필요한 변경인지 확인했다.
- [ ] 이미지·사운드·데이터 Manifest를 확인했다.
- [ ] PDF·Publication Manifest를 갱신하거나 정확한 비최신 상태를 표시했다.
- [ ] 실행한 테스트와 미검증을 분리했다.
- [ ] 백업·보류·제거 후보가 기본 컨텍스트에 혼입되지 않았다.
- [ ] 다음 작업·선행 조건·재개 조건을 기록했다.
- [ ] 콜드 스타트에서 방향·게이트·스킬·PDF·검증 경로를 찾을 수 있다.

## 9. 프로젝트별 조정

- 통합한 분야와 책임 장:
- 추가한 분야:
- 실제 경로·파일명:
- Foundation·분야 프로젝트 스킬:
- PDF 생성 명령·강제 수준:
- 변경 유형별 예외:
- 자동 검사로 강제하는 규칙:
- 수동 통합검수로 남긴 규칙:
