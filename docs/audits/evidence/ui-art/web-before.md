# UI 아트 정적 감사 후보

> 이 보고서는 정적 패턴 후보이며 결함 확정이나 자동 수정 지시가 아닙니다.

- 검사 루트: `before`
- 어댑터: web
- 검사 파일: 2
- 후보: 25
- 사유 있는 제외: 0

## Findings

### web-a-w-a-decorative-effect-96faafc3ce

- 영역/어댑터: A / web
- 심각도/신뢰도: MEDIUM / MEDIUM
- 위치: `style.css:4`
- 관찰: `.orb { position: absolute; width: 640px; height: 640px; right: -130px; top: -170px; border-radius: 50%; background: radial-gradient(circle, #b52cff99, #45137722 55%, transparent 72%); filter: blur(20px); }`
- 위험: 반복 장식이 정보 계층이나 상호작용 상태와 경쟁할 수 있다.
- 제안: 아트 방향과 실행 화면에서 효과의 목적을 확인하고 승인된 경우에만 강도·범위·사용 횟수를 조정한다.
- 검증: 승인된 화면에서 효과가 지정된 강조 대상에만 쓰이고 정보 판독을 방해하지 않는지 렌더로 확인한다.
- 상태: CANDIDATE

### web-a-w-a-decorative-effect-fe9a8b5eaf

- 영역/어댑터: A / web
- 심각도/신뢰도: MEDIUM / MEDIUM
- 위치: `style.css:5`
- 관찰: `.hero { position: absolute; width: 920px; left: 130px; top: 84px; padding: 29px; border: 1px solid #ffffff33; border-radius: 22px; background: linear-gradient(145deg, #ffffff16, #8c3aff0d); backdrop-filter: blur(24px); box-shadow: 0 24px 80`
- 위험: 반복 장식이 정보 계층이나 상호작용 상태와 경쟁할 수 있다.
- 제안: 아트 방향과 실행 화면에서 효과의 목적을 확인하고 승인된 경우에만 강도·범위·사용 횟수를 조정한다.
- 검증: 승인된 화면에서 효과가 지정된 강조 대상에만 쓰이고 정보 판독을 방해하지 않는지 렌더로 확인한다.
- 상태: CANDIDATE

### web-a-w-a-decorative-effect-a55823cfc2

- 영역/어댑터: A / web
- 심각도/신뢰도: MEDIUM / MEDIUM
- 위치: `style.css:7`
- 관찰: `h1 { margin: 5px 0; font-size: 58px; font-style: italic; background: linear-gradient(90deg, #fff, #d156ff); background-clip: text; color: transparent; }`
- 위험: 반복 장식이 정보 계층이나 상호작용 상태와 경쟁할 수 있다.
- 제안: 아트 방향과 실행 화면에서 효과의 목적을 확인하고 승인된 경우에만 강도·범위·사용 횟수를 조정한다.
- 검증: 승인된 화면에서 효과가 지정된 강조 대상에만 쓰이고 정보 판독을 방해하지 않는지 렌더로 확인한다.
- 상태: CANDIDATE

### web-a-w-a-decorative-effect-6425b24b3e

- 영역/어댑터: A / web
- 심각도/신뢰도: MEDIUM / MEDIUM
- 위치: `style.css:10`
- 관찰: `.cards article { height: 150px; padding: 17px; border: 1px solid #fff2; border-radius: 18px; background: #ffffff0c; box-shadow: 0 12px 36px #0007; }`
- 위험: 반복 장식이 정보 계층이나 상호작용 상태와 경쟁할 수 있다.
- 제안: 아트 방향과 실행 화면에서 효과의 목적을 확인하고 승인된 경우에만 강도·범위·사용 횟수를 조정한다.
- 검증: 승인된 화면에서 효과가 지정된 강조 대상에만 쓰이고 정보 판독을 방해하지 않는지 렌더로 확인한다.
- 상태: CANDIDATE

