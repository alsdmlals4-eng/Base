# PC-First Tooling Benchmark and Selection Record

조사일: 2026-08-13
결정 범위: 추가 비용 없이 개발자 1명이 PC 구현과 이미지·UX 배치 후 사용할 도구
명시적 제외: Android 연결, 외부 테스터 모집, 실제 게임 시각 품질 판정

## 현업 패턴과 비교

| 사례 | 확인한 현업 가치 | 현재 적합성 | 결정 |
|---|---|---|---|
| [Backstage Software Catalog](https://backstage.io/docs/features/software-catalog/) | 도구와 구성요소를 catalog 중심으로 모아 탐색·문맥 전환 비용을 줄임 | 방향은 맞지만 공식 도입 가이드도 중앙 운영팀·지원·CI/CD·on-call 소유를 전제로 설명한다. 1인 개발 단계에는 운영비가 과함 | 전체 플랫폼을 도입하지 않고, reviewed manifest + typed launcher라는 최소 패턴만 Tool Hub에 채택 |
| [Kiwi TCMS](https://kiwitcms.readthedocs.io/en/latest/about.html) | 수동·자동 테스트 계획, 실행, 추적, 권한, 보고를 통합하는 오픈소스 TCMS | 팀·테스터·서버 운영이 없는 현재 단계에는 기능과 운영면이 과함 | 지금은 제외. 외부 테스터와 반복 test run이 생길 때 재평가 |
| [Allure Report](https://allurereport.org/docs/) | 여러 자동화 프레임워크의 실행 결과를 첨부·단계와 함께 HTML 보고서로 변환 | 자동화 결과 보고에는 강하지만, 아직 존재하지 않는 실제 이미지·UX 인간 검토를 대신하지 못함 | 현재 의존성으로 추가하지 않음. 반복 자동화 결과가 축적될 때 packet exporter 후보 |
| [Playwright Trace Viewer](https://playwright.dev/docs/trace-viewer) | 실행 후 action, DOM snapshot, network, screenshot을 함께 탐색해 실패 원인을 재현 | 브라우저 UI 자동화가 안정된 뒤 강한 보완재. 현재는 실제 게임 이미지·UX가 배치되기 전이라 자동화가 앞섬 | Phase 1은 수동 PC 증거 Gate만 구현. 안정된 UI 흐름부터 후속 자동화 후보 |
| [GitHub Issue Forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository) | 필수 필드를 가진 구조화된 버그 입력을 저장소 이슈로 수집 | 기존 GitHub 안에서 추가 SaaS 비용 없이 쓸 수 있지만 신규 테스터·버그 intake가 현재 없음. 공식 문서상 public preview이기도 함 | 지금은 제외. 외부 피드백 채널을 열 때 최소 intake 후보 |

## 성공 사례에서 가져온 것과 가져오지 않은 것

- Backstage는 Spotify에서 중앙 포털을 제품처럼 운영하는 조직 소유가 성공 조건이라고 명시한다. 따라서 Base에는 "한 화면에서 검토된 도구를 찾는다"는 패턴만 가져오고, 플러그인 생태계·서비스 catalog·운영 플랫폼은 가져오지 않았다.
- Kiwi TCMS의 [SiteGround 사례](https://kiwitcms.org/blog/)는 테스트 지식·추적성의 중앙 저장소와 자동화/CI 실행을 구분한다. QA Evidence Studio도 같은 구분을 적용해 사람이 확인한 이미지 증거와 도구 자체 회귀테스트를 서로 대체하지 않는다.
- Allure의 [history와 retries](https://allurereport.org/docs/history-and-retries/)는 동일 테스트의 반복 결과가 쌓일 때 가치가 커진다. 단발성 개발자 검토 단계에서는 history UI를 먼저 만들지 않고, Git commit·SHA-256·결과 상태가 포함된 이식 가능한 JSON packet만 남긴다.

## 적대적 분류

| 분류 | 도구/패턴 | 판단 근거 |
|---|---|---|
| 지금 정말 사용하면 좋음 | 최소 Tool Hub | 이미 존재하는 Studio를 reviewed registry로 발견하고, 프로젝트 ID에 묶인 고정 실행만 허용해 실행 혼선과 임의 명령 위험을 줄임 |
| 지금 정말 사용하면 좋음 | QA Evidence Studio | 개발자 단독 PC 검토라는 실제 인력 조건, 이미지·UX 배치 이후라는 시점, Android 연기 상태를 왜곡 없이 증거화 |
| 조건 충족 후 좋음 | Playwright + Allure | UI가 안정되고 반복 자동화 run이 생긴 뒤 trace와 history를 연결할 때 투자 대비 효과가 생김 |
| 조건 충족 후 좋음 | GitHub Issue Forms | 신규 테스터나 외부 버그 제보자가 생겨 구조화된 intake가 필요할 때 사용 |
| 현재 사용하지 않음 | Kiwi TCMS / 전체 Backstage | 1인·로컬·무서버 단계에서 설치·운영·권한·업그레이드 비용이 현재 효용보다 큼 |

## 선택 결론

Phase 1은 Base 내부의 기존 Python/FastAPI 구성만 사용한다. 유료 API, 외부 데이터 저장, 신규 서버, Android SDK, 테스터 계정은 추가하지 않는다. 실제 게임 품질 판정은 이미지와 UX가 배치된 이후 개발자 검토로만 생성하며, 자동 회귀테스트는 도구 계약이 작동한다는 증거로만 보고한다.
