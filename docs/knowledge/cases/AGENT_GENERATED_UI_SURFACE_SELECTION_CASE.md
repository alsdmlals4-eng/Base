# 사례 — 에이전트 생성 UI 시대의 CLI/TUI/GUI 선택

- 출처 프로젝트·벤치마킹: 외부 글 `Stop Making TUIs` 및 공개 반론, Base 내부 도구 구조
- 확인 날짜: 2026-08-24
- 작성 상태: 채택 — Base 선택 규칙 반영, 실제 프로젝트 반복 검증 전
- 주제: 에이전트가 UI 구현비용을 낮춘 환경에서 CLI/TUI/thin GUI를 언제 선택할지 결정

## 1. 문제

에이전트가 네이티브·그래픽 UI 구현을 빠르게 보조할 수 있게 되면서 “내부 도구는 구현하기 쉬운 CLI/TUI로 만든다”는 과거의 비용 전제가 약해졌다. 반대로 생성 비용이 낮아졌다는 이유만으로 모든 도구에 GUI를 추가하면 UI 스택·패키징·플랫폼 검증·접근성·유지보수 비용이 다시 늘고, Base가 이미 폐기한 Tool Hub류의 별도 관리 surface가 되살아날 수 있다.

필요한 것은 `TUI vs GUI` 취향 결론이 아니라 **동일 core를 보존한 채 실제 operator와 작업 특성에 맞는 interface surface를 선택하는 계약**이다.

## 2. 맥락과 제약

- 사용자·플레이어 경험: 주 대상은 개발자/AI가 사용하는 제작·검증 도구이며, 사람 반복 작업에서는 discoverability와 visual comparison도 중요하다.
- 플랫폼·장르: Base는 Windows 중심 게임 개발과 GitHub/Notion/로컬 실행을 함께 사용하지만, 공용 규칙은 특정 desktop framework를 강제하지 않는다.
- 일정·예산·팀: 1인 개발에 맞게 `ZERO_INCREMENTAL_COST_DEFAULT`와 낮은 수명주기 비용이 중요하다.
- 기술·성능: CLI는 자동화·CI·agent invocation·headless/remote 실행에 강하고, TUI/GUI는 추가 surface 비용이 생긴다.
- 권리·출처: 외부 글과 공개 토론은 설계 근거일 뿐 Base나 프로젝트 정본이 아니다. 고유 코드·UI 표현은 복사하지 않는다.

## 3. 관찰 근거

- 직접 확인한 자료:
  - 사용자 제공 `Stop Making TUIs` GeekNews 요약 및 Hacker News 반론 모음.
  - Base의 현재 `VISUAL_COLLABORATION_TOOL_POLICY.md`, `CAPABILITY_COMPOSITION_MAP.md`, `BENCHMARKING_REFERENCE_GUIDE.md`와 retired-surface 정책.
- 1차 출처:
  - `https://sockpuppet.org/blog/2026/08/20/stop-making-tuis/`
  - Microsoft Windows App SDK / WinUI 3 공식 문서 — 새 Windows native app의 현행 선택지를 교차 확인.
  - Ratatui 공식 문서 — TUI가 여전히 SSH/terminal-resident 도구의 현행 선택지임을 교차 확인.
- 사용자 반응:
  - 공개 반론에서는 TUI의 cross-platform/SSH/tmux/terminal residency와 keyboard-centric efficiency가 실제 가치라는 의견이 반복됐다.
  - 동시에 `keyboard-first`와 높은 정보 밀도는 TUI 고유 속성이 아니라 GUI에서도 설계 가능한 상호작용 속성이라는 반론도 확인됐다.
