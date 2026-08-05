# External UI Procurement and Anti-Generic Quality Gate

## 목적

shadcn/ui Registry·MCP 등 외부 UI 코드와 디자인 참고 자료를 프로젝트에 넣기 전에 출처·공급망·플랫폼 적합성·실제 품질을 분리해 판정한다.

## Gate 분리

```text
1. Source acquisition
2. Code admission
3. Installation approval
4. Runtime·accessibility validation
5. Actual render anti-generic review
```

`MCP 연결 성공`은 검색 통로가 열렸다는 뜻일 뿐 `설치 승인`, 코드 안전, 접근성, 실제 렌더 품질 통과가 아니다.

## Procurement receipt

```yaml
registry_source:
exact_version_or_commit:
registry_item:
source_paths: []
content_hash:
license:
dependencies: []
registry_dependencies: []
scripts: []
secrets: []
files_added_or_replaced: []
existing_system_overlap: []
security_review:
accessibility_review:
runtime_review:
actual_render:
rollback:
decision: ADOPT | ADAPT | REJECT | BLOCKED_UNVERIFIED
reason_codes: []
```

다음 중 하나라도 확인되지 않으면 fail closed한다.

- exact source identity와 content hash
- license와 프로젝트 배포 조건
- declared dependency와 실제 import·생성 결과
- install script·postinstall·network·secret 요구
- 기존 파일 덮어쓰기·상태 소유권·rollback

문서·Registry·source 간 의존성 선언이 다르면 즉시 결함으로 단정하지 않고 CLI 변환·생성 결과를 확인할 때까지 `BLOCKED_UNVERIFIED`로 둔다.

## 플랫폼 판정

### Web

프로젝트가 React·Web 표면이고 기존 디자인 시스템과 충돌하지 않으면 `ADOPT` 또는 `ADAPT` 후보가 될 수 있다. 소스 소유형 배포라도 upstream provenance와 update 책임은 남는다.

### Godot

React·CSS·Tailwind 컴포넌트는 Godot `Control`·`Theme`·Scene 구현이 아니다. Web 관리 도구가 별도 범위로 승인되지 않은 한 Godot 프로젝트에 기본 설치하지 않고 `REJECT` 또는 `BLOCKED_UNVERIFIED`로 판정한다.

## Anti-generic quality

설치 뒤 다음을 실제 렌더에서 검토한다.

```yaml
Design Read:
page_or_screen_kind:
audience:
project_vibe:
visual_variance:
motion_intensity:
information_density:
repeated_default_patterns: []
intentional_exceptions: []
actual_render:
before_after:
```

- 흔한 AI 기본값을 후보로 찾되 gradient, card, glass, serif 등 표현을 무조건 금지하지 않는다.
- 계층·가독성·상태·입력·복구·접근성을 장식보다 먼저 해결한다.
- 프로젝트의 DESIGN.md·GAME_UX_UI_SYSTEM·실제 목적에 맞는 의도적 표현은 보존한다.
- 실제 렌더 없이 “AI 티가 제거됐다”고 주장하지 않는다.

## 판정

- `ADOPT`: source·license·dependency·overwrite·runtime·accessibility·render가 검증됐고 최소 수정으로 적합하다.
- `ADAPT`: 원리는 적합하지만 프로젝트 token·상태·입력·플랫폼에 맞는 변환이 필요하다.
- `REJECT`: 플랫폼·코어·보안·라이선스·상태 소유권과 충돌한다.
- `BLOCKED_UNVERIFIED`: 필요한 source·CLI 변환·build·runtime·접근성·렌더 증거가 없다.

## 적대적 검토

- “공식 Registry”라는 이유로 코드를 무검토 설치했는가.
- source 조회 성공을 설치·빌드·품질 성공으로 승격했는가.
- dependency 선언과 실제 import·lockfile이 일치하는가.
- MCP 또는 설치 도구가 secret·network·shell·overwrite 범위를 넓혔는가.
- 외부 컴포넌트가 도메인 상태를 소유하거나 기존 시스템을 이중화하는가.
- default styling을 그대로 배치해 프로젝트 고유 방향과 접근성을 잃었는가.
- rollback이 source receipt와 실제 변경 파일을 복원할 수 있는가.
