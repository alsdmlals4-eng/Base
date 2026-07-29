from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, content: str) -> None:
    (ROOT / path).write_text(content, encoding="utf-8")


def insert_before(text: str, marker: str, addition: str) -> str:
    if addition.strip() in text:
        return text
    if marker not in text:
        raise RuntimeError(f"marker not found: {marker}")
    return text.replace(marker, addition + "\n\n" + marker, 1)


def insert_after(text: str, marker: str, addition: str) -> str:
    if addition.strip() in text:
        return text
    if marker not in text:
        raise RuntimeError(f"marker not found: {marker}")
    return text.replace(marker, marker + "\n\n" + addition, 1)


def update_registry() -> None:
    path = "skills/SKILL_REGISTRY.json"
    data = json.loads(read(path))
    skill = next(
        item
        for item in data["skills"]
        if item["skill_id"] == "analyzing-and-refining-game-concepts"
    )

    for trigger in (
        "game-system-design",
        "system-boundary",
        "difficulty-design",
        "combat-ai-design",
        "adaptive-difficulty",
        "dynamic-difficulty-adjustment",
        "attack-budget",
        "threat-budget",
        "tension-pacing",
        "enemy-ai-fairness",
    ):
        if trigger not in skill["trigger_tags"]:
            skill["trigger_tags"].append(trigger)

    skill["use_when"] = [
        "핵심 컨셉·뾰족한 재미·제약·DDD, 게임 시스템 경계, 난이도·전투 AI, 비교 게임·플레이어 반응·행동 근거·플레이테스트를 개선안과 PoC·재조정 방향으로 변환한다."
    ]

    for trigger in (
        "system boundary missing",
        "difficulty reduced to health scaling",
        "unfair hidden information",
        "player input cheating",
        "attack budget missing",
        "threat budget missing",
        "tension pacing missing",
        "success punished by scaling",
        "adaptive difficulty oscillation",
        "hysteresis missing",
        "difficulty change timing hidden",
        "accessibility confused with difficulty",
    ):
        if trigger not in skill["review_triggers"]:
            skill["review_triggers"].append(trigger)

    skill["last_reviewed_at"] = "2026-07-29"
    skill["last_reviewed_commit"] = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    skill["knowledge_state"] = "HYPOTHESIS"

    write(path, json.dumps(data, ensure_ascii=False, separators=(",", ":")))


def update_start_here() -> None:
    path = "START_HERE.md"
    text = read(path)
    old = """frame
→ constrain
→ sharpen
→ structure
→ 필요한 경우 benchmark-and-player-research
→ analyze
→ 필요한 경우 playtest-and-experiment"""
    new = """frame
→ constrain
→ sharpen
→ structure
→ 필요한 경우 system-design
→ 필요한 경우 difficulty-and-combat-ai
→ 필요한 경우 benchmark-and-player-research
→ analyze
→ 필요한 경우 playtest-and-experiment"""
    if old in text:
        text = text.replace(old, new, 1)
    elif "→ 필요한 경우 system-design" not in text:
        raise RuntimeError("START_HERE mode sequence not found")

    addition = """### 게임 시스템·난이도·전투 AI 설계

`analyzing-and-refining-game-concepts`의 `system-design` 또는 `difficulty-and-combat-ai` Skill Mode를 사용한다.

```text
플레이어 경험 목표
→ 시스템 경계·행동/선택/결과
→ 난이도 장벽·공정성 안전 규칙
→ 개별 적 판단·전투 조율자·난이도/페이싱 디렉터
→ 공격·위협 예산·긴장도 상태
→ 고정·적응형 난이도
→ 텔레메트리·플레이테스트·PoC
```

상세 절차는 `skills/analyzing-and-refining-game-concepts/references/game-system-difficulty-and-combat-ai.md`, 프로젝트 작성 틀은 `templates/planning/GAME_SYSTEM_DIFFICULTY_AND_COMBAT_AI_CONTRACT.md`를 사용한다. 새 독립 난이도·전투 AI Skill을 만들지 않는다."""
    text = insert_before(text, "### 프로젝트 코어 판정", addition)
    write(path, text)


