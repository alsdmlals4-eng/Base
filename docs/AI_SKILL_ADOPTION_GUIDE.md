# AI Skill Adoption Guide

이 문서는 외부 AI 스킬과 에이전트 워크플로우를 프로젝트에 채택할 때 쓰는 공용 판단 기준이다. 특정 저장소의 프롬프트를 그대로 복사하지 않고, 검증 가능한 원칙만 현재 프로젝트 규칙에 맞게 적용한다.

## 1. 우선순위

외부 스킬은 보조 수단이다. 다음을 덮어쓸 수 없다.

1. 사용자의 최신 지시
2. 프로젝트 `AGENTS.md`와 보안·엔진 규칙
3. 현재 Issue, 승인된 사양, Goal
4. 실제 파일과 실행 결과
5. 선택한 외부 스킬

스킬이 충돌하면 더 구체적인 상위 규칙을 따른다. 플러그인 미설치나 실행 실패는 프로젝트 작업 중단 사유가 아니다.

## 2. 채택 전 확인

외부 스킬을 설치하거나 규칙에 반영하기 전에 다음을 확인한다.

- 해결하려는 작업 유형과 실제 trigger가 맞는가
- `SKILL.md`, 실행 스크립트, hook, MCP, 외부 API, 저장 경로를 확인했는가
- 저장소의 최신 상태, 라이선스, 유지보수 상태를 확인했는가
- 브라우저 쿠키, API 키, 파일 쓰기, 네트워크 전송처럼 추가 권한이 필요한가
- 기존 프로젝트 규칙과 중복되거나 모순되는가
- 같은 효과를 현재 도구나 짧은 규칙으로 얻을 수 있는가
- 설치하지 않고 원칙만 적용하는 편이 더 단순한가

외부 스크립트는 첫 실행 전에 읽는다. 비밀값을 출력·저장·전송하는지 확인하고, 필요하면 `preflight` 또는 읽기 전용 진단부터 실행한다.

## 3. 최소 라우팅

한 작업에는 필요한 최소 스킬만 사용한다. 기본값은 프로세스 스킬 1개와 도메인 스킬 1개 이하이며, 실제로 독립된 작업이 있을 때만 추가한다.

| 작업 신호 | 적용할 원칙 | 참고 계열 |
|---|---|---|
| 요구가 모호함 | 의도 확인, 사양, 실행 프롬프트 순으로 구체화 | Superpowers, mattpocock/skills |
| 기능·수정 구현 | 기존 코드 재사용, native/stdlib 우선, 최소 diff | Ponytail |
| 버그·성능 문제 | 재현 가능한 feedback loop와 root cause를 먼저 확보 | mattpocock/skills, Superpowers |
| UI/UX | brief·대상·기존 디자인을 먼저 읽고 밀도·움직임·변형 정도를 명시 | Taste Skill |
| 장기 조사 | 기간, 출처 종류, 최신성, 신뢰도, 적용 결론을 분리 | last30days |
| 보안 경계 | secrets, 입력, 권한, 외부 전송, 의존성을 별도 점검 | ECC |
| 완료 보고 | 실제 명령과 결과를 근거로 완료 여부 판단 | ECC, Superpowers |
| 긴 작업 | 논리적 phase 경계에서만 compact하고 핵심 상태를 파일에 남김 | ECC strategic-compact |
| 긴 문서·보고 | filler와 중복을 제거하되 경로·명령·숫자·결정은 보존 | Caveman |

스킬 이름을 호출하는 것보다 원칙이 현재 작업에 맞는지가 중요하다.

### 자원 인식형 도구·에이전트 운영

- 성능 문제가 생기면 작업량을 줄이기 전에 전체 메모리, 상위 점유 프로세스, 중복 MCP·언어 서버·브라우저 렌더러를 측정한다.
- 대부분의 작업에 필요하지 않은 MCP, 대시보드, 언어 서버 같은 선택형 보조 도구는 기본 비활성화하거나 필요한 작업에서만 실행한다.
- 핵심 작업량과 사용자가 요구한 병렬 흐름은 보존하되, 같은 저장소의 대용량 외부 worker는 측정된 여유가 없으면 한 번에 하나만 실행한다.
- 외부 worker 결과는 전체 원시 대화보다 작업 계약, 변경 diff, 검증 결과, 길이가 제한된 보고서로 회수한다. 원시 로그는 실패 분석에 필요할 때만 읽는다.
- 단계가 끝나면 사용이 끝난 subprocess와 보조 서버를 종료하고, 성공한 임시 작업 공간만 안전하게 정리한다. 실패하거나 변경이 남은 작업 공간은 자동 삭제하지 않는다.
- 최적화 완료 여부는 설정값이 아니라 재시작 후 프로세스 수와 전후 자원 사용량으로 검증한다.

