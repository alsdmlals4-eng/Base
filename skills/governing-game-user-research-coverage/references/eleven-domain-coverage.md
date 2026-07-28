# Games User Research 11영역 계약

각 영역은 `owner / canonical_source / question / method / sample_or_version / evidence / status / finding / implication / decision / limitation / next_check`를 가진다.

상태는 `NOT_STARTED / PLANNED / IN_PROGRESS / EVIDENCE_COLLECTED / SYNTHESIZED / VERIFIED / NOT_APPLICABLE / BLOCKED`로 구분한다.

- 시장·장르: 시장 약속, 대상층, 가격·운영, 지역·플랫폼.
- 벤치마킹·경쟁: 비교 차원, 작동 원리, 실패 조건, 차별화.
- SWOT: S/W/O/T를 SO/WO/ST/WT 행동으로 연결.
- 사용자 조사: 대상 세그먼트, 질문, 표본, 편향.
- 플레이테스트: 빌드·과제·관찰·피드백.
- 튜토리얼: 첫 행동·이해·오입력·이탈.
- UX: 목표·막힘·정보 위계·접근성.
- 텔레메트리: 이벤트 정의, 퍼널, 버전, 누락 데이터.
- 밸런스: 분포, 승률·사용률, 경제 흐름, 이상치.
- 가설·실험: 사전 가설, 변형, 지표, 결과, 한계.
- 개선·결정: 채택·변형·제외·보류와 근거·재검토 조건.

## 사람 검증 Artifact 조건부 라우팅

작은 표본, 카드·종이·클릭 Mock, 기존 PoC overlay, simulated recognition, scripted outcome, fixed RNG 결과를 사용하는 사람 검증 계획은 다음을 함께 읽는다.

- Governance: `docs/knowledge/game-development/HUMAN_VALIDATION_ARTIFACT_GOVERNANCE.md`
- Session Packet: `templates/research/HUMAN_VALIDATION_SESSION_PACKET.md`

이 경로에서는 다음을 분리한다.

- Artifact fidelity와 `claim_ceiling`.
- simulated·scripted·fixed 구성요소와 실제 제품 구성요소.
- 피드백 전 `first_attempt`와 피드백 후 `post_feedback_attempt`.
- 행동 관찰·플레이어 자기보고·진행자 개입·실제 로그.
- 작은 표본의 분자/분모·반복 결함·심각도 높은 반례·경험군 차이.
- 미실행 제품·기기·접근성·성능·알고리즘 검증.

작은 표본의 기본 판정은 `PROMISING_DIRECTION / ADAPT / REWORK / REJECT / STOP`이다. 실제 제품 또는 목표 fidelity Build의 반복 증거와 프로젝트 승인 전에는 자동 `ADOPT`를 사용하지 않는다.
