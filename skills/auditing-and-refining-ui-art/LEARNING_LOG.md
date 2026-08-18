# Auditing and Refining UI Art — Learning Log

## 2026-08-19 — UI/UX 외부 Source 선택 흡수와 Figma discovery watch

- **상태:** `OBSERVATION`
- **Sources:** `nextlevelbuilder/ui-ux-pro-max-skill@a38d04c3d5c298c851dbe5e6ee1965ee3de42cb5`, `google-labs-code/design.md@9bf8eae67128b6cc55ad9bf86665767deb4c11cd`, `https://huddling.ai/figma-info`.
- **Finding:** Base의 BCP-008과 `auditing-and-refining-ui-art`가 DESIGN.md adapter·외부 UI 조달·anti-generic Gate·UI 상태/중단 계약을 이미 소유하므로 외부 Skill/CLI를 통째로 설치하면 owner와 데이터가 중복된다. 반면 design intent를 prose로 고정하는 방식, specific reference의 이유 기록, resilient text와 compact state의 중단 복원은 기존 owner를 더 명확하게 만든다.
- **Decision:** `ui-ux-pro-max-skill`은 `ADAPT` — `essential text` reflow, badge/chip 의미의 다중 신호, interaction cancel 뒤 semantic state/focus/content 일치, visual variance·motion intensity·information density를 설계 비교축으로만 흡수한다. 79-style/제품 profile/BM25/Web stack CLI와 데이터셋은 복제·설치하지 않는다.
- **Decision:** `google-labs-code/design.md`의 token/schema/lint/diff와 Project DESIGN.md adapter는 `ALREADY_COVERED`; `ADAPT`로 prose 기반 design intent, specific reference + reason, 짧은 Do/Don't, token/lint의 증거 상한만 기존 UI method에 보강한다.
- **Decision:** Huddling Figmapedia는 `DISCOVERY_FEED`로 weekly cadence에 등록한다. Figma 기능·MCP·정책 사실은 Huddling 설명만으로 확정하지 않고 Figma 공식 문서·release note 또는 연결된 original source로 backtrace한다.
- **Boundary:** 신규 ACTIVE Skill `0`, 신규 scheduler `0`, package/CLI 설치 `0`, 프로젝트 Canon·Godot runtime 변경 `0`. 외부 원문·스타일 표·대규모 데이터셋을 Base에 복제하지 않는다.
- **TDD evidence:** Draft PR #526 RED head `c59ee2a1ecbc620a9e6934106af2267d1beadfab`에서 기존 UI unittest 53개는 PASS했고 신규 계약 3개가 의도한 누락으로 FAIL했다. GREEN과 전체 적대적 회귀는 구현 exact head에서 별도 확인한다.
- **Evidence ceiling:** Source 흡수와 정적 회귀는 실제 프로젝트 렌더·사람 이해·미적 품질 개선을 증명하지 않는다. 실제 프로젝트 적용 전 효과는 `OBSERVATION`이다.
- **Next trigger:** 세 upstream source의 material update, Huddling 후보가 반복적으로 Figma 공식 원문과 불일치, 또는 서로 다른 두 프로젝트에서 이 Design Read/복원력 계약의 실제 효과가 관찰될 때 재검토한다.