- 아직 확인하지 못한 항목:
  - 외부 글의 직접 실험은 주로 macOS/SwiftUI이며 Windows/Linux의 동일 생산성은 검증되지 않았다.
  - Base의 실제 프로젝트 도구에서 thin GUI가 CLI/TUI보다 반복 작업 시간을 얼마나 줄이는지는 아직 측정하지 않았다.
  - 접근성 우위는 surface 종류만으로 판정할 수 없으며 대상 OS/프레임워크에서 별도 검증이 필요하다.

## 4. 검토한 대안

### 대안 A — CLI-only를 계속 기본 최종 surface로 고정

- 장점: 자동화·테스트·agent 호출·배포가 단순하고 lifecycle cost가 가장 낮다.
- 단점: 이미지/프리뷰 비교, drag-and-drop, 공간 배치, 반복 triage 같은 인간 작업에서는 조작 마찰이 커질 수 있다.
- 제외 또는 채택 이유: machine-facing 기본 계약으로는 **채택**하지만, 모든 human-facing 작업의 유일 surface로 고정하는 것은 제외한다.

### 대안 B — agent가 UI를 쉽게 만드므로 GUI-first로 전환

- 장점: standard controls, visual comparison, discoverability, direct manipulation을 얻기 쉽다.
- 단점: GUI stack·packaging·platform verification·accessibility·maintenance가 추가되며, 생성 성공을 제품 품질로 오인하기 쉽다.
- 제외 또는 채택 이유: **REJECT**. 외부 글의 직접 검증 범위가 macOS/SwiftUI에 치우쳐 있고 Base의 retired management surface 정책과도 충돌한다.

### 대안 C — one core + CLI/programmatic contract + 조건부 TUI/thin GUI

- 장점: 자동화 가능성을 유지하면서 실제 반복 인간 작업이 필요할 때만 richer surface를 추가한다. 상태·정본 중복을 피할 수 있다.
- 단점: surface 선택 기준과 target-platform evidence를 명시적으로 관리해야 한다.
- 제외 또는 채택 이유: **ADAPT / 권장안**. 장기 비용·재사용성·되돌리기 가능성과 Base의 현재 구조가 가장 잘 맞는다.

## 5. 결정

```text
canonical data / repository / runtime truth
→ reusable domain core
→ stable CLI / programmatic contract
   ├─ CLI-only
   ├─ TUI when terminal residency materially matters
   └─ thin GUI when repeated human visual/direct manipulation repays cost
```

- 채택한 이유:
  - CLI의 automation/composability 장점을 보존한다.
  - TUI의 실제 강점인 SSH/tmux/terminal residency를 취향이 아니라 조건으로 보존한다.
  - thin GUI는 반복 인간 작업의 visual/spatial friction을 줄이는 경우에만 추가한다.
  - keyboard-first/high information density를 surface-independent 목표로 분리한다.
  - 하나의 domain core가 상태·규칙을 소유하므로 GUI/TUI가 두 번째 정본이 되는 것을 막는다.
- 적용 범위:
  - Base 내부 도구와 프로젝트용 제작·검증 도구의 새 surface 설계 또는 대규모 surface 변경.
  - `TOOL_PATTERN` 역공학 결과를 실제 도구로 구현할 때의 선택 gate.
- 제외 범위:
  - Tool Hub, QA Evidence Studio, Figma-first, external HTML dashboard/workspace의 자동 부활.
  - 모든 기존 CLI에 GUI를 붙이는 일괄 migration.
  - 특정 native/cross-platform UI framework의 공용 표준화.

## 6. 결과

- 실제 결과:
  - Base에 `TOOL_INTERFACE_SURFACE_SELECTION` 계약과 CLI/TUI/thin-GUI 3안 비교 구조를 추가하는 변경을 준비했다.
  - 새 broad Skill이나 UI framework dependency를 추가하지 않고 기존 benchmarking/capability owner에 흡수했다.
- 측정·테스트:
  - focused repository contract가 owner 문서에 선택 gate, single-core 경계, machine contract, conditional human surface, target-platform evidence, retired-surface 비회귀를 요구한다.
  - 실제 project tool에서 human-workflow productivity 측정은 아직 실행하지 않았다.
