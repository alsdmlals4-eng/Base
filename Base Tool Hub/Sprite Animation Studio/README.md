# Sprite Animation Studio

**실행 정본:** `tools/sprite-animation-studio`

캐릭터/이펙트 프레임을 프로젝트별로 가져오고 검수해 GIF, atlas, Godot handoff로 내보내는 도구입니다.

- `sprite_action`: 행동 프레임
- `pose_sequence`: 포즈 시퀀스
- `effect_stages`: 단계별 이펙트
- project-scoped export와 Figma 전달 패킷

실제 비투명 샘플 프레임을 이용한 action/effect import/export와 프로젝트 격리는 Linux smoke에서 검증됐습니다. production `sprite-gen` 생성은 안전한 mutable workspace isolation이 아직 없어 차단되어 있고, Windows child Studio 실행도 `BLOCKED_PLATFORM`입니다.
