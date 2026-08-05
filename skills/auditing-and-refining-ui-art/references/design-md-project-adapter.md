# Project DESIGN.md Adapter

## 목적

프로젝트의 색·타이포그래피·간격·형태·깊이·컴포넌트 표현을 AI와 도구가 읽을 수 있는 시각 토큰 정본으로 관리한다. `GAME_UX_UI_SYSTEM`은 플레이어 경험·화면 흐름·정보 계층·상태·입력·접근성·Godot 소유권의 상위 행동 정본으로 유지한다.

## 적용 조건

- 여러 화면·구현자·도구에서 반복되는 시각 토큰이 있다.
- Godot Theme 또는 Web CSS/token으로 변환할 명시적 값이 필요하다.
- 외부 브랜드·getdesign 계열 참고를 프로젝트 고유 원칙으로 변환해 출처와 차이를 기록해야 한다.

작은 단일 화면이나 시각 방향이 아직 미확정이면 새 `DESIGN.md`를 만들지 않는다.

## 권한 경계

`DESIGN.md`가 소유:
- 색, typography, spacing, radius, border, elevation
- 컴포넌트의 시각적 variant와 Do/Don't
- Godot `Theme`·`StyleBox`·Font·Color·Constant mapping
- Web CSS variable·DTCG·Tailwind mapping

`GAME_UX_UI_SYSTEM`이 소유:
- 플레이어 경험, 화면 질문, journey, information hierarchy
- 상태 의미·도메인 소유권·입력 결과
- 접근성 행동·복구·오류·피드백 계약

게임 규칙·보상·저장·진행은 어느 시각 토큰 파일도 소유하지 않는다.

## 형식·버전 고정

```yaml
format: google-design-md | project-design-md
format_version: alpha | <approved-version>
source_commit_or_release:
last_verified_at:
canonical_scope: visual-language-only
```

외부 형식이 alpha이면 자동 갱신하지 않고 exact source identity를 고정한다. 형식 변경은 diff·migration·rollback을 거친다.

## 플랫폼 mapping

### Godot
- token을 `Theme`, `StyleBox`, Font, Color, Constant와 재사용 Scene에 매핑한다.
- CSS·React 컴포넌트를 Godot 구현으로 간주하지 않는다.
- Theme 적용 뒤 실제 최소/목표 해상도와 입력 장치에서 렌더한다.

### Web
- token을 CSS custom property·DTCG·Tailwind config 중 승인된 형식에 매핑한다.
- 외부 UI 코드는 `external-ui-procurement-and-anti-generic-quality.md` Gate를 별도로 통과한다.

## 검증

- 토큰 ID 중복·순환 참조·누락 mapping
- 긴 한국어·최소 해상도·색 대비·포커스·Reduced Motion
- 같은 상태가 Godot Theme와 Web CSS에서 다른 의미가 되지 않는지
- 실제 렌더 전후와 프로젝트 고유 방향

자동 lint는 사람 이해·브랜드 적합성·접근성 준수를 자동 증명하지 않는다.
