# UI 아트 정적 감사 후보

> 이 보고서는 정적 패턴 후보이며 결함 확정이나 자동 수정 지시가 아닙니다.

- 검사 루트: `after`
- 어댑터: godot
- 검사 파일: 2
- 후보: 29
- 사유 있는 제외: 0

## Findings

### godot-b-g-b-manual-layout-728de45afb

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:35`
- 관찰: `offset_left = 72.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-6fda139284

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:36`
- 관찰: `offset_top = 60.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-3a852ce5e1

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:37`
- 관찰: `offset_right = -72.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-b-g-b-manual-layout-16b2249225

- 영역/어댑터: B / godot
- 심각도/신뢰도: MEDIUM / LOW
- 위치: `main.tscn:38`
- 관찰: `offset_bottom = -52.0`
- 위험: 수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.
- 제안: 노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.
- 검증: 프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다.
- 상태: CANDIDATE

### godot-d-g-d-type-effect-466d941135

- 영역/어댑터: D / godot
- 심각도/신뢰도: MEDIUM / HIGH
- 위치: `main.tscn:57`
- 관찰: `theme_override_font_sizes/font_size = 18`
- 위험: 작은 텍스트가 실제 폰트와 스케일에서 읽히지 않을 수 있다.
- 제안: 텍스트 역할과 프로젝트 타입 스케일을 확인하고 승인된 최소 크기와 계층으로 조정한다.
- 검증: Godot 실행 화면에서 한글·영문·숫자의 판독성과 계층을 확인한다.
- 상태: CANDIDATE

### godot-d-g-d-type-effect-148467a1c2

- 영역/어댑터: D / godot
- 심각도/신뢰도: MEDIUM / HIGH
- 위치: `main.tscn:61`
- 관찰: `theme_override_font_sizes/font_size = 58`
- 위험: 작은 텍스트가 실제 폰트와 스케일에서 읽히지 않을 수 있다.
- 제안: 텍스트 역할과 프로젝트 타입 스케일을 확인하고 승인된 최소 크기와 계층으로 조정한다.
- 검증: Godot 실행 화면에서 한글·영문·숫자의 판독성과 계층을 확인한다.
- 상태: CANDIDATE

### godot-d-g-d-type-effect-4eb4d1e26b

- 영역/어댑터: D / godot
- 심각도/신뢰도: MEDIUM / HIGH
- 위치: `main.tscn:66`
- 관찰: `theme_override_font_sizes/font_size = 18`
- 위험: 작은 텍스트가 실제 폰트와 스케일에서 읽히지 않을 수 있다.
- 제안: 텍스트 역할과 프로젝트 타입 스케일을 확인하고 승인된 최소 크기와 계층으로 조정한다.
- 검증: Godot 실행 화면에서 한글·영문·숫자의 판독성과 계층을 확인한다.
- 상태: CANDIDATE

### godot-d-g-d-type-effect-2f4b96ed35

- 영역/어댑터: D / godot
- 심각도/신뢰도: MEDIUM / HIGH
- 위치: `main.tscn:76`
- 관찰: `theme_override_font_sizes/font_size = 22`
- 위험: 작은 텍스트가 실제 폰트와 스케일에서 읽히지 않을 수 있다.
- 제안: 텍스트 역할과 프로젝트 타입 스케일을 확인하고 승인된 최소 크기와 계층으로 조정한다.
- 검증: Godot 실행 화면에서 한글·영문·숫자의 판독성과 계층을 확인한다.
- 상태: CANDIDATE

### godot-d-g-d-type-effect-effeb3ddba

- 영역/어댑터: D / godot
- 심각도/신뢰도: MEDIUM / HIGH
- 위치: `main.tscn:98`
- 관찰: `theme_override_font_sizes/font_size = 28`
- 위험: 작은 텍스트가 실제 폰트와 스케일에서 읽히지 않을 수 있다.
- 제안: 텍스트 역할과 프로젝트 타입 스케일을 확인하고 승인된 최소 크기와 계층으로 조정한다.
- 검증: Godot 실행 화면에서 한글·영문·숫자의 판독성과 계층을 확인한다.
- 상태: CANDIDATE

### godot-d-g-d-type-effect-b2e08570d6

