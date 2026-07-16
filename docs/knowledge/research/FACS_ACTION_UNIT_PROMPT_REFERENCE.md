# FACS Action Unit 프롬프트 참고표

- 상태: 참고 자료·모델별 검증 필요
- 목적: 표정 편집 프롬프트에서 얼굴 움직임을 짧게 지정할 때 사용할 용어와 주의점을 정리한다.

## 1. 사용 원칙

FACS는 얼굴 움직임을 관찰해 기록하는 코딩 체계다. 이미지 생성 모델의 공통 프롬프트 프로토콜이 아니다.

따라서 다음처럼 사용한다.

```text
자연어 표정 설명
+ 좌우·강도·시선·머리 방향
+ AU 번호를 보조 표기
+ 원본 정체성 보호
```

나쁜 예:

```text
AU46
```

권장 예:

```text
원본 캐릭터의 얼굴 비율, 안경, 앞머리와 채색을 유지한다.
오른쪽 눈만 자연스럽게 윙크한다. 보조 표기: FACS AU46R.
반대쪽 눈, 눈썹, 입 모양과 머리 방향은 유지한다.
```

한 번 성공한 AU 조합을 다른 모델·캐릭터에서도 동일하게 작동한다고 가정하지 않는다.

## 2. 표준 FACS에서 널리 사용하는 AU·동작 표기

| 코드 | 영문 | 한국어 프롬프트 의미 |
|---:|---|---|
| AU1 | Inner Brow Raiser | 안쪽 눈썹 올리기 |
| AU2 | Outer Brow Raiser | 바깥쪽 눈썹 올리기 |
| AU4 | Brow Lowerer | 눈썹 내리기·미간 모으기 |
| AU5 | Upper Lid Raiser | 윗눈꺼풀 크게 열기 |
| AU6 | Cheek Raiser | 뺨 올리기 |
| AU7 | Lid Tightener | 눈꺼풀 조이기 |
| AU9 | Nose Wrinkler | 코 주름짓기 |
| AU10 | Upper Lip Raiser | 윗입술 올리기 |
| AU11 | Nasolabial Deepener | 비순 고랑 깊게 하기 |
| AU12 | Lip Corner Puller | 입꼬리 올리기 |
| AU13 | Cheek Puffer | 뺨 부풀리기 계열. 일부 비공식 그리드의 `Sharp Lip Puller` 표기와 다름 |
| AU14 | Dimpler | 보조개·입꼬리 안쪽 당기기 |
| AU15 | Lip Corner Depressor | 입꼬리 내리기 |
| AU16 | Lower Lip Depressor | 아랫입술 내리기 |
| AU17 | Chin Raiser | 턱끝 올리기 |
| AU18 | Lip Pucker | 입술 오므리기 |
| AU20 | Lip Stretcher | 입술 옆으로 늘리기 |
| AU22 | Lip Funneler | 입술 깔때기 모양 |
| AU23 | Lip Tightener | 입술 조이기 |
| AU24 | Lip Pressor | 입술 누르기 |
| AU25 | Lips Part | 입술 벌리기 |
| AU26 | Jaw Drop | 턱 내리기 |
| AU27 | Mouth Stretch | 입 크게 벌리기 |
| AU28 | Lip Suck | 입술 안으로 말기 |
| AU41 | Lid Droop | 윗눈꺼풀 처짐 |
| AU42 | Slit | 눈 가늘게 뜨기 |
| AU43 | Eyes Closed | 눈 감기 |
| AU44 | Squint | 눈 찌푸리기 |
| AU45 | Blink | 양쪽 눈 깜박임 |
| AU46 | Wink | 한쪽 눈 윙크 |
| AU51 | Head Turn Left | 머리 왼쪽 회전 |
| AU52 | Head Turn Right | 머리 오른쪽 회전 |
| AU53 | Head Up | 머리 올리기 |
| AU54 | Head Down | 머리 내리기 |
| AU55 | Head Tilt Left | 머리 왼쪽 기울이기 |
| AU56 | Head Tilt Right | 머리 오른쪽 기울이기 |
| AU57 | Head Forward | 머리 앞으로 내밀기 |
| AU58 | Head Back | 머리 뒤로 당기기 |
| AU61 | Eyes Turn Left | 시선 왼쪽 |
| AU62 | Eyes Turn Right | 시선 오른쪽 |
| AU63 | Eyes Up | 시선 위 |
| AU64 | Eyes Down | 시선 아래 |
| AU81 | Chewing | 씹는 동작 |