### web-a-w-a-decorative-effect-54a731f9d1

- 영역/어댑터: A / web
- 심각도/신뢰도: MEDIUM / MEDIUM
- 위치: `style.css:14`
- 관찰: `button { padding: 13px 29px; border: 0; border-radius: 999px; color: #fff; background: linear-gradient(90deg, #7b2dff, #dd39ff); box-shadow: 0 10px 28px #a22eff66; font-weight: 700; }`
- 위험: 반복 장식이 정보 계층이나 상호작용 상태와 경쟁할 수 있다.
- 제안: 아트 방향과 실행 화면에서 효과의 목적을 확인하고 승인된 경우에만 강도·범위·사용 횟수를 조정한다.
- 검증: 승인된 화면에서 효과가 지정된 강조 대상에만 쓰이고 정보 판독을 방해하지 않는지 렌더로 확인한다.
- 상태: CANDIDATE

### web-b-w-b-fixed-layout-ffd9fcee7c

- 영역/어댑터: B / web
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `style.css:3`
- 관찰: `.shell { position: relative; width: 1180px; height: 720px; margin: auto; overflow: hidden; }`
- 위험: 고정 크기나 절대 위치가 콘텐츠·번역·viewport 변화에서 구조를 깨뜨릴 수 있다.
- 제안: 해당 고정값의 연출 목적을 확인하고 필요하면 flow, flex, grid 또는 유연한 제약으로 바꾼다.
- 검증: 대표 viewport와 긴 콘텐츠에서 겹침·잘림·가로 스크롤이 없는지 확인한다.
- 상태: CANDIDATE

### web-b-w-b-fixed-layout-630132820a

- 영역/어댑터: B / web
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `style.css:4`
- 관찰: `.orb { position: absolute; width: 640px; height: 640px; right: -130px; top: -170px; border-radius: 50%; background: radial-gradient(circle, #b52cff99, #45137722 55%, transparent 72%); filter: blur(20px); }`
- 위험: 고정 크기나 절대 위치가 콘텐츠·번역·viewport 변화에서 구조를 깨뜨릴 수 있다.
- 제안: 해당 고정값의 연출 목적을 확인하고 필요하면 flow, flex, grid 또는 유연한 제약으로 바꾼다.
- 검증: 대표 viewport와 긴 콘텐츠에서 겹침·잘림·가로 스크롤이 없는지 확인한다.
- 상태: CANDIDATE

### web-b-w-b-fixed-layout-2a333567c5

- 영역/어댑터: B / web
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `style.css:5`
- 관찰: `.hero { position: absolute; width: 920px; left: 130px; top: 84px; padding: 29px; border: 1px solid #ffffff33; border-radius: 22px; background: linear-gradient(145deg, #ffffff16, #8c3aff0d); backdrop-filter: blur(24px); box-shadow: 0 24px 80`
- 위험: 고정 크기나 절대 위치가 콘텐츠·번역·viewport 변화에서 구조를 깨뜨릴 수 있다.
- 제안: 해당 고정값의 연출 목적을 확인하고 필요하면 flow, flex, grid 또는 유연한 제약으로 바꾼다.
- 검증: 대표 viewport와 긴 콘텐츠에서 겹침·잘림·가로 스크롤이 없는지 확인한다.
- 상태: CANDIDATE

### web-b-w-b-fixed-layout-79fb286892

- 영역/어댑터: B / web
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `style.css:8`
- 관찰: `.intro { width: 520px; font-size: 13px; line-height: 1.5; }`
- 위험: 고정 크기나 절대 위치가 콘텐츠·번역·viewport 변화에서 구조를 깨뜨릴 수 있다.
- 제안: 해당 고정값의 연출 목적을 확인하고 필요하면 flow, flex, grid 또는 유연한 제약으로 바꾼다.
- 검증: 대표 viewport와 긴 콘텐츠에서 겹침·잘림·가로 스크롤이 없는지 확인한다.
- 상태: CANDIDATE

