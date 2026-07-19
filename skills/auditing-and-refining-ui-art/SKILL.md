---
name: auditing-and-refining-ui-art
description: Godot 또는 Web UI 결과물의 기계적 장식, 구조, 간격, 타이포그래피, 색상·상태 표현을 증거 기반으로 감사하고 사용자 승인 범위만 개선할 때 사용한다. UI 아트 방향 수립, 기존 화면 품질 감사, 정적 후보 검사, 전후 렌더 재검수가 필요한 요청에서 사용한다.
---

# UI 아트 감사와 개선

## 역할

Godot와 Web UI를 같은 품질 원칙으로 감사하되 플랫폼 구조는 각각의 어댑터로 해석한다. 정적 패턴은 후보만 보고하며 실행 화면, 확정된 아트 방향, 사용자 의도를 함께 대조한 뒤 판단한다.

이 스킬은 생성 프롬프트나 기술 카드를 만드는 `designing-art-prompts-and-technique-cards`와 역할이 다르다. 그 스킬은 생성 전 계약을 만들고, 이 스킬은 만들어진 UI를 감사하고 승인된 범위만 개선한다.

## 사용 조건

다음 경우에 사용한다.

- Godot `Control`, `Container`, `Theme`, `StyleBox` 기반 UI를 감사하거나 개선한다.
- HTML, CSS, JavaScript, TypeScript, React 계열 UI를 감사하거나 개선한다.
- 아트 방향과 실제 실행 결과의 차이를 증거로 정리해야 한다.
- A~E 영역별 Findings와 전후 렌더 검증이 필요하다.

다음 경우에는 사용하지 않는다.

- UI와 무관한 게임 로직, 네트워크, 저장 데이터만 변경한다.
- 새 이미지 생성 프롬프트나 아트 기술 카드만 작성한다.
- 사용자가 이미 승인한 명확한 단일 파일 기계 수정만 수행한다.

## 필수 절차

1. 프로젝트 책임 원본과 실제 UI 파일을 읽고 현재 화면을 렌더한다.
2. 아트 방향이 미확정이거나 기능·게임 경험·구조·워크플로에 영향이 있으면 `conducting-deep-requirement-interviews`를 먼저 사용한다.
3. [inspection-areas.md](references/inspection-areas.md)의 A~E를 각각 독립적으로 감사한다.
4. 플랫폼별 구조는 [platform-adapters.md](references/platform-adapters.md)로 해석한다.
5. 필요하면 다음 명령으로 읽기 전용 후보를 만든다.

```text
python skills/auditing-and-refining-ui-art/scripts/scan_ui_art_signals.py --root <대상> --adapter auto --output-json <findings.json> --output-markdown <findings.md>
```

6. Findings JSON과 Markdown에 파일·행·관찰 증거·디자인 위험·제안·검증 조건을 기록한다.
7. 정적 패턴만으로 결함이나 “AI slop”을 확정하지 않는다. 각 후보를 실행 화면과 의도에 대조해 승인 요청 목록으로 정리한다.
8. 사용자 승인 전에는 UI 파일, 이미지, Theme, CSS를 수정하지 않는다.
9. 승인 후 A → B → C → D → E 순서로 수정한다. 앞 영역의 구조 변경이 뒤 영역의 판단을 바꿀 수 있으므로 한 영역씩 렌더하고 확인한다.
10. 기존 판단을 보지 않은 새 검사 컨텍스트로 재감사하고 Godot/Web 실제 렌더 전후를 비교한다.

## Findings 계약

각 finding은 다음 필드를 가진다.

```text
finding_id
area
adapter
severity
confidence
file
line
observed_evidence
design_risk
proposed_change
verification_predicate
status
```

검사기 결과의 초기 상태는 `CANDIDATE`다. 사용자가 승인하면 `APPROVED`, 보존하기로 하면 `WAIVED` 또는 `REJECTED`, 재검증까지 끝나면 `RESOLVED`로 기록한다.

목적 있는 표현은 해당 파일에 다음처럼 사유를 남겨 정적 후보에서 제외할 수 있다.

```text
base-ui-audit: allow <RULE_ID> reason=<보존 이유>
```

허용 지시는 결함을 숨기는 수단이 아니다. 실행 화면과 아트 방향에서 이유가 확인되지 않으면 다시 후보로 올린다.

## 승인과 검증 게이트

- 아트 방향 또는 승인 근거가 없으면 수정 단계로 넘어가지 않는다.
- 참조 작품은 변환 축과 차별화 근거로만 사용하고 화면, 자산, 고유 표현을 복제하지 않는다.
- Godot에서는 Scene 실행 결과, 테마 상속, 상태 피드백, 다른 해상도를 확인한다.
- Web에서는 실제 브라우저, 반응형 폭, 키보드 포커스, 상태 표현을 확인한다.
- 수정 후 정적 Findings가 줄었다는 사실만으로 통과시키지 않는다. 전후 렌더와 승인된 의도를 함께 검증한다.
- 전후 화면과 재감사 증거가 없으면 완료가 아니다.

## 필요한 도구·파일·권한 요청

작업에 필요한 실행 파일, 폰트, 참조 원본, 브라우저, Godot 버전, 쓰기 권한이 없으면 임의 대체하지 않는다. 사용자에게 `필요 항목 / 필요한 이유 / 공식 설치·적용 방법 / 확인 명령 / 최소 권한`을 함께 제시하고, 기존 정상 산출물을 보존한 채 기다린다.
