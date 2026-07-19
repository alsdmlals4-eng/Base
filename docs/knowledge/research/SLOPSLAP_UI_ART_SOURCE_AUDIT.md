# SlopSlap UI 아트 소스 감사

## 감사 기준

- 원본: [vibedesignlab/slopslap](https://github.com/vibedesignlab/slopslap)
- 기준 브랜치·커밋: `main` / `6b5dae1efaa319d7bb015ee5c2d593933b92911b`
- 라이선스: MIT, Copyright (c) 2026 groovelb
- 인벤토리: [slopslap-6b5dae1e.json](inventories/slopslap-6b5dae1e.json)
- tracked 파일: 51개, 400,241 bytes
- 역할 분류: asset 27, config 6, docs 5, lockfile 1, skill 3, source 9

모든 tracked 파일의 경로·SHA-256·크기·역할을 인벤토리화했다. 문서·스킬·스크립트·데이터·설정·lockfile은 내용을 읽고 호출 관계를 대조했으며, PNG/JPG 23개는 contact sheet로, SVG 4개는 실제 렌더로 전부 시각 확인했다. 외부 코드·스크린샷·참조 사이트 자산은 Base에 복사하지 않았다.

## 구조 파악

원본은 Claude Code 플러그인용 얇은 오케스트레이터와 A~E 영역 규칙, 정적 신호 스캐너, findings HTML 빌더, 외부 레퍼런스 데이터·스크린샷으로 구성된다. 정적 감사 → findings → A~E 순차 집행 → 새 컨텍스트 재점검 → 브라우저 렌더라는 흐름을 사용한다.

| 구성 | 역할 | Base 판정 | 근거 |
|---|---|---|---|
| A~E 독립 감사 | 장식·구조·간격·타입·색을 분리 | 변형 채택 | 누락을 줄이되 플랫폼 구조와 사용자 의도를 함께 본다. |
| findings의 검증 술어 | 상태 선언 대신 재확인 가능 조건 | 채택 | 각 제안이 실제로 검증 가능한지 드러낸다. |
| 감사 후 A→B→C→D→E 집행 | 상류 구조 변경 뒤 세부 표현 조정 | 채택 | 충돌과 중복 수정을 줄인다. |
| 별도 재점검 | 집행자의 자기확증 방지 | 채택 | 새 검사 컨텍스트와 실제 렌더를 요구한다. |
| 정적 신호 스캐너 | Web 후보 탐색 | 변형 채택 | Base는 Godot/Web을 지원하고 후보만 보고한다. |
| 문답 없는 기계 제거 | 효과를 발견 즉시 삭제 | 제외 | 확정된 아트 방향과 목적 있는 표현을 손상할 수 있다. |
| 모든 작업의 서브에이전트 강제 | A~E 병렬 실행 | 비이식 | Base 핵심 절차는 특정 에이전트 런타임 없이 동작해야 한다. |
| 로컬 HTML 서버·Claude 플러그인 | 결과 배포와 호출 | 프로젝트 전용 | Base는 JSON·Markdown 결과와 기존 도구를 사용한다. |
| 외부 사이트 실측값 snap | 변환 모드 참조값 | 변형 채택 | 참조는 복제값이 아니라 변환 축·차별화 근거로만 쓴다. |
| 원본 스크린샷·taxonomy 데이터 | 레퍼런스 코퍼스 | 비이식 | 출처·권리·최신성·프로젝트 적합성을 개별 검증해야 한다. |

## 비이식 구현과 결함

- `scripts/capture-reference.mjs`는 Playwright를 `/Users/ddd/Desktop/daily vibe/pizza/node_modules/playwright`에서 불러오는 macOS 사용자 전용 경로를 가진다.
- `build-findings-report.mjs`, `scan-slop-signals.mjs`, `fetch-references.mjs`, `gen-reference-data.mjs`, `src/data/referenceMatrix/index.js`는 `new URL(import.meta.url).pathname`을 Windows 파일 경로로 직접 사용한다. 공백·드라이브 문자가 포함된 Windows ESM 경로에서는 `fileURLToPath(import.meta.url)`이 필요하다.
- 정적 tell은 의도적 디자인과 반복적 결함을 항상 구분하지 못한다. Base 검사기는 신뢰도와 관찰 증거를 제시하고 수정 승인 권한을 갖지 않는다.
- “보이면 삭제”와 콘텐츠 불변을 전역 규칙으로 이식하지 않는다. Base에서는 사용자 작업 계약과 프로젝트 책임 원본이 변경·보호 범위를 정한다.

## Base 채택 계약

1. 딥인터뷰 또는 이미 확정된 아트 방향을 먼저 확인한다.
2. Godot와 Web의 구조 차이는 별도 어댑터로 해석한다.
3. 정적 검사는 `CANDIDATE`만 만들고 사용자 승인 전 대상 파일을 수정하지 않는다.
4. 승인된 finding만 A→B→C→D→E 순서로 고친다.
5. 목적 있는 디자인은 규칙 ID와 보존 사유를 기록해 반례로 유지한다.
6. 집행과 분리된 재감사와 실제 전후 렌더가 완료 증거다.
7. 참조 작품은 Adopt·Adapt·Reject·Differentiation 결정 근거이며 고유 표현이나 자산 복제 대상이 아니다.

## 추가 표준 근거

- [Godot Control 공식 문서](https://docs.godotengine.org/en/stable/classes/class_control.html): anchor·offset, Container 배치, Theme·override 관계의 플랫폼 근거
- [WCAG 2.2 Contrast Minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html): 텍스트 대비 판정 근거
- [WCAG 2.2 Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html): 상태·컨트롤·그래픽 대비 판정 근거

이 문서는 원본의 표현을 복제하는 설계서가 아니라, 기준 커밋에서 확인한 구조와 Base에 채택·제외한 이유를 추적하는 감사 기록이다.