### web-b-w-b-fixed-layout-ed7c40f257

- 영역/어댑터: B / web
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `style.css:10`
- 관찰: `.cards article { height: 150px; padding: 17px; border: 1px solid #fff2; border-radius: 18px; background: #ffffff0c; box-shadow: 0 12px 36px #0007; }`
- 위험: 고정 크기나 절대 위치가 콘텐츠·번역·viewport 변화에서 구조를 깨뜨릴 수 있다.
- 제안: 해당 고정값의 연출 목적을 확인하고 필요하면 flow, flex, grid 또는 유연한 제약으로 바꾼다.
- 검증: 대표 viewport와 긴 콘텐츠에서 겹침·잘림·가로 스크롤이 없는지 확인한다.
- 상태: CANDIDATE

### web-c-w-c-irregular-spacing-d211efee9f

- 영역/어댑터: C / web
- 심각도/신뢰도: MEDIUM / MEDIUM
- 위치: `style.css:5`
- 관찰: `.hero { position: absolute; width: 920px; left: 130px; top: 84px; padding: 29px; border: 1px solid #ffffff33; border-radius: 22px; background: linear-gradient(145deg, #ffffff16, #8c3aff0d); backdrop-filter: blur(24px); box-shadow: 0 24px 80`
- 위험: 간격 값이 반복 가능한 리듬보다 임시 미세조정에 의존할 수 있다.
- 제안: 주변 관계와 간격 체계를 대조해 의도 없는 예외만 승인 후 토큰이나 공통 단계로 정렬한다.
- 검증: 수정된 간격이 인접 요소의 관계를 명확히 하고 두 viewport에서 같은 리듬을 유지하는지 확인한다.
- 상태: CANDIDATE

### web-c-w-c-irregular-spacing-990fa4809c

- 영역/어댑터: C / web
- 심각도/신뢰도: MEDIUM / MEDIUM
- 위치: `style.css:9`
- 관찰: `.cards { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 17px; margin: 29px 0; }`
- 위험: 간격 값이 반복 가능한 리듬보다 임시 미세조정에 의존할 수 있다.
- 제안: 주변 관계와 간격 체계를 대조해 의도 없는 예외만 승인 후 토큰이나 공통 단계로 정렬한다.
- 검증: 수정된 간격이 인접 요소의 관계를 명확히 하고 두 viewport에서 같은 리듬을 유지하는지 확인한다.
- 상태: CANDIDATE

### web-c-w-c-irregular-spacing-489d46289c

- 영역/어댑터: C / web
- 심각도/신뢰도: MEDIUM / MEDIUM
- 위치: `style.css:10`
- 관찰: `.cards article { height: 150px; padding: 17px; border: 1px solid #fff2; border-radius: 18px; background: #ffffff0c; box-shadow: 0 12px 36px #0007; }`
- 위험: 간격 값이 반복 가능한 리듬보다 임시 미세조정에 의존할 수 있다.
- 제안: 주변 관계와 간격 체계를 대조해 의도 없는 예외만 승인 후 토큰이나 공통 단계로 정렬한다.
- 검증: 수정된 간격이 인접 요소의 관계를 명확히 하고 두 viewport에서 같은 리듬을 유지하는지 확인한다.
- 상태: CANDIDATE

### web-c-w-c-irregular-spacing-879bd3922f

- 영역/어댑터: C / web
- 심각도/신뢰도: MEDIUM / MEDIUM
- 위치: `style.css:12`
- 관찰: `.cards h2 { font-size: 19px; margin: 23px 0 7px; }`
- 위험: 간격 값이 반복 가능한 리듬보다 임시 미세조정에 의존할 수 있다.
- 제안: 주변 관계와 간격 체계를 대조해 의도 없는 예외만 승인 후 토큰이나 공통 단계로 정렬한다.
- 검증: 수정된 간격이 인접 요소의 관계를 명확히 하고 두 viewport에서 같은 리듬을 유지하는지 확인한다.
- 상태: CANDIDATE