def update_documentation_map() -> None:
    path = "docs/DOCUMENTATION_MAP.md"
    text = read(path)
    old = "| 핵심 컨셉·뾰족한 재미·DDD·기획 정렬 | `analyzing-and-refining-game-concepts` | `frame` / `constrain` / `sharpen` / `structure` / `analyze` |"
    new = "| 핵심 컨셉·뾰족한 재미·DDD·게임 시스템·난이도·전투 AI·기획 정렬 | `analyzing-and-refining-game-concepts` | `frame` / `constrain` / `sharpen` / `structure` / `system-design` / `difficulty-and-combat-ai` / `analyze` |"
    if old in text:
        text = text.replace(old, new, 1)
    elif "`difficulty-and-combat-ai` / `analyze`" not in text:
        raise RuntimeError("Documentation Map skill row not found")

    row = "| 게임 시스템 경계·난이도·적 전투 AI·공격 예산·긴장도·DDA를 어떻게 설계하는가? | `skills/analyzing-and-refining-game-concepts/references/game-system-difficulty-and-combat-ai.md` | `templates/planning/GAME_SYSTEM_DIFFICULTY_AND_COMBAT_AI_CONTRACT.md` |"
    marker = "| 어떤 게임·유저 반응을 어떻게 조사하고 반영하는가?"
    if row not in text:
        if marker not in text:
            raise RuntimeError("Documentation Map reference table marker not found")
        text = text.replace(marker, row + "\n" + marker, 1)

    write(path, text)


def update_guide() -> None:
    path = "docs/knowledge/game-development/GAME_DESIGN_AND_PLAYER_EXPERIENCE_GUIDE.md"
    text = read(path)
    addition = """## 8.1 게임 시스템 설계

게임 시스템 설계는 기능 목록이나 Godot Node 목록이 아니다.

```text
플레이어 경험 목표
→ 플레이어가 읽을 정보
→ 고민할 선택과 위험
→ 입력·행동·자원·상태·규칙
→ 시스템 반응·결과·피드백
→ 실패 후 학습·복구
→ 다음 행동과 검증 Evidence
```

각 시스템은 책임·입력·출력·비책임·정본·실패·검증을 가진다. 인접 시스템과 같은 상태를 중복 소유하지 않으며, 새로운 기능을 추가하기 전에 `REMOVE → REDUCE → MERGE → CLARIFY → FEEDBACK 강화 → ADD` 순서로 검토한다.

상세 실행은 `analyzing-and-refining-game-concepts: system-design`과 `templates/planning/GAME_SYSTEM_DIFFICULTY_AND_COMBAT_AI_CONTRACT.md`가 책임진다.

## 8.2 난이도 장벽 프로필

난이도는 적 체력 하나가 아니라 규칙 이해, 정보 탐색, 의사결정, 기억·주의, 반응·정밀 입력, 시간 압박, 자원·손실, 반복·복구 거리, 감각·입력 장벽, 적 조합·공간·카메라 압박의 조합이다.

대상 플레이어별로 `의도한 도전 / 요구 능력·지식 / 예고·정보 / 복구·대안 / 측정 / 접근성 위험`을 기록한다. 난이도와 접근성 보조를 같은 축으로 합치지 않는다.

## 8.3 공정성 안전 규칙

높은 난이도에서도 다음을 유지한다.

- 보이지 않는 정보나 플레이어 입력 직접 읽기로 즉시 처벌하지 않는다.
- 강한 공격은 시각·음향·동작 중 하나 이상으로 예고한다.
- 카메라 밖 즉사, 연속 기절, 기상 직후 재경직, 회피 불가능 조합을 제한한다.
- 실패 원인과 다음에 바꿀 행동을 설명할 수 있어야 한다.
- 정보 채널을 색 하나에만 의존하지 않는다.

공정성은 쉬움이 아니라 정보·인과·대응 가능성이 유지되는 어려움이다.

## 8.4 적 전투 AI와 공격·위협 예산

영리함과 압박량을 분리한다.

```text
개별 적 판단
→ 감지·기억·행동 후보·Utility·쿨다운

전투 조율자
→ 역할·위치 슬롯·공격 예산·위협 예산·동시 강공격 제한

난이도·페이싱 디렉터
→ 웨이브·증원·예산 상한·회복 구간·긴장도·다음 전투 조절
```

공격 권한을 받지 못한 적은 멈추지 않고 선회·엄폐·장전·경고·재배치를 수행한다. 쉬움 난이도에서 적을 멍청하게 만들기보다 반응시간, 동시 공격, 전술 빈도, 회복 폭과 자원 지원을 조절한다.

## 8.5 긴장도 곡선

```text
Build Up
→ Sustain Peak
→ Peak Fade
→ Relax
→ 다음 Build Up
```

계속 최고 압박을 유지하면 아슬아슬함이 아니라 피로가 된다. Peak 뒤에는 결과 이해, 회복, 보상, 장비·경로 선택 시간이 필요하다.

## 8.6 고정·적응형 난이도

고정 난이도는 먼저 경험 의도를 정한 뒤 다음 순서로 조절한다.

1. 정보·예고·반응·회복·동시 공격
2. 측면·엄폐·정보 공유·역할 교대 등 전술 빈도
3. 웨이브·특수 적·회복 구간·자원
4. 체력·피해·속도 등 수치

적응형 난이도는 장기 실력과 단기 스트레스를 분리한다. 히스테리시스, 최소 상태 유지시간, 변경 쿨다운, 한 번에 한 단계, 안전한 적용 시점을 둔다. 현재 플레이어가 보고 있는 적의 체력·피해를 갑자기 바꾸는 것을 기본값으로 삼지 않는다.

**성공을 벌주지 않는다.** 좋은 장비·숙련 직후 적 수치를 같은 비율로 올려 성장 체감을 무효화하지 않고, 이후 구간에서 더 다양한 조합·선택·전술을 제공한다.

텔레메트리는 전투 시간, 최저 체력, 피해 폭증, 동시 공격자, 예산 사용량, 무력화 시간, 카메라 밖 피해, 자원 소비, 사망 직전 상태와 난이도 변경 이유를 기록할 수 있다. 감정과 원인은 플레이 영상·관찰·인터뷰를 결합해 판정한다."""
    text = insert_before(text, "## 9. 온보딩과 점진적 공개", addition)
    write(path, text)