- 영역/어댑터: D / godot
- 심각도/신뢰도: MEDIUM / HIGH
- 위치: `main.tscn:102`
- 관찰: `theme_override_font_sizes/font_size = 23`
- 위험: 작은 텍스트가 실제 폰트와 스케일에서 읽히지 않을 수 있다.
- 제안: 텍스트 역할과 프로젝트 타입 스케일을 확인하고 승인된 최소 크기와 계층으로 조정한다.
- 검증: Godot 실행 화면에서 한글·영문·숫자의 판독성과 계층을 확인한다.
- 상태: CANDIDATE

### godot-d-g-d-type-effect-dd4a646bf7

- 영역/어댑터: D / godot
- 심각도/신뢰도: MEDIUM / HIGH
- 위치: `main.tscn:116`
- 관찰: `theme_override_font_sizes/font_size = 28`
- 위험: 작은 텍스트가 실제 폰트와 스케일에서 읽히지 않을 수 있다.
- 제안: 텍스트 역할과 프로젝트 타입 스케일을 확인하고 승인된 최소 크기와 계층으로 조정한다.
- 검증: Godot 실행 화면에서 한글·영문·숫자의 판독성과 계층을 확인한다.
- 상태: CANDIDATE

### godot-d-g-d-type-effect-01839cfa97

- 영역/어댑터: D / godot
- 심각도/신뢰도: MEDIUM / HIGH
- 위치: `main.tscn:120`
- 관찰: `theme_override_font_sizes/font_size = 23`
- 위험: 작은 텍스트가 실제 폰트와 스케일에서 읽히지 않을 수 있다.
- 제안: 텍스트 역할과 프로젝트 타입 스케일을 확인하고 승인된 최소 크기와 계층으로 조정한다.
- 검증: Godot 실행 화면에서 한글·영문·숫자의 판독성과 계층을 확인한다.
- 상태: CANDIDATE

### godot-d-g-d-type-effect-14c220ef76

- 영역/어댑터: D / godot
- 심각도/신뢰도: MEDIUM / HIGH
- 위치: `main.tscn:134`
- 관찰: `theme_override_font_sizes/font_size = 28`
- 위험: 작은 텍스트가 실제 폰트와 스케일에서 읽히지 않을 수 있다.
- 제안: 텍스트 역할과 프로젝트 타입 스케일을 확인하고 승인된 최소 크기와 계층으로 조정한다.
- 검증: Godot 실행 화면에서 한글·영문·숫자의 판독성과 계층을 확인한다.
- 상태: CANDIDATE

### godot-d-g-d-type-effect-8757078b14

- 영역/어댑터: D / godot
- 심각도/신뢰도: MEDIUM / HIGH
- 위치: `main.tscn:138`
- 관찰: `theme_override_font_sizes/font_size = 23`
- 위험: 작은 텍스트가 실제 폰트와 스케일에서 읽히지 않을 수 있다.
- 제안: 텍스트 역할과 프로젝트 타입 스케일을 확인하고 승인된 최소 크기와 계층으로 조정한다.
- 검증: Godot 실행 화면에서 한글·영문·숫자의 판독성과 계층을 확인한다.
- 상태: CANDIDATE

### godot-d-g-d-type-effect-3dbbe51229

- 영역/어댑터: D / godot
- 심각도/신뢰도: MEDIUM / HIGH
- 위치: `main.tscn:151`
- 관찰: `theme_override_font_sizes/font_size = 17`
- 위험: 작은 텍스트가 실제 폰트와 스케일에서 읽히지 않을 수 있다.
- 제안: 텍스트 역할과 프로젝트 타입 스케일을 확인하고 승인된 최소 크기와 계층으로 조정한다.
- 검증: Godot 실행 화면에서 한글·영문·숫자의 판독성과 계층을 확인한다.
- 상태: CANDIDATE

### godot-d-g-d-type-effect-f5c14d65de

- 영역/어댑터: D / godot
- 심각도/신뢰도: MEDIUM / HIGH
- 위치: `main.tscn:157`
- 관찰: `theme_override_font_sizes/font_size = 18`
- 위험: 작은 텍스트가 실제 폰트와 스케일에서 읽히지 않을 수 있다.
- 제안: 텍스트 역할과 프로젝트 타입 스케일을 확인하고 승인된 최소 크기와 계층으로 조정한다.
- 검증: Godot 실행 화면에서 한글·영문·숫자의 판독성과 계층을 확인한다.
- 상태: CANDIDATE