### web-c-w-c-irregular-spacing-6b24df6eb4

- 영역/어댑터: C / web
- 심각도/신뢰도: MEDIUM / MEDIUM
- 위치: `style.css:14`
- 관찰: `button { padding: 13px 29px; border: 0; border-radius: 999px; color: #fff; background: linear-gradient(90deg, #7b2dff, #dd39ff); box-shadow: 0 10px 28px #a22eff66; font-weight: 700; }`
- 위험: 간격 값이 반복 가능한 리듬보다 임시 미세조정에 의존할 수 있다.
- 제안: 주변 관계와 간격 체계를 대조해 의도 없는 예외만 승인 후 토큰이나 공통 단계로 정렬한다.
- 검증: 수정된 간격이 인접 요소의 관계를 명확히 하고 두 viewport에서 같은 리듬을 유지하는지 확인한다.
- 상태: CANDIDATE

### web-d-w-d-type-effect-3ddbc88878

- 영역/어댑터: D / web
- 심각도/신뢰도: MEDIUM / HIGH
- 위치: `style.css:6`
- 관찰: `.eyebrow { letter-spacing: .32em; font-size: 10px; color: #d79cff; }`
- 위험: 작은 글자나 과도한 장식이 정보 계층과 가독성을 약화할 수 있다.
- 제안: 텍스트 역할과 사용 언어를 확인하고 승인된 타입 스케일·굵기·행간으로 조정한다.
- 검증: 한글·영문·숫자를 실제 폰트로 렌더해 계층과 판독성을 확인한다.
- 상태: CANDIDATE

### web-d-w-d-type-effect-f6e1fa7a3c

- 영역/어댑터: D / web
- 심각도/신뢰도: MEDIUM / HIGH
- 위치: `style.css:7`
- 관찰: `h1 { margin: 5px 0; font-size: 58px; font-style: italic; background: linear-gradient(90deg, #fff, #d156ff); background-clip: text; color: transparent; }`
- 위험: 작은 글자나 과도한 장식이 정보 계층과 가독성을 약화할 수 있다.
- 제안: 텍스트 역할과 사용 언어를 확인하고 승인된 타입 스케일·굵기·행간으로 조정한다.
- 검증: 한글·영문·숫자를 실제 폰트로 렌더해 계층과 판독성을 확인한다.
- 상태: CANDIDATE

### web-d-w-d-type-effect-ae543c2741

- 영역/어댑터: D / web
- 심각도/신뢰도: MEDIUM / HIGH
- 위치: `style.css:11`
- 관찰: `.cards span { color: #c772ff; font-size: 11px; }`
- 위험: 작은 글자나 과도한 장식이 정보 계층과 가독성을 약화할 수 있다.
- 제안: 텍스트 역할과 사용 언어를 확인하고 승인된 타입 스케일·굵기·행간으로 조정한다.
- 검증: 한글·영문·숫자를 실제 폰트로 렌더해 계층과 판독성을 확인한다.
- 상태: CANDIDATE

### web-d-w-d-type-effect-f3e06ab6bc

- 영역/어댑터: D / web
- 심각도/신뢰도: MEDIUM / HIGH
- 위치: `style.css:13`
- 관찰: `.cards p { font-size: 11px; color: #9b92a9; }`
- 위험: 작은 글자나 과도한 장식이 정보 계층과 가독성을 약화할 수 있다.
- 제안: 텍스트 역할과 사용 언어를 확인하고 승인된 타입 스케일·굵기·행간으로 조정한다.
- 검증: 한글·영문·숫자를 실제 폰트로 렌더해 계층과 판독성을 확인한다.
- 상태: CANDIDATE

### web-e-w-e-color-literal-297725e58b

