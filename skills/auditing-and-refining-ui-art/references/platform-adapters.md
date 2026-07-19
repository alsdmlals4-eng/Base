# 플랫폼 어댑터

## Godot

- `Control`: 최소 크기, size flags, mouse filter, focus mode, anchor와 offset 관계를 확인한다.
- `Container`: 자식의 직접 위치 지정이 컨테이너 계산과 충돌하지 않는지 확인한다.
- `Theme`: 상속과 type variation을 우선하고 불필요한 노드별 override를 찾는다.
- `StyleBox`: 배경, 테두리, 모서리, 그림자, content margin이 상태와 계층을 표현하는지 확인한다.
- 폰트·색상·상태: normal, hover, pressed, disabled, focus와 입력 장치별 피드백을 렌더한다.
- 프로젝트의 Godot 버전과 stretch 설정을 먼저 읽고 다른 버전 동작을 추정하지 않는다.

## Web

- HTML 의미 구조와 CSS flow, flex, grid를 우선 확인한다.
- 고정 폭·절대 위치는 반응형 레이아웃과 콘텐츠 변화에서 실제로 실패하는지 확인한다.
- CSS 변수와 디자인 토큰의 일관성을 보되 단순한 literal 존재만으로 결함 처리하지 않는다.
- hover뿐 아니라 focus-visible, active, disabled, loading, error 상태를 확인한다.
- React·Vue·Svelte 같은 프레임워크에서는 컴포넌트 경계와 상태 소유권을 함께 본다.
- 최소 두 개의 대표 viewport와 실제 브라우저 렌더를 확인한다.

## 공통 검증

- 정적 검사는 후보 수집 단계다.
- 화면 캡처만으로 접근성 트리, 키보드 이동, 동적 상태를 통과 처리하지 않는다.
- 참조 UI의 수치와 스타일을 그대로 옮기지 않고 프로젝트의 정보 구조와 차별화 방향에 맞게 변환한다.
