# Managing Game Project Operating System Learning Log

## 2026-08-05 — 플랫폼 심사·자산 권리·참조 기반 독립 제작

- **상태:** `PATTERN_CANDIDATE`
- **Trigger:** Steam·STOVE·Google Play 출시를 준비하면서 등급 위험, 모든 에셋 범주의 상업·배포 권리, AI·외주 계약, 이미지·사운드 등의 참조 후 독립 제작을 Base 공용 구조에 반영하라는 승인된 요청.
- **Finding:** 기존 출시 Guide, Godot 에셋 평가, 이미지 프롬프트·검수, Vertical Slice와 Evidence Pack에 관련 규칙이 분산돼 있었지만, 직접 포함과 `REFERENCE_TO_ORIGINAL`, 게임 포함 배포와 원본 재배포, 등급과 target audience, 공개 저장소와 민감 계약 원본을 하나의 출시 차단 계약으로 연결하지 못했다.
- **Decision:** 새 광역 Skill을 추가하지 않음. 기존 `managing-game-project-operating-system`, 에셋 평가, 아트 프롬프트, Vertical Slice, 변경 검증 Skill에 공용 Guide와 두 프로젝트 증빙 Template을 연결한다. 등급은 `LOWEST_VIABLE_RATING`과 `AVOID_ADULTS_ONLY`를 사용해 청소년이용불가·18+를 기본 회피하되 전체이용가를 강제하지 않는다.
- **Reference production:** 외부 이미지·사운드·폰트·3D·애니메이션·UI·코드에서 기능·구조·일반 제작 원리만 추출하고, 식별 가능한 표현을 `forbidden_expression`으로 제거한 `reference_brief`에서 별도 최종 자산을 제작한다. 약간 수정하거나 AI로 재생성했다는 사실은 독립성 증거가 아니다.
- **Rights evidence:** `commercial_use`, `distribution_in_game_build`, `raw_source_redistribution`, 수정·고지·NOTICE·AI 약관·외주 범위를 분리하며, 필수 증거가 없으면 `RELEASE_BLOCKED_UNVERIFIED`다.
- **Security boundary:** 공개 저장소에 unredacted 계약·신분증·서명·결제·개인정보를 넣지 않고 최소 metadata·hash·검토 결과와 `secure_original_location`만 둔다.
- **Automation boundary:** 자동 법률 판정기를 추가하지 않음. 파일·hash·설문 필드로 실제 권리, 침해 유사성, 법률 clearance나 플랫폼 승인을 자동 확정할 수 없으므로 자동 검사는 누락과 상태 불일치만 차단한다.
- **Evidence:** PR #163의 focused RED에서 기존 167개 테스트 중 새 Guide·Template·라우팅 부재만 실패했다. 구현 뒤 exact-head GREEN, 전체 회귀, 참조 최신성, 독립 검토는 별도 완료 증거로 기록한다.
- **Boundary:** 실제 프로젝트 자산 감사, runtime 사용, store·build 비교, 법률 검토, 등급 제출과 플랫폼 승인은 `NOT_RUN`이며 Template·정적 테스트로 대체하지 않는다.
- **Next trigger:** 여러 프로젝트에서 동일한 누락 패턴이 반복되고 구조화 입력으로 안전하게 검사 가능한 항목이 확인될 때만 전용 자동 validator 또는 별도 Skill 책임을 재검토한다.