- 영역/어댑터: E / web
- 심각도/신뢰도: LOW / LOW
- 위치: `style.css:2`
- 관찰: `body { margin: 0; background: #070611; color: #bbb2c9; font-family: Arial, sans-serif; }`
- 위험: 직접 색상 값이 상태 체계와 대비 규칙에서 벗어날 수 있다.
- 제안: 실제 전경·배경과 상태 역할을 확인하고 필요한 경우에만 승인된 토큰으로 연결한다.
- 검증: 실제 조합의 대비와 normal·hover·focus·disabled 상태 구분을 확인한다.
- 상태: CANDIDATE

### web-e-w-e-color-literal-e6484e8f02

- 영역/어댑터: E / web
- 심각도/신뢰도: LOW / LOW
- 위치: `style.css:6`
- 관찰: `.eyebrow { letter-spacing: .32em; font-size: 10px; color: #d79cff; }`
- 위험: 직접 색상 값이 상태 체계와 대비 규칙에서 벗어날 수 있다.
- 제안: 실제 전경·배경과 상태 역할을 확인하고 필요한 경우에만 승인된 토큰으로 연결한다.
- 검증: 실제 조합의 대비와 normal·hover·focus·disabled 상태 구분을 확인한다.
- 상태: CANDIDATE

### web-e-w-e-color-literal-d63228d35e

- 영역/어댑터: E / web
- 심각도/신뢰도: LOW / LOW
- 위치: `style.css:10`
- 관찰: `.cards article { height: 150px; padding: 17px; border: 1px solid #fff2; border-radius: 18px; background: #ffffff0c; box-shadow: 0 12px 36px #0007; }`
- 위험: 직접 색상 값이 상태 체계와 대비 규칙에서 벗어날 수 있다.
- 제안: 실제 전경·배경과 상태 역할을 확인하고 필요한 경우에만 승인된 토큰으로 연결한다.
- 검증: 실제 조합의 대비와 normal·hover·focus·disabled 상태 구분을 확인한다.
- 상태: CANDIDATE

### web-e-w-e-color-literal-cd272c0def

- 영역/어댑터: E / web
- 심각도/신뢰도: LOW / LOW
- 위치: `style.css:11`
- 관찰: `.cards span { color: #c772ff; font-size: 11px; }`
- 위험: 직접 색상 값이 상태 체계와 대비 규칙에서 벗어날 수 있다.
- 제안: 실제 전경·배경과 상태 역할을 확인하고 필요한 경우에만 승인된 토큰으로 연결한다.
- 검증: 실제 조합의 대비와 normal·hover·focus·disabled 상태 구분을 확인한다.
- 상태: CANDIDATE

### web-e-w-e-color-literal-87307472a9

- 영역/어댑터: E / web
- 심각도/신뢰도: LOW / LOW
- 위치: `style.css:13`
- 관찰: `.cards p { font-size: 11px; color: #9b92a9; }`
- 위험: 직접 색상 값이 상태 체계와 대비 규칙에서 벗어날 수 있다.
- 제안: 실제 전경·배경과 상태 역할을 확인하고 필요한 경우에만 승인된 토큰으로 연결한다.
- 검증: 실제 조합의 대비와 normal·hover·focus·disabled 상태 구분을 확인한다.
- 상태: CANDIDATE

### web-e-w-e-color-literal-5e79ad3ae3

- 영역/어댑터: E / web
- 심각도/신뢰도: LOW / LOW
- 위치: `style.css:14`
- 관찰: `button { padding: 13px 29px; border: 0; border-radius: 999px; color: #fff; background: linear-gradient(90deg, #7b2dff, #dd39ff); box-shadow: 0 10px 28px #a22eff66; font-weight: 700; }`
- 위험: 직접 색상 값이 상태 체계와 대비 규칙에서 벗어날 수 있다.
- 제안: 실제 전경·배경과 상태 역할을 확인하고 필요한 경우에만 승인된 토큰으로 연결한다.
- 검증: 실제 조합의 대비와 normal·hover·focus·disabled 상태 구분을 확인한다.
- 상태: CANDIDATE
