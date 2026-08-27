# Visual Concept Comparison → Direction Lock → Consistent Production 사례

```text
USER_PROVIDED_COMPARISON_EXAMPLES_REVIEWED
CONCEPT_OPTIONS_BEFORE_SCALE
SELECTED_DIRECTION_IS_A_DECISION_NOT_A_VIBE
FLOW_AND_STYLE_ANCHORS_PREVENT_PRODUCTION_DRIFT
COMPARISON_BOARD_IS_NOT_RUNTIME_ASSET_DELIVERY
```

## 1. 출처와 evidence ceiling

2026-08-27 사용자가 이미지 작업 초기에 여러 컨셉·그림체 예시를 먼저 비교하고 하나를 확정한 뒤, 확정된 컨셉시안·Flow map을 기준으로 분위기와 그림체의 일관성을 유지해 달라고 요청했다.

사용자가 제공한 이미지는 두 비교 패턴을 보여준다.

1. **동일 gameplay board/surface의 환경·분위기 비교**
   - 왕실 전술 홀/전략실
   - 고대 투기장
   - 마법 전술 성소
   - 전쟁 지휘실
   - 기본 보드·카메라·카드 영역은 비슷하게 두고 건축·광원·재질·분위기를 바꿔 비교한다.

2. **Pixel Art style family 비교**
   - Anime Pixel Art
   - Cluster-based / Clean Pixel Art
   - HD Pixel Art 등
   - 캐릭터 비례, 픽셀 클러스터, 렌더 밀도, 배경 표현과 팔레트 차이를 나란히 판독한다.

이 사례는 사용자가 제공한 **workflow evidence**다. 이미지 자체의 출처·권리·프로젝트 소속·제품 사용 승인을 Base가 추정하지 않으며 Base repository에 binary를 복제하지 않는다.

## 2. 기존 Base에서 이미 잘 작동하던 것

- Art Direction Guide는 Concept Exploration에서 서로 다른 방향 3개 안팎과 동일 조건 비교를 요구했다.
- Image policy는 actual consumer, candidate lifecycle, Visual continuity, runtime validation을 분리했다.
- Conversation Gate는 text brief 뒤 사용자 승인 1회당 한 생성 결과만 허용했다.
- Candidate review는 실제 역할·가독성·identity·implementation fitness로 후보를 비교했다.
- Continuity gate는 Project relation과 Keep/Avoid/Do Not Drift를 보존했다.
- Local Visual profile은 approved style anchor를 Codex와 runtime acceptance에 전달할 수 있었다.

즉 기능이 없었던 것이 아니라 **탐색 → 선택 → 방향 잠금 → 일관된 production**의 전이 receipt가 분산돼 있었다.

## 3. 확인된 실패 모드

### 3.1 Final-first production

```text
첫 이미지 생성
→ 그럴듯함
→ 사실상 Art Direction으로 취급
→ 같은 방향으로 대량 생산
→ 후속 화면에서 사용자 선호/가독성/제작성 불일치 발견
→ 대량 재작업
```

한 장이 예쁘다는 사실은 장기 production 방향이 맞다는 증거가 아니다.

### 3.2 Fake alternatives

- 사실상 같은 구도·스타일에 색만 조금 다른 후보
- 이름만 A/B/C로 바꾼 후보
- 추천안 하나와 의도적으로 약한 들러리 둘

이런 후보는 사용자의 실질 선택을 돕지 않는다.

### 3.3 Confounded comparison

후보마다 카메라, 캐릭터 수, 조명, UI 양, 배경 복잡도가 모두 다르면 무엇 때문에 더 좋아 보이는지 판단할 수 없다.

```text
SAME_CONSUMER_CONTROLLED_COMPARISON
CONTROLLED_VARIABLE_COMPARISON_REQUIRED
```

가능한 범위에서 기본 소비처·프레이밍·정보량을 유지하고 선언한 축만 바꿔야 한다.

### 3.4 Comparison board delivery compression

여러 option panel이 있는 비교 시트 한 장은 방향 선택에는 유효할 수 있다. 그러나 이것을 여러 독립 gameplay 배경·캐릭터·아이콘의 납품으로 계산하면 실제 source asset, crop, alpha, resolution과 runtime slot이 사라진다.

```text
comparison board = one exploration result
comparison board != N independent runtime assets
```

### 3.5 Vague selection

“이 느낌으로”만 승인하면 후속 작업자가 무엇을 유지하고 무엇을 바꿀 수 있는지 알 수 없다.

필요한 기록:

- selected candidate
- adopted elements
- rejected elements
- selection reason
- confirmed Flow/Screen anchor
- Keep / Avoid / Do Not Drift
- allowed variation

### 3.6 Rigid sameness

일관성은 모든 지역·캐릭터·진영을 같은 색과 장식으로 만드는 것이 아니다. 너무 엄격하면 정보 구분과 세계 확장이 약해진다.

```text
shared visual grammar
+ intentional bounded variation
```

예를 들어 같은 픽셀 밀도·카메라·명도 위계·UI family를 공유하면서 장소별 재질·색·상징을 달리할 수 있다.