## 4. 최소 구현 사다리

구현 전 다음 순서로 멈출 지점을 찾는다.

1. 요청된 변경이 실제로 필요한가
2. 저장소에 이미 같은 기능이나 패턴이 있는가
3. 표준 라이브러리나 엔진 기본 기능으로 해결되는가
4. 이미 설치된 의존성이 해결하는가
5. 가장 작은 변경으로 관찰 가능한 완료 기준을 만족하는가

보안, 데이터 손실 방지, 입력 검증, 접근성, 사용자가 명시한 요구는 단순화를 이유로 제거하지 않는다. 작은 diff보다 올바른 root cause 위치가 우선이다.

## 5. Context capsule

긴 조사 결과와 파일 전문을 대화에 계속 유지하지 않는다. 실행에 필요한 상태를 아래 capsule로 압축한다.

```md
## Active Context
- Goal:
- User value:
- Decisions:
- Scope:
- Excluded:
- Files:
- Risks:
- Next verification:
```

보존할 것:

- 사용자의 최신 결정
- 정확한 파일 경로, 명령, 버전, 식별자
- 현재 실패 증상과 검증 명령
- 미완료 작업과 blocker
- 저장/보안/호환성 위험

줄일 것:

- 이미 문서에 저장된 원문
- 같은 결론을 반복하는 설명
- 실패한 탐색의 전체 로그
- 적용하지 않기로 한 대안의 장문 설명
- 도구 호출 내역 자체

compact는 조사→계획, 계획→구현, 디버깅 종료→다음 작업처럼 논리적 경계에서 수행한다. 부분 구현 중에는 변수명·파일·상태 손실 위험 때문에 compact하지 않는다. 먼저 capsule과 필요한 결정을 파일에 기록한다.

## 6. 좋은 작업 프롬프트

```md
# Goal
한 문장 목표와 사용자 가치

## Evidence
확인한 Issue, 규칙, 실제 파일, 외부 근거

## Scope
수정할 동작과 파일

## Excluded
하지 않을 기능, 리팩터링, 데이터 변경

## Constraints
규칙 우선순위, 보안, 저장, 호환성

## Completion
조건 → 행동 → 관찰 결과

## Verification
실행할 명령과 수동 확인 경로

## Report
변경 파일, 이유, 검증, 미검증, 위험
```

Issue와 문서에 이미 있는 장문은 반복하지 않는다. 프롬프트에는 구현에 필요한 결정과 검증 기준만 남긴다.

## 7. 검증과 보고

- 버그는 가능하면 실제 증상을 잡는 red-capable command를 먼저 만든다.
- 테스트는 private 구현보다 사용자에게 보이는 seam과 public interface를 검증한다.
- 완료 전 build, type/lint, test, security, diff 중 프로젝트에 존재하는 검증만 실행한다.
- 존재하지 않는 테스트 체계나 도구를 실행한 것처럼 보고하지 않는다.
- 위험한 작업은 압축 문체를 중단하고 대상, 영향, 복구 가능성을 명확히 쓴다.
- 최종 보고는 결과, 변경 이유, 검증 근거, 미검증 항목, 남은 위험 순으로 짧게 쓴다.

## 8. 참고 저장소와 적용 결론

| 저장소 | 가져올 원칙 | 그대로 가져오지 않을 것 |
|---|---|---|
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | YAGNI, 기존 코드·native·stdlib 우선, 최소 diff | 정확성·보안·검증을 줄이는 극단적 축소 |
| [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | filler 제거, 중복 압축, 기술 식별자 보존, 위험 작업의 clarity fallback | 모든 상황에 문장 파편 스타일 강제 |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | brief와 대상 우선, 기존 디자인 감사, variance/motion/density 명시 | 웹 랜딩 페이지 규칙을 운영 UI·게임 UI에 그대로 적용 |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 작은 composable skill, spec→ticket→implementation 산출물 연결, feedback loop | 프로젝트에 없는 issue label·tracker 가정 |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | 전략적 compact, 보안 preflight, verification loop, 역할 분리 | 대형 skill bundle 전체 설치와 고정 80% 기준 강제 |
| [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | 기간 제한, 다중 출처, 최신성·반응·근거 분리, permission preflight | 쿠키·유료 API·외부 저장을 자동 허용 |
| [obra/superpowers](https://github.com/obra/superpowers) | spec-first, systematic debugging, TDD, verification-before-completion | 빠른 수정에도 모든 gate와 산출물을 동일하게 강제 |

외부 저장소의 수치·기능·설치법은 변경될 수 있다. 실제 채택 작업에서는 최신 원본을 다시 확인한다.