- 실패·부작용:
  - 새 regression 파일을 만들기만 했을 때 기존 permanent CI가 이를 자동 발견하지 않는 문제가 확인됐다. permanent Base v9 test list에 명시적으로 연결해 실제 RED를 확인하도록 보완했다.
- 미검증:
  - 실제 Windows/Linux/macOS GUI/TUI implementation quality.
  - 실제 접근성.
  - 실제 반복 작업 시간 절감과 human decision quality.

결과의 현재 evidence ceiling은 Base 정책/CI 계약 수준이며 실제 UI 제품의 `TARGET_PLATFORM_VERIFIED` 또는 `HUMAN_WORKFLOW_VALUE_VERIFIED`를 의미하지 않는다.

## 7. 재사용 가능한 원칙

- 다른 프로젝트에서도 사용할 수 있는 판단 원리:
  - **machine contract와 human surface를 분리한다.**
  - **한 core가 상태와 규칙을 소유한다.**
  - **surface 추가는 반복 작업에서 비용을 갚을 때만 한다.**
  - **keyboard-first는 TUI 여부가 아니라 interaction requirement로 기록한다.**
  - **한 플랫폼의 성공을 다른 플랫폼/접근성 성공으로 일반화하지 않는다.**
- 체크리스트로 바꿀 항목:
  - operator, 반복 빈도, SSH/remote, visual/spatial need, keyboard density, packaging, accessibility, testability, lifecycle cost, monetary cost, same-core reuse.
- methods 또는 skills 승격 후보:
  - 별도 Skill은 만들지 않는다. 현행 `BENCHMARKING_REFERENCE_GUIDE.md`와 `CAPABILITY_COMPOSITION_MAP.md`의 reusable method/contract로 유지한다.

## 8. 그대로 복사하면 안 되는 요소

- 프로젝트 특화 수치·세계관·자산: 해당 없음. 외부 앱의 화면·코드·고유 표현은 재사용하지 않는다.
- 다른 전제에서 실패할 조건:
  - GUI runtime/packaging가 설치 불가능한 remote 서버.
  - terminal-only 환경.
  - 인간 조작이 거의 없고 agent/CI만 사용하는 one-shot tool.
  - GUI framework가 project platform/dependency budget과 맞지 않는 경우.
- 권리·라이선스 주의:
  - 공개 글에서 관찰한 원리만 추출한다. 외부 code/assets/UI expression 직접 재사용은 별도 license 검토가 필요하다.

## 9. 검증 방법

- 자동 검증:
  - Base focused contract test + permanent Base CI.
  - interface adapter가 core/state owner를 중복하지 않는 구조 검사.
- 수동 검증:
  - 실제 target OS에서 build/package, keyboard/mouse path, resize/scaling, file/drag-drop, error/recovery를 요구 수준에 맞게 확인.
- 사용자 테스트:
  - 동일 작업을 CLI-only baseline과 비교해 반복 작업 시간, 오류, decision quality, discoverability가 실제로 개선되는지 측정.
- 후속 질문:
  - 이 도구는 실제로 사람이 얼마나 자주 조작하는가?
  - terminal residency가 필요 조건인가, 단지 익숙함인가?
  - richer surface가 추가 lifecycle cost를 갚는가?

## 10. 관련 문서

- Base 방법: `docs/BENCHMARKING_REFERENCE_GUIDE.md`
- Base 스킬: 새 Skill 없음; 기존 Existing Solution First / benchmarking / review routing을 재사용
- 프로젝트 책임 원본: 실제 채택 시 해당 프로젝트 `AGENTS.md`, Active Context, tool/runtime owner
- 외부 출처: `Stop Making TUIs` 및 공개 반론; Windows App SDK/WinUI 3, Ratatui 공식 문서의 2026-08-24 확인 범위
