# UI 아트 정적 감사 후보

> 이 보고서는 정적 패턴 후보이며 결함 확정이나 자동 수정 지시가 아닙니다.

- 검사 루트: `after`
- 어댑터: web
- 검사 파일: 2
- 후보: 2
- 사유 있는 제외: 0

## Findings

### web-b-w-b-fixed-layout-0045d15be8

- 영역/어댑터: B / web
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `style.css:20`
- 관찰: `@media (max-width: 760px) { .shell { padding: 2rem 1.25rem; } header { align-items: start; flex-direction: column; } .steps { grid-template-columns: 1fr; } }`
- 위험: 고정 크기나 절대 위치가 콘텐츠·번역·viewport 변화에서 구조를 깨뜨릴 수 있다.
- 제안: 해당 고정값의 연출 목적을 확인하고 필요하면 flow, flex, grid 또는 유연한 제약으로 바꾼다.
- 검증: 대표 viewport와 긴 콘텐츠에서 겹침·잘림·가로 스크롤이 없는지 확인한다.
- 상태: CANDIDATE

### web-e-w-e-color-literal-6b90ece857

- 영역/어댑터: E / web
- 심각도/신뢰도: LOW / LOW
- 위치: `style.css:3`
- 관찰: `body { margin: 0; min-height: 100vh; background: #091116; color: var(--ink); font-family: "Noto Sans KR", "Malgun Gothic", sans-serif; }`
- 위험: 직접 색상 값이 상태 체계와 대비 규칙에서 벗어날 수 있다.
- 제안: 실제 전경·배경과 상태 역할을 확인하고 필요한 경우에만 승인된 토큰으로 연결한다.
- 검증: 실제 조합의 대비와 normal·hover·focus·disabled 상태 구분을 확인한다.
- 상태: CANDIDATE