### godot-e-g-e-color-literal-b20cf65538

- 영역/어댑터: E / godot
- 심각도/신뢰도: LOW / LOW
- 위치: `main.tscn:6`
- 관찰: `bg_color = Color(0.945, 0.722, 0.294, 1)`
- 위험: 직접 색상 override가 Theme 상속과 상태 대비를 우회할 수 있다.
- 제안: 색상의 역할과 상속 경로를 확인하고 필요한 경우에만 승인된 Theme 색상으로 통합한다.
- 검증: normal·hover·pressed·disabled·focus 상태와 실제 전경·배경 대비를 확인한다.
- 상태: CANDIDATE

### godot-e-g-e-color-literal-cd259279ae

- 영역/어댑터: E / godot
- 심각도/신뢰도: LOW / LOW
- 위치: `main.tscn:56`
- 관찰: `theme_override_colors/font_color = Color(0.945, 0.722, 0.294, 1)`
- 위험: 직접 색상 override가 Theme 상속과 상태 대비를 우회할 수 있다.
- 제안: 색상의 역할과 상속 경로를 확인하고 필요한 경우에만 승인된 Theme 색상으로 통합한다.
- 검증: normal·hover·pressed·disabled·focus 상태와 실제 전경·배경 대비를 확인한다.
- 상태: CANDIDATE

### godot-e-g-e-color-literal-97c2d66fd9

- 영역/어댑터: E / godot
- 심각도/신뢰도: LOW / LOW
- 위치: `main.tscn:65`
- 관찰: `theme_override_colors/font_color = Color(0.68, 0.75, 0.78, 1)`
- 위험: 직접 색상 override가 Theme 상속과 상태 대비를 우회할 수 있다.
- 제안: 색상의 역할과 상속 경로를 확인하고 필요한 경우에만 승인된 Theme 색상으로 통합한다.
- 검증: normal·hover·pressed·disabled·focus 상태와 실제 전경·배경 대비를 확인한다.
- 상태: CANDIDATE

### godot-e-g-e-color-literal-76f572fec9

- 영역/어댑터: E / godot
- 심각도/신뢰도: LOW / LOW
- 위치: `main.tscn:75`
- 관찰: `theme_override_colors/font_color = Color(0.945, 0.722, 0.294, 1)`
- 위험: 직접 색상 override가 Theme 상속과 상태 대비를 우회할 수 있다.
- 제안: 색상의 역할과 상속 경로를 확인하고 필요한 경우에만 승인된 Theme 색상으로 통합한다.
- 검증: normal·hover·pressed·disabled·focus 상태와 실제 전경·배경 대비를 확인한다.
- 상태: CANDIDATE

### godot-e-g-e-color-literal-2108bc286d

- 영역/어댑터: E / godot
- 심각도/신뢰도: LOW / LOW
- 위치: `main.tscn:80`
- 관찰: `theme_override_colors/font_color = Color(0.68, 0.75, 0.78, 1)`
- 위험: 직접 색상 override가 Theme 상속과 상태 대비를 우회할 수 있다.
- 제안: 색상의 역할과 상속 경로를 확인하고 필요한 경우에만 승인된 Theme 색상으로 통합한다.
- 검증: normal·hover·pressed·disabled·focus 상태와 실제 전경·배경 대비를 확인한다.
- 상태: CANDIDATE

### godot-e-g-e-color-literal-e62de55ce9

- 영역/어댑터: E / godot
- 심각도/신뢰도: LOW / LOW
- 위치: `main.tscn:97`
- 관찰: `theme_override_colors/font_color = Color(0.945, 0.722, 0.294, 1)`
- 위험: 직접 색상 override가 Theme 상속과 상태 대비를 우회할 수 있다.
- 제안: 색상의 역할과 상속 경로를 확인하고 필요한 경우에만 승인된 Theme 색상으로 통합한다.
- 검증: normal·hover·pressed·disabled·focus 상태와 실제 전경·배경 대비를 확인한다.
- 상태: CANDIDATE

### godot-e-g-e-color-literal-5666c3e557

