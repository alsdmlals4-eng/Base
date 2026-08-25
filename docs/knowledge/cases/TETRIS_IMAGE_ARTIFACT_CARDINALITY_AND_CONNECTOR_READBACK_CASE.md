# 사례 — Tetris 이미지 산출물 수량·Notion connector readback

- 출처 프로젝트·벤치마킹: `alsdmlals4-eng/Tetris`
- 확인 날짜: 2026-08-25
- 작성 상태: 부분 검증
- 주제: 생성 이미지 산출물 수량 계약, 승인/폐기 reference 분리, connector capability 재탐색, live handoff readback

## 1. 문제

한 이미지 제작 세션에서 서로 다른 네 종류의 운영 실패가 같은 원인 계열로 연결됐다.

1. 이전에 성공한 Notion 이미지 업로드 경로가 있었는데도 capability를 재탐색하지 않고 `직접 업로드 불가`라고 잘못 판단했다.
2. 사용자가 `3장씩`, 각기 다른 목적의 독립 이미지를 요청했는데 생성 결과가 세 번 연속 합본 UI concept sheet로 drift했다.
3. Home의 최신 승인 스타일과 Visual Bible의 이전 스타일 권위가 동시에 남아 새 채팅에서 서로 다른 정본을 읽을 위험이 생겼다.
4. 대화 handoff만 신뢰하면 live GitHub/Notion 상태와 어긋날 수 있었다.

## 2. 맥락과 제약

- 사용자·플레이어 경험: 사용자는 이미지 결과를 직접 검수하며 그림체와 UI 방향을 점진적으로 잠갔다.
- 플랫폼·장르: 게임 제작 프로젝트의 AI-assisted concept art / UI / asset workflow.
- 일정·예산·팀: 반복 생성 비용과 style drift를 줄여야 하는 소규모 제작 흐름.
- 기술·성능: ChatGPT image generation + Notion/GitHub connected tools. Connector capability는 세션 노출 상태와 action discovery에 따라 달라질 수 있다.
- 권리·출처: 프로젝트 고유 이미지와 설정은 Base에 복제하지 않고 운영 교훈만 일반화한다.

## 3. 관찰 근거

- 직접 확인한 자료:
  - Tetris Notion Home에 이전 업로드된 손그림 판타지 UI 이미지가 실제 image block으로 readback 됨.
  - Notion `create-attachment` action을 재탐색해 Markdown attachment를 실제 업로드하고 새 handoff page에 부착함.
  - 3개 독립 이미지 요청에서 생성된 3개 결과가 모두 목적 분리 대신 UI 합본 sheet로 나왔고 사용자가 즉시 문제를 지적함.
  - Tetris Home과 Visual Bible 사이에 current visual authority 충돌이 실제로 존재함.
- 1차 출처: Tetris GitHub/Notion project authority와 해당 세션의 실제 connector invocation/readback.
- 사용자 반응: 합본 결과를 정식 시안으로 인정하지 않고 독립 산출물로 다시 작업하기로 결정. 이후 인수인계 시 Base 승격 및 문제-교훈 기록을 요청.
- 아직 확인하지 못한 항목:
  - `3 independent requests → 3 independent artifacts` gate를 적용한 다음 실제 이미지 배치의 성공률.
  - 동일 connector 재탐색 규칙이 다른 서비스/프로젝트에서도 같은 방식으로 재현되는지.

## 4. 검토한 대안

### 대안 A — 대화 상태만 믿고 계속 진행

- 장점: 가장 빠르다.
- 단점: stale state, capability 오판, 승인/폐기 reference 혼입 위험이 크다.
- 제외 또는 채택 이유: 제외. 실제로 stale visual authority와 upload capability 오판이 발생했다.

### 대안 B — 매 재개/실패 시 live authority + connector action을 다시 읽고 artifact contract를 명시

- 장점: 잘못된 불가 선언과 stale handoff를 줄이고, 다중 이미지 작업의 산출물 단위를 검증할 수 있다.
- 단점: 짧은 readback/discovery 비용이 추가된다.
- 제외 또는 채택 이유: 채택. Notion action rediscovery와 readback으로 실제 capability를 복구했고 handoff authority 충돌도 수정했다.

## 5. 결정

```text
resume or capability doubt
→ live source-of-truth fetch
→ if equivalent action succeeded before: rediscover connector action
→ invoke before declaring unavailable
→ readback

N independent requested artifacts
→ write N one-purpose artifact contracts
→ generate
→ verify artifact count == N
→ verify purpose isolation per artifact
→ classify APPROVED / REFERENCE_ONLY / REJECTED
→ only approved references feed the next batch
```

- 채택한 이유: 실패가 대부분 `추정 → 바로 실행/불가 선언`에서 발생했고, live readback과 산출물 단위 검수가 직접적인 방지책이었다.
- 적용 범위: AI image generation, 파일/문서 connector upload, 다중 산출물 batch, chat-to-chat handoff.
- 제외 범위: 특정 이미지 모델의 prompt 문법, Tetris 고유 art direction, 특정 Notion page ID나 파일 경로.

## 6. 결과

