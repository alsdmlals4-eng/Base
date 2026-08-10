# Laws of UX 완전성 매트릭스

> 확인일: 2026-08-10
> 목적: 사용자 제공 31개 항목을 `ui-ux-visual-design-rulebook.md`에 누락 없이 대응시키고, 같은 원칙의 중복·오용을 명시한다.
> 권한: 이 매트릭스는 `auditing-and-refining-ui-art`의 보조 reference다. Rulebook의 `MUST / SHOULD / STYLE_DEFAULT / TEST_REQUIRED`와 프로젝트별 `ADOPT / ADAPT / AVOID / TEST / IGNORE` 판정을 대체하지 않는다.

| # | 원칙 | 기본 Tier | Base 적용 | 오용/충돌 방지 |
|---:|---|---|---|---|
| 1 | Aesthetic-Usability Effect | TEST_REQUIRED | 미적 완성도와 perceived usability를 활용하되 task success와 분리 측정 | 아름다움이 실제 defect를 가릴 수 있음 |
| 2 | Cognitive Bias | TEST_REQUIRED | 판단·레이블·기본값·추천이 특정 편향을 증폭하는지 공격 검토 | confirmation bias 등 편향을 조작/설득 기술로 악용 금지 |
| 3 | Cognitive Load | SHOULD | 현재 목표와 무관한 장식·중복·기억 부담을 줄임 | 장르적 전략 복잡성 자체를 삭제하지 않음 |
| 4 | Selective Attention | SHOULD | 첫 시선·critical cue·primary action의 시각 우선순위 확보 | 모든 요소를 강조해 경쟁시키지 않음 |
| 5 | Working Memory | SHOULD | 비교 정보와 현재 맥락을 화면/시스템이 유지 | Miller `7±2`를 기계적 개수 제한으로 사용 금지 |
| 6 | Choice Overload | SHOULD | filter/search/recommendation/side-by-side 비교로 결정 부담 완화 | 선택 자체가 핵심 재미면 수를 무조건 축소하지 않음 |
| 7 | Hick's Law | SHOULD | 반응 시간이 중요한 순간의 선택 수·복잡성을 낮춤 | 과도한 단순화로 의미/비용/위험을 숨기지 않음 |
| 8 | Mental Model | SHOULD | 기존 플랫폼·장르·프로젝트 관례를 활용 | 새 모델 도입 시 migration/onboarding 없이 급변 금지 |
| 9 | Doherty Threshold | SHOULD | 입력 접수와 처리 상태를 빠르게 보여 perceived latency를 줄임 | `400ms`를 universal SLA로 고정하거나 가짜 지연을 추가하지 않음 |
| 10 | Fitts's Law | SHOULD | 중요·빈번 target을 크게·가깝게, hit region과 간격을 충분히 | visual size와 hit target을 혼동하지 않음 |
| 11 | Flow | TEST_REQUIRED | skill/challenge 균형과 명료한 feedback으로 불필요한 UI friction 제거 | 난이도·긴장·발견을 편의성 하나로 평준화하지 않음 |
| 12 | Goal-Gradient Effect | TEST_REQUIRED | 실제 목표 진행도를 명료하게 표시 | 허위 진행·기만적 사전 채움 금지 |
| 13 | Zeigarnik Effect | TEST_REQUIRED | 미완료 task의 재개 지점과 상태를 기억하기 쉽게 함 | badge pressure·streak anxiety·강박적 retention 금지 |
| 14 | Chunking | SHOULD | heading/spacing/alignment로 의미 단위 그룹화 | 무의미한 카드/컨테이너 남발 금지 |
| 15 | Miller's Law | SHOULD | working memory 부담을 줄이고 recognition을 우선 | 메뉴/탭 항목을 `7±2`로 하드 제한하지 않음 |
| 16 | Serial Position Effect | SHOULD | 중요한 시작·마지막 정보/행동의 기억 우위를 고려 | 실제 task order·focus/read order가 우선 |
| 17 | Law of Common Region | SHOULD | 같은 경계/배경을 실제 관계에 사용 | 장식용 container가 관계를 오도하지 않게 함 |
| 18 | Law of Proximity | SHOULD | 관련 요소는 더 가깝게, 다른 그룹은 더 멀게 | spacing 수치를 의미보다 우선하지 않음 |
| 19 | Law of Prägnanz | SHOULD | shape와 정보 구조를 쉽게 해석할 수 있게 단순화 | 고유 아트·필요한 정보 차이를 없애지 않음 |
| 20 | Law of Similarity | SHOULD | 같은 기능/상태에 같은 시각 문법 | 다른 기능인데 같은 형태를 써 거짓 affordance 생성 금지 |
| 21 | Law of Uniform Connectedness | SHOULD | 실제 연결 관계를 선·프레임·연속성으로 표현 | 관계 없는 요소를 연결해 오해시키지 않음 |
| 22 | Jakob's Law | SHOULD | 다른 제품에서 학습한 관례를 활용 | 관례가 접근성·프로젝트 고유 가치보다 높은 권한을 갖지 않음 |
| 23 | Paradox of the Active User | SHOULD | 매뉴얼을 먼저 읽는다고 가정하지 않고 inline learning·progressive disclosure·undo로 즉시 행동 지원 | tutorial을 없애라는 뜻이 아니며 재열람 가능한 도움 경로 유지 |
| 24 | Peak-End Rule | TEST_REQUIRED | 핵심 peak와 session ending의 clarity/recovery/delight를 다듬음 | 중간의 지속적 불편을 화려한 끝으로 덮지 않음 |
| 25 | Von Restorff Effect | TEST_REQUIRED | 중요한 CTA/critical state를 제한적으로 차별화 | 강조 남용·광고 오인·색상 단독 강조 금지 |
| 26 | Primacy-Recency → Serial Position Effect | SHOULD | 16번의 같은 원칙으로 통합 | 별도 법칙처럼 중복 규칙을 만들지 않음 |
| 27 | Tesler's Law | SHOULD | 시스템이 흡수 가능한 복잡성을 내부 처리 | 사용자가 이해·제어해야 하는 선택까지 숨기지 않음 |
| 28 | Postel's Law | SHOULD | 합리적 입력 변형을 수용하고 출력은 일관 | security/schema/payment/save-format validation을 약화하지 않음 |
| 29 | Occam's Razor | SHOULD | 같은 목표라면 불필요한 가정·컴포넌트·장식 제거 | 단순함 자체를 목표로 핵심 기능/정체성 삭제 금지 |
| 30 | Pareto Principle | TEST_REQUIRED | 실제 사용 데이터가 있을 때 고가치·고빈도 흐름에 우선 투자 | 측정 없이 `80/20`을 사실처럼 가정하지 않음 |
| 31 | Parkinson's Law | TEST_REQUIRED | 명확한 범위·시간 frame이 task 이해를 돕는지 검증 | fake urgency/countdown/압박을 만들지 않음 |

## 완전성 판정

- 사용자 제공 31개 행: `31/31 MAPPED`
- 중복 원칙: `#26 → #16 Serial Position Effect`로 통합
- 명시 보강: `#2 Cognitive Bias`, `#23 Paradox of the Active User`
- 전역 강제 수치로 승격: `0`
- 다크 패턴 정당화에 사용 가능: `0`

## 적용 순서

```text
해결하려는 실제 플레이어 문제
→ 관련 원칙 후보
→ source/evidence type 확인
→ Rulebook tier 확인
→ 프로젝트 코어·플랫폼·입력 충돌 확인
→ ADOPT / ADAPT / AVOID / TEST / IGNORE
→ 실제 렌더·입력·사람 증거
```

원칙 이름이 있다는 이유만으로 적용하지 않는다. 원칙의 목적은 설계 결정을 설명하고 검증 가능한 가설을 만드는 것이며, 실제 사용자 연구·플레이테스트를 대체하지 않는다.