- 영역/어댑터: E / godot
- 심각도/신뢰도: LOW / LOW
- 위치: `main.tscn:106`
- 관찰: `theme_override_colors/font_color = Color(0.68, 0.75, 0.78, 1)`
- 위험: 직접 색상 override가 Theme 상속과 상태 대비를 우회할 수 있다.
- 제안: 색상의 역할과 상속 경로를 확인하고 필요한 경우에만 승인된 Theme 색상으로 통합한다.
- 검증: normal·hover·pressed·disabled·focus 상태와 실제 전경·배경 대비를 확인한다.
- 상태: CANDIDATE

### godot-e-g-e-color-literal-708a8adb4f

- 영역/어댑터: E / godot
- 심각도/신뢰도: LOW / LOW
- 위치: `main.tscn:115`
- 관찰: `theme_override_colors/font_color = Color(0.945, 0.722, 0.294, 1)`
- 위험: 직접 색상 override가 Theme 상속과 상태 대비를 우회할 수 있다.
- 제안: 색상의 역할과 상속 경로를 확인하고 필요한 경우에만 승인된 Theme 색상으로 통합한다.
- 검증: normal·hover·pressed·disabled·focus 상태와 실제 전경·배경 대비를 확인한다.
- 상태: CANDIDATE

### godot-e-g-e-color-literal-e09aaadf52

- 영역/어댑터: E / godot
- 심각도/신뢰도: LOW / LOW
- 위치: `main.tscn:124`
- 관찰: `theme_override_colors/font_color = Color(0.68, 0.75, 0.78, 1)`
- 위험: 직접 색상 override가 Theme 상속과 상태 대비를 우회할 수 있다.
- 제안: 색상의 역할과 상속 경로를 확인하고 필요한 경우에만 승인된 Theme 색상으로 통합한다.
- 검증: normal·hover·pressed·disabled·focus 상태와 실제 전경·배경 대비를 확인한다.
- 상태: CANDIDATE

### godot-e-g-e-color-literal-eb2a6f928c

- 영역/어댑터: E / godot
- 심각도/신뢰도: LOW / LOW
- 위치: `main.tscn:133`
- 관찰: `theme_override_colors/font_color = Color(0.945, 0.722, 0.294, 1)`
- 위험: 직접 색상 override가 Theme 상속과 상태 대비를 우회할 수 있다.
- 제안: 색상의 역할과 상속 경로를 확인하고 필요한 경우에만 승인된 Theme 색상으로 통합한다.
- 검증: normal·hover·pressed·disabled·focus 상태와 실제 전경·배경 대비를 확인한다.
- 상태: CANDIDATE

### godot-e-g-e-color-literal-8f9acbeca7

- 영역/어댑터: E / godot
- 심각도/신뢰도: LOW / LOW
- 위치: `main.tscn:142`
- 관찰: `theme_override_colors/font_color = Color(0.68, 0.75, 0.78, 1)`
- 위험: 직접 색상 override가 Theme 상속과 상태 대비를 우회할 수 있다.
- 제안: 색상의 역할과 상속 경로를 확인하고 필요한 경우에만 승인된 Theme 색상으로 통합한다.
- 검증: normal·hover·pressed·disabled·focus 상태와 실제 전경·배경 대비를 확인한다.
- 상태: CANDIDATE

### godot-e-g-e-color-literal-f8b7091c8e

- 영역/어댑터: E / godot
- 심각도/신뢰도: LOW / LOW
- 위치: `main.tscn:150`
- 관찰: `theme_override_colors/font_color = Color(0.68, 0.75, 0.78, 1)`
- 위험: 직접 색상 override가 Theme 상속과 상태 대비를 우회할 수 있다.
- 제안: 색상의 역할과 상속 경로를 확인하고 필요한 경우에만 승인된 Theme 색상으로 통합한다.
- 검증: normal·hover·pressed·disabled·focus 상태와 실제 전경·배경 대비를 확인한다.
- 상태: CANDIDATE

### godot-e-g-e-color-literal-571f099882

- 영역/어댑터: E / godot
- 심각도/신뢰도: LOW / LOW
- 위치: `main.tscn:156`
- 관찰: `theme_override_colors/font_color = Color(0.12, 0.08, 0, 1)`
- 위험: 직접 색상 override가 Theme 상속과 상태 대비를 우회할 수 있다.
- 제안: 색상의 역할과 상속 경로를 확인하고 필요한 경우에만 승인된 Theme 색상으로 통합한다.
- 검증: normal·hover·pressed·disabled·focus 상태와 실제 전경·배경 대비를 확인한다.
- 상태: CANDIDATE