- 실제 결과:
  - Notion upload capability를 재탐색해 attachment upload + page attachment에 성공.
  - Tetris Notion Home, Visual Bible, P0 image package, handoff page를 같은 현재 visual authority로 동기화함.
  - 프로젝트 GitHub에 image-work handoff를 별도 문서로 기록함.
- 측정·테스트:
  - Notion page fetch에서 기존 style-anchor image block이 실제 반환됨.
  - 새 handoff page read/write 경로가 connector에서 성공함.
- 실패·부작용:
  - 초기 capability 오판.
  - 독립 3장 요청을 합본으로 생성한 세 번의 artifact-purpose failure.
- 미검증:
  - image artifact cardinality gate를 적용한 후속 3장 배치의 실제 성공.
  - 다중 프로젝트에서의 반복 검증.

## 7. 재사용 가능한 원칙

- 다른 프로젝트에서도 사용할 수 있는 판단 원리:
  - **REUSE-SUCCESS-BEFORE-UNAVAILABLE**: 이전 동등 작업 성공 증거가 있으면 capability 부재를 선언하기 전에 action을 재탐색하고 실제 호출을 시도한다.
  - **ARTIFACT-CARDINALITY-GATE**: N개의 독립 산출물 요청은 N개의 독립 파일/이미지로 검증한다.
  - **PURPOSE-ISOLATION-BEFORE-AESTHETICS**: 다중 자산 batch는 미감보다 먼저 각 자산이 한 목적만 수행하는지 검사한다.
  - **STYLE-ANCHOR-LOCK**: 탐색 종료 후 승인 reference 하나를 style anchor로 명시해 다음 batch와 새 채팅의 drift를 줄인다.
  - **APPROVED-REFERENCE-SEPARATION**: 승인 / 참고 / 폐기 reference를 섞지 않는다.
  - **LIVE-REFETCH-ON-RESUME**: 새 채팅/세션 재개 시 handoff만 믿지 않고 GitHub/Notion 등 현재 authority를 다시 읽는다.
  - **WRITE-THEN-READBACK**: connector write는 성공 응답만으로 끝내지 않고 필요한 경우 실제 대상 readback으로 durable state를 확인한다.
- 체크리스트로 바꿀 항목:
  - `prior equivalent success?`
  - `connector action rediscovered?`
  - `requested artifact count == delivered artifact count?`
  - `one purpose per artifact?`
  - `approved/reference/rejected classified?`
  - `current canon owners synchronized?`
  - `post-write readback completed?`
- methods 또는 skills 승격 후보:
  - `AI_ART_PROMPT_TECHNIQUE_METHOD`의 batch artifact gate.
  - `PROJECT_HANDOFF_CONTEXT_METHOD`의 live-refetch-on-resume.
  - connector/tool routing skill의 reuse-success-before-unavailable + write-then-readback.

현재는 한 프로젝트의 부분 검증 사례이므로 즉시 범용 `검증` rule로 승격하지 않는다. 같은 조건의 다른 프로젝트에서 재현되면 method/skill 승격을 검토한다.

## 8. 그대로 복사하면 안 되는 요소

- 프로젝트 특화 수치·세계관·자산: Tetris의 Vanguard, Gatebreaker, UI layout, style name/decision ID, 특정 image file.
- 다른 전제에서 실패할 조건: 사용자가 실제로 합본 concept sheet를 원하는 경우 artifact-purpose isolation은 다른 계약이 된다. Connector가 명백하게 설치되지 않았거나 권한이 거부된 경우 prior success가 현재 capability를 보장하지 않는다.
- 권리·라이선스 주의: 프로젝트 생성 이미지를 Base sample asset으로 복제하지 않는다.

## 9. 검증 방법

- 자동 검증:
  - text/file workflow에서는 요청 산출물 목록과 실제 artifact manifest cardinality 비교 가능.
  - connector workflow에서는 write response 뒤 target fetch/readback 결과 확인 가능.
- 수동 검증:
  - 이미지 batch에서 각 artifact가 지정된 한 목적만 수행하는지 시각 검수.
  - 새 채팅이 handoff + live source fetch만으로 동일한 approved/rejected reference set을 재구성할 수 있는지 확인.
- 사용자 테스트:
  - 다음 3장 이미지 batch를 artifact-cardinality gate로 생성한 뒤 사용자가 목적 분리가 맞는지 검수.
- 후속 질문:
  - 두 번째 프로젝트에서도 connector capability 재탐색과 artifact gate가 동일한 실패를 방지하는가?

## 10. 관련 문서

- Base 방법:
  - `docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md`
  - `docs/knowledge/methods/AI_ART_PROMPT_TECHNIQUE_METHOD.md`
- Base 스킬:
  - `skills/managing-project-intake-and-work-contract/SKILL.md`
  - `skills/reviewing-and-validating-project-changes/SKILL.md`
- 프로젝트 책임 원본:
  - Tetris `docs/operations/image-work/2026-08-25_IMAGE_WORK_HANDOFF.md`
  - Tetris Notion `Tetris · Home`, `02 · 비주얼 바이블`, `14 · P0 이미지 제작 패키지`, `17 · 이미지 작업 인수인계 · 2026-08-25`
- 외부 출처: 없음. 이번 사례는 프로젝트 실행·connector readback에서 직접 추출한 운영 교훈이다.
