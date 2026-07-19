# UI 아트 정적 감사 후보

> 이 보고서는 정적 패턴 후보이며 결함 확정이나 자동 수정 지시가 아닙니다.

- 검사 루트: `before`
- 어댑터: godot
- 검사 파일: 2
- 후보: 41
- 사유 있는 제외: 0

## Findings

### godot-b-g-b-manual-layout-73720e860a

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:24`
- 관찰: `offset_left = 130.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-04f188c62d

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:25`
- 관찰: `offset_top = 82.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-b93af30478

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:26`
- 관찰: `offset_right = 1150.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-99e4c1b789

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:27`
- 관찰: `offset_bottom = 638.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-728de45afb

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:35`
- 관찰: `offset_left = 180.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-6fda139284

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:36`
- 관찰: `offset_top = 128.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-3a852ce5e1

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:37`
- 관찰: `offset_right = 690.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-16b2249225

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:38`
- 관찰: `offset_bottom = 208.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-2517dfda7e

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:44`
- 관찰: `offset_left = 184.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-e3cd5b7f69

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:45`
- 관찰: `offset_top = 220.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-982183b1fb

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:46`
- 관찰: `offset_right = 760.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-7a164b5f37

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:47`
- 관찰: `offset_bottom = 250.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-499a200318

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:53`
- 관찰: `offset_left = 180.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-9411532492

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:54`
- 관찰: `offset_top = 300.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-369a596ab6

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:55`
- 관찰: `offset_right = 1100.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-760b466fc1

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:56`
- 관찰: `offset_bottom = 490.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-d29239f5ef

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:64`
- 관찰: `offset_left = 20.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-dcbb5bf44f

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:65`
- 관찰: `offset_top = 28.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-bc0cd26603

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:66`
- 관찰: `offset_right = 230.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-3bc08a6ad7

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:67`
- 관찰: `offset_bottom = 88.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-4383dc054a

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:75`
- 관찰: `offset_left = 20.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-0a759c45b6

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:76`
- 관찰: `offset_top = 28.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-f8f2943c14

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:77`
- 관찰: `offset_right = 230.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-525bbb9c06

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:78`
- 관찰: `offset_bottom = 88.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-2cf7951b80

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:86`
- 관찰: `offset_left = 20.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-7406090735

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:87`
- 관찰: `offset_top = 28.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-9b7185ff91

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:88`
- 관찰: `offset_right = 230.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-707c762c43

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:89`
- 관찰: `offset_bottom = 88.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-872f9d5ad6

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:94`
- 관찰: `offset_left = 870.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-ef2a20c277

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:95`
- 관찰: `offset_top = 544.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-7cd783b44c

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:96`
- 관찰: `offset_right = 1098.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-1f9cec9492

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:97`
- 관찰: `offset_bottom = 594.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-c-g-c-irregular-spacing-23442abc45

- 영역/어댑터: C / godot
- 심각도/신뢰도: MEDIUM / MEDIUM
- 위치: `main.tscn:57`
- 관찰: `theme_override_constants/separation = 17`
- 위험: 간격 override가 공통 Theme 리듬과 다른 임시 조정일 수 있다.
- 제안: 주변 관계와 Theme 상수를 대조해 의도 없는 예외만 승인 후 공통 간격으로 정렬한다.
- 검증: 긴 텍스트와 대표 해상도에서 그룹 관계와 밀도가 일관적인지 확인한다.
- 상태: CANDIDATE

### godot-d-g-d-type-effect-43cb2cbe98

- 영역/어댑터: D / godot
- 심각도/신뢰도: MEDIUM / HIGH
- 위치: `main.tscn:40`
- 관찰: `theme_override_font_sizes/font_size = 54`
- 위험: 작은 텍스트가 실제 폰트와 스케일에서 읽히지 않을 수 있다.
- 제안: 텍스트 역할과 프로젝트 타입 스케일을 확인하고 승인된 최소 크기와 계층으로 조정한다.
- 검증: Godot 실행 화면에서 한글·영문·숫자의 판독성과 계층을 확인한다.
- 상태: CANDIDATE

### godot-d-g-d-type-effect-d5046d0eb5