### 3.7 Unbounded drift

반대로 `allowed variation`이 무제한이면 lock이 아무것도 보호하지 않는다. protected identity와 공통 문법을 벗어난 변화는 새 방향 결정 또는 affected-scope revalidation이 필요하다.

### 3.8 Stale Flow/Screen anchor

기획 Flow가 바뀌었는데 과거 screen concept을 계속 기준으로 쓰면 실제 runtime과 이미지는 다른 제품을 설명한다.

```text
VISUAL_DIRECTION_OR_FLOW_DRIFT_REVALIDATION_REQUIRED
```

## 4. 채택한 구조

```text
actual consumer와 시각 결정 질문
→ 3개 안팎의 실질 후보 또는 가능한 유효 후보 수
→ 같은 조건의 controlled comparison
→ 명시적 comparison board 또는 독립 candidate
→ user selection
→ CONCEPT_DIRECTION_SELECTION
→ APPROVED_VISUAL_DIRECTION_PACKET
→ confirmed Flow/Screen anchor
→ 후속 local Visual/Codex packet
→ target-size/runtime consistency review
```

Base에는 project-specific Art Bible을 복제하지 않고 다음 thin contract만 추가한다.

```text
docs/knowledge/game-development/VISUAL_CONCEPT_EXPLORATION_AND_CONTINUITY_LOCK.md
```

## 5. Comparison board와 Conversation Gate

비교 board를 생성하려면 기존 Image Conversation Approval Gate를 그대로 따른다.

```text
text brief에 후보 수·고정 조건·변경 축·exploration 상태 명시
→ 다음 사용자 메시지 승인
→ board 1개 생성
→ stop
```

한 board는 명시적으로 요청된 하나의 exploration artifact다. 생성 뒤 사용자가 방향을 선택하기 전 다음 production batch로 자동 진행하지 않는다.

## 6. Selection/Lock의 실제 가치

### 작업 전

```text
reference / concept image
→ 각 작업자가 주관적으로 '비슷하게' 해석
→ 캐릭터·환경·UI·VFX가 서로 drift
```

### 작업 후

```text
selected candidate + adopted/rejected elements
→ mood/style/palette/light/camera
→ confirmed Flow/Screen anchors
→ Keep/Avoid/Do Not Drift/allowed variation
→ production acceptance
→ runtime consistency validation
```

### 기대효과

- 방향 오류를 대량 production 전에 발견
- 사용자의 시각 선호와 제품 역할을 구분해 기록
- 새 Work/Codex가 과거 채팅 없이 같은 기준을 복원
- 환경·캐릭터·UI·VFX가 같은 프로젝트로 인지됨
- 필요한 지역/진영 변주는 유지
- stale Flow와 asset drift의 영향 범위를 좁게 재검증

## 7. 문제→해결→교훈

```yaml
Incident:
  symptom: concept candidate와 continuity rule은 있었지만 selection-to-production lock 전이가 분산됨
  root_cause: 여러 current owner의 책임은 존재했으나 공통 receipt와 route가 없었음
  rejected_fix:
    - 이미지 정책 전체에 Art Bible 세부 절차 복제
    - 프로젝트별 기존 Visual 상태 일괄 migration
    - 모든 이미지마다 후보 3개 강제
  solution: current owner를 조합하는 thin transition contract + continuity gate route + regression test
  recurrence_guard:
    - controlled candidates
    - explicit comparison-board boundary
    - selection and lock packet
    - local Visual packet mapping
    - bounded drift reopen
```

핵심 교훈:

```text
OPTION_COUNT_WITHOUT_CONTROLLED_COMPARISON_IS_NOT_REAL_EXPLORATION
A_SELECTED_IMAGE_WITHOUT_ADOPT_REJECT_RULES_IS_NOT_A_DURABLE_DIRECTION
STYLE_CONSISTENCY_NEEDS_ALLOWED_VARIATION
A_COMPARISON_BOARD_IS_DECISION_SUPPORT_NOT_PRODUCT_BYTES
FLOW_DRIFT_MUST_INVALIDATE_AFFECTED_VISUAL_EVIDENCE
```

## 8. Adversarial review checklist

- 후보가 실질적으로 다른가
- 같은 소비처와 조건을 비교하는가
- board가 runtime asset을 압축하지 않는가
- pseudo-text가 의미 owner가 되지 않는가
- 사용자 선택·채택·비채택 이유가 기록됐는가
- confirmed Flow/Screen만 anchor인가
- 후속 asset이 lock ID를 실제 소비하는가
- allowed variation과 Do Not Drift가 함께 있는가
- target-size/runtime에서 검증하는가
- drift가 생기면 가장 이른 affected scope만 reopen하는가
- candidate/asset/runtime/Human evidence를 분리하는가
- reference rights와 project identity를 보존하는가

## 9. Evidence ceiling

이 사례는 공용 Visual production workflow를 설명한다.

```text
process contract exists
!= actual project concept selected
!= image quality PASS
!= PROJECT_ASSET_APPROVED
!= runtime consistency PASS
!= Human usability / Player Experience PASS
```