def update_changelog() -> None:
    path = "docs/CHANGELOG.md"
    text = read(path)
    bullet = "- 게임 시스템·난이도·전투 AI 설계 구조를 기존 `analyzing-and-refining-game-concepts`의 `system-design`·`difficulty-and-combat-ai` Mode로 통합했다. 새 독립 Skill을 추가하지 않음으로써 주 책임 분야 중복을 피하고, 전용 reference·프로젝트 contract·Registry trigger·사람용 라우팅·게임 기획 Guide·TDD 계약을 연결했다."
    text = insert_after(
        text,
        "## Unreleased - Base audit and operating-contract consistency",
        bullet,
    )
    write(path, text)


def update_learning_log() -> None:
    path = "skills/SKILL_LEARNING_LOG.md"
    text = read(path)
    entry = """## 2026-07-29 — 난이도·전투 AI 설계 책임 통합

- **Trigger:** 적 AI를 영리하면서도 사용자 수준에 맞게 균형을 유지하고 아슬아슬한 긴장감을 만들 수 있도록 게임 설계·난이도 설계 Skill과 작업 구조로 공용화하라는 요청.
- **Finding:** 기존 `analyzing-and-refining-game-concepts`가 플레이어 경험·게임 요소 정렬·벤치마크·플레이테스트·PoC를 이미 책임한다. 별도 난이도·전투 AI Skill을 만들면 주 책임 분야와 Evidence·검증 절차가 중복된다.
- **Decision:** **새 Skill을 추가하지 않음**. 기존 Skill에 `system-design`과 `difficulty-and-combat-ai` Mode를 추가하고, 개별 적 판단·전투 조율자·난이도/페이싱 디렉터, 공격·위협 예산, 공정성 안전 규칙, 고정·적응형 난이도, 텔레메트리·플레이테스트를 전용 reference와 Template로 분리한다.
- **Boundary:** 반응시간·예산·배율·적 역할·스테이지 규칙·Godot 구현 상태는 프로젝트 전용 유지다. Base는 입력·판정·검증·공용화 경계만 제공한다.
- **Learning state:** 구조와 계약은 `HYPOTHESIS`이며 **프로젝트 Pilot 검증 대기**다.
- **Promotion guard:** 한 프로젝트나 한 번의 성공을 공용 강제 규칙으로 승격하지 않음. 실제 문구는 **한 번의 성공을 공용 강제 규칙으로 승격하지 않음**이며, 서로 다른 프로젝트에서 공정성·긴장도·오라우팅·밸런스 조정 비용을 비교한 뒤 재검토한다.
- **Next trigger:** 모바일 실시간 전투와 PC 전술·액션 프로젝트에서 각각 적용해 사망 원인 설명 가능성, 피해 폭증, 동시 공격, 플레이어 자기보고, 조정 비용을 비교할 때 재검토한다."""
    text = insert_after(text, "# Base Skill Learning Log", entry)
    write(path, text)


def main() -> None:
    update_registry()
    update_start_here()
    update_documentation_map()
    update_guide()
    update_changelog()
    update_learning_log()


if __name__ == "__main__":
    main()