강도는 FACS 기록에서 A~E로 표현되는 경우가 있다. 이미지 모델에는 `AU12B`처럼 코드만 쓰지 말고 `아주 약하게 입꼬리를 올린다` 같은 자연어를 함께 쓴다.

## 3. 제공된 캐릭터 레퍼런스 그리드의 비표준 별칭

사용자가 제공한 그리드에는 다음과 같은 편집용 별칭이 포함되어 있다.

| 그리드 코드 | 그리드 표기 | 운용 규칙 |
|---:|---|---|
| AU13 | Sharp Lip Puller | 표준 AU13 설명과 다르므로 모델별 별칭으로 취급 |
| AU71 | Brow Furrow | 표준 FACS AU 번호로 확정하지 말고 `미간 주름` 자연어 병기 |
| AU72 | Brow Bulge | 비표준 별칭. `눈썹 주변 부풀림` 자연어 병기 |
| AU82 | Nostril Dilator | 일부 표준 목록의 다른 번호와 충돌 가능. `콧구멍 벌리기`를 우선 사용 |
| AU83 | Nostril Compressor | `콧구멍 좁히기` 자연어를 우선 사용 |
| AU84 | Tongue Up | `혀 올리기` 자연어를 우선 사용 |
| AU85 | Tongue Out | `혀 내밀기` 자연어를 우선 사용 |

이 별칭은 해당 레퍼런스 그리드와 특정 이미지 모델에서 짧은 제어어로 시험할 수 있지만, Base의 표준 FACS 정의로 사용하지 않는다.

## 4. 자주 쓰는 조합 예시

| 목적 | 자연어 + 보조 코드 예시 |
|---|---|
| 가벼운 미소 | 입꼬리를 약하게 올리고 뺨을 조금 올린다. `AU12B + AU6A` |
| 윙크 미소 | 오른쪽 눈만 윙크하고 입꼬리를 가볍게 올린다. `AU46R + AU12B` |
| 걱정 | 안쪽 눈썹을 올리고 입꼬리를 약하게 내린다. `AU1B + AU15A` |
| 놀람 | 눈을 크게 뜨고 턱을 약하게 내린다. `AU1 + AU2 + AU5 + AU26` |
| 집중 | 눈썹을 내리고 눈꺼풀을 약하게 조인다. `AU4B + AU7A` |
| 눈 감은 웃음 | 양쪽 눈을 감고 입꼬리와 뺨을 올린다. `AU43 + AU12 + AU6` |
| 옆을 보는 표정 | 머리와 시선을 같은 방향으로 돌린다. `AU51 + AU61` 또는 `AU52 + AU62` |

## 5. 편집 QA

- [ ] 원본 얼굴 비율과 캐릭터 식별 요소가 유지된다.
- [ ] 변경 요청한 눈·입·머리·시선 외 요소가 불필요하게 바뀌지 않는다.
- [ ] 안경, 앞머리, 속눈썹, 눈썹이 충돌하지 않는다.
- [ ] 좌우 지시가 결과 이미지 기준으로 혼동되지 않는다.
- [ ] 표정 차이가 실제 사용 크기에서 읽힌다.
- [ ] AU 코드 없이도 자연어 설명만으로 의도를 이해할 수 있다.
- [ ] 모델·버전·원본·프롬프트·결과를 기록했다.

## 6. 근거와 한계

- 표준 용어 확인 기준: Carnegie Mellon University의 FACS 요약표와 Ekman·Friesen 계열 FACS 명칭.
- 제공된 여성 캐릭터 레퍼런스 그리드는 이미지 생성용 실험 자료로 취급한다.
- 본 문서는 심리학적 FACS 판정이나 인증을 위한 매뉴얼이 아니다.
- 모델의 AU 코드 이해는 공식 보장 기능이 아닐 수 있으므로 실제 편집 테스트가 필요하다.