- 영역/어댑터: D / godot
- 심각도/신뢰도: MEDIUM / HIGH
- 위치: `main.tscn:49`
- 관찰: `theme_override_font_sizes/font_size = 13`
- 위험: 작은 텍스트가 실제 폰트와 스케일에서 읽히지 않을 수 있다.
- 제안: 텍스트 역할과 프로젝트 타입 스케일을 확인하고 승인된 최소 크기와 계층으로 조정한다.
- 검증: Godot 실행 화면에서 한글·영문·숫자의 판독성과 계층을 확인한다.
- 상태: CANDIDATE

### godot-d-g-d-type-effect-95ffa94b5e

- 영역/어댑터: D / godot
- 심각도/신뢰도: MEDIUM / HIGH
- 위치: `main.tscn:68`
- 관찰: `theme_override_font_sizes/font_size = 22`
- 위험: 작은 텍스트가 실제 폰트와 스케일에서 읽히지 않을 수 있다.
- 제안: 텍스트 역할과 프로젝트 타입 스케일을 확인하고 승인된 최소 크기와 계층으로 조정한다.
- 검증: Godot 실행 화면에서 한글·영문·숫자의 판독성과 계층을 확인한다.
- 상태: CANDIDATE

### godot-d-g-d-type-effect-11ff3ad964

- 영역/어댑터: D / godot
- 심각도/신뢰도: MEDIUM / HIGH
- 위치: `main.tscn:79`
- 관찰: `theme_override_font_sizes/font_size = 22`
- 위험: 작은 텍스트가 실제 폰트와 스케일에서 읽히지 않을 수 있다.
- 제안: 텍스트 역할과 프로젝트 타입 스케일을 확인하고 승인된 최소 크기와 계층으로 조정한다.
- 검증: Godot 실행 화면에서 한글·영문·숫자의 판독성과 계층을 확인한다.
- 상태: CANDIDATE

### godot-d-g-d-type-effect-7f2785d954

- 영역/어댑터: D / godot
- 심각도/신뢰도: MEDIUM / HIGH
- 위치: `main.tscn:90`
- 관찰: `theme_override_font_sizes/font_size = 22`
- 위험: 작은 텍스트가 실제 폰트와 스케일에서 읽히지 않을 수 있다.
- 제안: 텍스트 역할과 프로젝트 타입 스케일을 확인하고 승인된 최소 크기와 계층으로 조정한다.
- 검증: Godot 실행 화면에서 한글·영문·숫자의 판독성과 계층을 확인한다.
- 상태: CANDIDATE

### godot-d-g-d-type-effect-effeb3ddba

- 영역/어댑터: D / godot
- 심각도/신뢰도: MEDIUM / HIGH
- 위치: `main.tscn:98`
- 관찰: `theme_override_font_sizes/font_size = 18`
- 위험: 작은 텍스트가 실제 폰트와 스케일에서 읽히지 않을 수 있다.
- 제안: 텍스트 역할과 프로젝트 타입 스케일을 확인하고 승인된 최소 크기와 계층으로 조정한다.
- 검증: Godot 실행 화면에서 한글·영문·숫자의 판독성과 계층을 확인한다.
- 상태: CANDIDATE

### godot-e-g-e-color-literal-b0340849a4

- 영역/어댑터: E / godot
- 심각도/신뢰도: LOW / LOW
- 위치: `main.tscn:39`
- 관찰: `theme_override_colors/font_color = Color(0.92, 0.65, 1, 1)`
- 위험: 직접 색상 override가 Theme 상속과 상태 대비를 우회할 수 있다.
- 제안: 색상의 역할과 상속 경로를 확인하고 필요한 경우에만 승인된 Theme 색상으로 통합한다.
- 검증: normal·hover·pressed·disabled·focus 상태와 실제 전경·배경 대비를 확인한다.
- 상태: CANDIDATE

### godot-e-g-e-color-literal-4f9e0e23d9

- 영역/어댑터: E / godot
- 심각도/신뢰도: LOW / LOW
- 위치: `main.tscn:48`
- 관찰: `theme_override_colors/font_color = Color(0.62, 0.55, 0.68, 1)`
- 위험: 직접 색상 override가 Theme 상속과 상태 대비를 우회할 수 있다.
- 제안: 색상의 역할과 상속 경로를 확인하고 필요한 경우에만 승인된 Theme 색상으로 통합한다.
- 검증: normal·hover·pressed·disabled·focus 상태와 실제 전경·배경 대비를 확인한다.
- 상태: CANDIDATE
