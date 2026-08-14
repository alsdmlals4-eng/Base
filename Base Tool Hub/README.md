# Base Tool Hub

`Base Tool Hub/`는 Base 저장소의 로컬 개발 도구를 한곳에서 찾고 상태를 판단하기 위한 **공식 스위트 루트**입니다.

## 왜 실행 소스는 아직 `tools/*`에 있는가

현재 Base Tool Registry v1은 실행 소유자 경로를 `tools/<tool>`로 제한하고, Tool Hub의 고정 adapter·runtime trust·CI editable install 경로도 그 위치를 검증합니다. 지금 소스를 복사하면 두 개의 정본이 생기고, symlink를 두면 Windows reparse/symlink 안전 경계와 충돌합니다.

따라서 현재 단계에서는:

- 이 폴더가 **사람이 보는 통합 입구와 machine-readable suite manifest의 정본**입니다.
- 실제 실행 코드는 기존 `tools/*` 한 벌만 유지합니다.
- 물리 소스 이동은 Registry v2 경로 마이그레이션에서 모든 소비자를 한 번에 갱신한 뒤 진행합니다.

## 도구

| 도구 | 역할 | 현재 실행 정본 |
| --- | --- | --- |
| [Tool Hub](Tool%20Hub/README.md) | 프로젝트 자동 탐색·복제·등록, 도구 카탈로그, Windows 바탕화면 실행 | `tools/tool-hub` |
| [Character Studio](Character%20Studio/README.md) | 표정, 캐릭터 정체성을 유지한 복장 변경, 장소·배경 변경 | `tools/expression-studio` |
| [Sprite Animation Studio](Sprite%20Animation%20Studio/README.md) | 행동·포즈·이펙트 프레임, GIF·atlas·Godot handoff | `tools/sprite-animation-studio` |
| [QA Evidence Studio](QA%20Evidence%20Studio/README.md) | 결과 증거 검토와 Reality Gate | `tools/qa-evidence-studio` |
| [Tool Radar](Tool%20Radar/README.md) | 외부 도구 탐색·벤치마크·채택 판단 | 아직 Tool Hub 흡수 대상 |

기계가 읽는 목록은 [`TOOL_SUITE.json`](TOOL_SUITE.json)을 사용합니다.

## 현재 Reality Gate

- **Tool Hub Windows 실행/프로젝트 온보딩:** 검증됨. 바탕화면 `.lnk`로 PowerShell 없이 Hub를 시작·재사용·종료하고 프로젝트를 탐색/복제할 수 있습니다.
- **Figma 전달 대상:** 등록된 8개 프로젝트 모두 exact `Generated Assets` 노드에 대해 실제 PNG write → raw image readback → cleanup을 검증했습니다. 정본 라우팅은 `READY_FOR_DELIVERY`입니다.
- **Character/Sprite/QA의 Windows child 실행:** 아직 `BLOCKED_PLATFORM`. Hub가 Windows에서 켜지는 것과 Studio child를 안전하게 실행하는 것은 별도 단계입니다.
- **Character Studio 실제 provider 생성:** OpenAI Images adapter는 존재하지만 실제 성공 이미지는 아직 검증되지 않았습니다. provider 크레딧/실행 성공 증거가 필요합니다.
- **Sprite production 생성:** 행동·이펙트 import/export는 검증됐지만 production generator는 mutable workspace isolation이 없어 차단 상태입니다.

## 다음 구조 마이그레이션

실행 소스를 실제로 이 폴더 아래로 옮기려면 다음을 한 PR에서 함께 바꿔야 합니다.

1. Tool Registry schema v2의 `owner_path` 허용 경로.
2. Tool Hub의 reviewed tuple·runtime trust·source pin.
3. CI의 editable install/테스트 경로.
4. 문서·템플릿·테스트의 활성 참조.
5. Windows Studio portable backend와 새 경로 smoke.
6. exact-head 검증 후 병합, 새 `main` readback, 구 경로 제거/호환 정책 확인.

그 전에는 `tools/*`를 삭제·복제·symlink 처리하지 않습니다.
