from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel: str, text: str) -> None:
    (ROOT / rel).write_text(text, encoding="utf-8", newline="\n")


def replace_once(rel: str, old: str, new: str, label: str) -> None:
    text = read(rel)
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly 1 match, got {count}")
    write(rel, text.replace(old, new, 1))


def run(*args: str) -> None:
    print("$", " ".join(args))
    subprocess.run(args, cwd=ROOT, check=True)


def patch_agents() -> None:
    rel = "AGENTS.md"
    replace_once(
        rel,
        "REQUIRED_WORK_REMAINING\nFIGMA_DEFAULT_VISUAL_WORKSPACE\nCURRENT_PAID_PLANS: GPT_PRO, FIGMA_PRO",
        "REQUIRED_WORK_REMAINING\nFIGMA_USAGE: DISABLED_BY_USER\nLEGACY_FIGMA_REFERENCE\nCURRENT_PAID_PLANS: GPT_PRO, FIGMA_PRO",
        "AGENTS machine contract",
    )
    replace_once(
        rel,
        "- 새 시각 작업의 기본 협업면은 프로젝트별 Figma이며, balance/economy/schema/runtime config는 repo-native structured source를 사용한다. 기존 Google Sheets는 검증된 migration이 끝날 때까지 legacy proposal/migration source로 보존한다.",
        "- 새 시각 작업에는 고정 외부 시각 workspace를 강제하지 않는다. GitHub 정본과 repo-native 구조화 데이터·프로젝트 자산·사용자가 승인한 현재 artifact surface를 사용하며, `FIGMA_USAGE: DISABLED_BY_USER`를 따른다. 기존 Google Sheets는 검증된 migration이 끝날 때까지 legacy proposal/migration source로 보존한다.",
        "AGENTS long-horizon summary",
    )
    replace_once(
        rel,
        "- 새 프로젝트·새 시각 기획의 기본 협업면은 `FIGMA_DEFAULT_VISUAL_WORKSPACE`다. 화면·컴포넌트·상태·프로토타입·승인 레퍼런스는 프로젝트 Figma에 구조화하고, 규칙·Decision은 GitHub 정본, 밸런스·경제·schema·runtime config는 repo-native structured source가 소유한다.",
        "- 새 프로젝트·새 시각 기획에는 고정 외부 시각 workspace를 두지 않는다. 화면·컴포넌트·상태·프로토타입·승인 레퍼런스는 GitHub 정본에 연결된 프로젝트 문서·repo-native 자산 또는 사용자가 승인한 현재 artifact surface에서 관리하고, 규칙·Decision은 GitHub 정본, 밸런스·경제·schema·runtime config는 repo-native structured source가 소유한다. `FIGMA_DEFAULT_VISUAL_WORKSPACE`는 `LEGACY_FIGMA_REFERENCE`로만 남고 `FIGMA_USAGE: DISABLED_BY_USER`가 현재 권위다.",
        "AGENTS project visual workspace",
    )
    replace_once(
        rel,
        "Sheet-only 고유 내용과 proposal을 GitHub/Figma/repo-native source에 reconcile하고 readback·replacement pointer를 확인하기 전에는 삭제·폐기·migration 완료를 주장하지 않는다.",
        "Sheet-only 고유 내용과 proposal을 GitHub/repo-native source와 사용자가 승인한 project artifact에 reconcile하고 readback·replacement pointer를 확인하기 전에는 삭제·폐기·migration 완료를 주장하지 않는다.",
        "AGENTS Sheet migration destination",
    )
    replace_once(
        rel,
        "새 작업의 기본 workspace 권위는 이 파일과 `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`의 Figma/repo-native 전환 규칙이 우선한다.",
        "새 작업의 workspace 권위는 이 파일과 `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`의 Figma 비활성/repo-native 전환 규칙이 우선한다.",
        "AGENTS Sheet authority",
    )
    replace_once(
        rel,
        "- 일반 기획·상태 확인은 GitHub 정본을 우선하고, 시각 협업은 프로젝트 Figma, 구조화 데이터는 repo-native source를 사용한다. 기존 Sheet는 migration/proposal 확인이 필요한 경우에만 읽는다.",
        "- 일반 기획·상태 확인은 GitHub 정본을 우선하고, 시각 협업은 GitHub 정본에 연결된 프로젝트 문서·repo-native 자산·사용자가 승인한 현재 artifact surface, 구조화 데이터는 repo-native source를 사용한다. Figma는 사용하지 않으며, 기존 Sheet는 migration/proposal 확인이 필요한 경우에만 읽는다.",
        "AGENTS current planning route",
    )


def patch_long_horizon() -> None:
    rel = "docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md"
    replace_once(
        rel,
        "REUSABLE_SYSTEM_EXTRACTION\nFIGMA_DEFAULT_VISUAL_WORKSPACE\nREPO_NATIVE_STRUCTURED_DATA",
        "REUSABLE_SYSTEM_EXTRACTION\nFIGMA_USAGE: DISABLED_BY_USER\nLEGACY_FIGMA_REFERENCE\nREPO_NATIVE_STRUCTURED_DATA",
        "long-horizon machine contract",
    )
    old = '''## 9. Figma·Google Sheets·구조화 데이터 전환

### `FIGMA_DEFAULT_VISUAL_WORKSPACE`

새 프로젝트와 새 기획 작업의 **시각 협업 기본 작업면**은 프로젝트별 Figma다.

Figma가 소유하기 적합한 것:

- 방향 무드와 승인 레퍼런스
- 화면·컴포넌트·상태·프로토타입
- 이미지/시각 자료의 구조화·레이어화·재사용 분류
- WIP / Approved / Rejected / Final 시각 상태
- 구현에 pin한 visual handoff view

Figma는 게임 규칙·런타임 데이터·테스트 결과의 정본이 아니며, Figma readback 없이 업로드/동기화를 성공으로 주장하지 않는다.

### `REPO_NATIVE_STRUCTURED_DATA`

다음은 Figma로 옮겨 두 번째 정본을 만들지 않는다.

- 밸런스 수치
- 경제/확률
- schema
- runtime configuration
- save/state data contract
- 테스트용 fixture

프로젝트 기술에 맞는 JSON, CSV, Godot Resource 등 **repo-native structured source**를 정본으로 사용한다. 사람용 시각 요약은 Figma에서 해당 정본의 ID/Commit을 참조할 수 있다.
'''
    new = '''## 9. 시각 협업·Google Sheets·구조화 데이터 전환

### `FIGMA_USAGE: DISABLED_BY_USER`

현재 Figma는 Base와 Base 적용 프로젝트의 기본·보조·fallback 작업면이 아니다. 사용자가 다시 명시적으로 승인하기 전에는 Figma workspace·connector·MCP·Visual Bible·delivery 경로를 선택하거나 자동 read/write하지 않는다.

`LEGACY_FIGMA_REFERENCE`는 과거 계약·Template·도구·evidence의 provenance와 호환성을 해석하기 위한 표식이다. 과거 안정 계약명 `FIGMA_DEFAULT_VISUAL_WORKSPACE`가 문서·테스트·Archive에 남아 있어도 현재 라우팅 권위를 갖지 않는다.

새 프로젝트와 새 기획 작업에는 고정 외부 시각 workspace를 강제하지 않는다. 방향 무드·승인 레퍼런스·화면·컴포넌트·상태·프로토타입·이미지 구조화 자료는 GitHub 정본에 연결된 프로젝트 문서, repo-native 자산 또는 사용자가 승인한 현재 artifact surface에서 관리한다. Notion 공식 자료는 Skill·작업구조 학습 Source로 조사할 수 있지만 Figma를 대체하는 자동 시각 workspace로 승격하지 않는다.

### `REPO_NATIVE_STRUCTURED_DATA`

다음은 외부 시각 workspace로 옮겨 두 번째 정본을 만들지 않는다.

- 밸런스 수치
- 경제/확률
- schema
- runtime configuration
- save/state data contract
- 테스트용 fixture

프로젝트 기술에 맞는 JSON, CSV, Godot Resource 등 **repo-native structured source**를 정본으로 사용한다. 사람용 시각 요약은 해당 정본의 ID/Commit과 연결되는 프로젝트 문서·자산·승인 artifact로만 파생한다.
'''
    replace_once(rel, old, new, "long-horizon section 9")
    replace_once(
        rel,
        "→ visual/human-facing content → Figma\n→ structured runtime/balance data → repo-native source\n→ Figma/repo readback",
        "→ visual/human-facing content → repo/project approved artifact\n→ structured runtime/balance data → repo-native source\n→ repo/project artifact readback",
        "long-horizon Sheet migration flow",
    )
    replace_once(
        rel,
        "- 새 GitHub/Figma 위치 readback",
        "- 새 GitHub/repo-native/승인 project artifact 위치 readback",
        "long-horizon Sheet readback criterion",
    )
    replace_once(
        rel,
        "## 10. Tool Hub·외부 HTML 카탈로그·Figma",
        "## 10. Tool Hub·외부 HTML 카탈로그",
        "long-horizon section 10 title",
    )
    replace_once(
        rel,
        "- 실제 구현·데이터·자산·Tool/Runtime·Figma/구조화 데이터 경계",
        "- 실제 구현·데이터·자산·Tool/Runtime·legacy Figma 비활성·구조화 데이터 경계",
        "long-horizon adversarial scope",
    )
    replace_once(
        rel,
        "- 현재 사용 가능한 유료 플랜은 **GPT Pro와 Figma Pro 정확히 두 개**다.\n- 두 플랜 안에서 이미 포함된 기능은 사용할 수 있지만, 별도 API·credit·metered billing·marketplace·runner·compute·storage·추가 SaaS 과금으로 넘어가면 허용 범위 밖이다.",
        "- 현재 비용 inventory에는 **GPT Pro와 Figma Pro 정확히 두 개**가 기록되어 있다. Figma Pro 기록은 사용 승인이나 활성 workspace 지정을 뜻하지 않는다.\n- GPT Pro에 이미 포함된 기능은 별도 API·credit·metered billing·marketplace·runner·compute·storage·추가 SaaS 과금으로 넘어가지 않는 범위에서 사용할 수 있다. Figma는 `FIGMA_USAGE: DISABLED_BY_USER`이므로 구독 포함 여부와 무관하게 사용하지 않는다.",
        "long-horizon cost wording",
    )


def patch_visual_policy() -> None:
    rel = "docs/VISUAL_COLLABORATION_TOOL_POLICY.md"
    replace_once(
        rel,
        "Figma와 Whimsical은 기획·UX/UI·인계·검토를 돕는 `VISUAL_WORKSPACE`다. 어느 도구도 GitHub의 승인 결정·상세 규칙·구현 계약·실제 Godot 상태를 대체하지 않는다.\n\n## Context and authority",
        "## Legacy Figma policy — inactive\n\n`LEGACY_FIGMA_REFERENCE`: 아래 Figma/Whimsical 상세 규칙은 과거 결정·기존 Template·도구·evidence를 해석하기 위한 호환성 기록이며, 현재 작업에서 실행·라우팅 지시로 사용하지 않는다. 과거에는 Figma와 Whimsical을 기획·UX/UI·인계·검토용 `VISUAL_WORKSPACE`로 다뤘다.\n\n## Legacy context and authority",
        "visual policy legacy boundary",
    )
    replace_once(
        rel,
        "새 프로젝트와 새 시각 작업의 기본 협업면은 `FIGMA_DEFAULT_VISUAL_WORKSPACE`다.",
        "과거 정책의 안정 계약명은 `FIGMA_DEFAULT_VISUAL_WORKSPACE`였지만 현재는 `LEGACY_FIGMA_REFERENCE`이며, 새 프로젝트와 새 시각 작업에는 적용하지 않는다.",
        "visual policy stale default",
    )


def patch_tests() -> None:
    rel = "tests/test_base_long_horizon_work_contract.py"
    replace_once(
        rel,
        '''        for term in (
            "FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS",
            "REQUIRED_WORK_REMAINING",
            "FIGMA_DEFAULT_VISUAL_WORKSPACE",
        ):
''',
        '''        for term in (
            "FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS",
            "REQUIRED_WORK_REMAINING",
            "FIGMA_USAGE: DISABLED_BY_USER",
            "LEGACY_FIGMA_REFERENCE",
        ):
''',
        "base long-horizon entrypoint test",
    )
    replace_once(
        rel,
        '''        for term in (
            "FIGMA_DEFAULT_VISUAL_WORKSPACE",
            "REPO_NATIVE_STRUCTURED_DATA",
''',
        '''        for term in (
            "FIGMA_USAGE: DISABLED_BY_USER",
            "LEGACY_FIGMA_REFERENCE",
            "REPO_NATIVE_STRUCTURED_DATA",
''',
        "base long-horizon visual authority test",
    )
    replace_once(
        rel,
        '''        self.assertIn("GPT Pro/Figma Pro", long_horizon)
        self.assertIn("요금제·권한", visual_policy)
''',
        '''        self.assertIn("GPT Pro/Figma Pro", long_horizon)
        self.assertIn("FIGMA_USAGE: DISABLED_BY_USER", long_horizon)
        self.assertIn("LEGACY_FIGMA_REFERENCE", visual_policy)
        self.assertIn("요금제·권한", visual_policy)
''',
        "base long-horizon legacy cost test",
    )

    rel = "tests/test_uiux_external_reference_absorption.py"
    replace_once(
        rel,
        '''        long_horizon = LONG_HORIZON.read_text(encoding="utf-8")
        visual_policy = VISUAL_POLICY.read_text(encoding="utf-8")

        for text in (long_horizon, visual_policy):
''',
        '''        agents = AGENTS.read_text(encoding="utf-8")
        long_horizon = LONG_HORIZON.read_text(encoding="utf-8")
        visual_policy = VISUAL_POLICY.read_text(encoding="utf-8")

        for text in (agents, long_horizon, visual_policy):
''',
        "uiux Figma active-route test scope",
    )
    replace_once(
        rel,
        '''        self.assertNotIn(
            "새 프로젝트와 새 기획 작업의 **시각 협업 기본 작업면**은 프로젝트별 Figma다.",
            long_horizon,
        )
''',
        '''        self.assertNotIn("새 시각 작업의 기본 협업면은 프로젝트별 Figma", agents)
        self.assertNotIn("새 프로젝트·새 시각 기획의 기본 협업면은 `FIGMA_DEFAULT_VISUAL_WORKSPACE`다.", agents)
        self.assertNotIn("시각 협업은 프로젝트 Figma", agents)
        self.assertNotIn(
            "새 프로젝트와 새 기획 작업의 **시각 협업 기본 작업면**은 프로젝트별 Figma다.",
            long_horizon,
        )
''',
        "uiux Figma stale AGENTS assertions",
    )


def main() -> None:
    patch_agents()
    patch_long_horizon()
    patch_visual_policy()
    patch_tests()
    run("python", "-m", "unittest", "tests.test_uiux_external_reference_absorption", "tests.test_base_long_horizon_work_contract")
    run("git", "diff", "--check")

    # Remove the temporary migration harness before the verified commit is created.
    for rel in (".github/workflows/one-shot-figma-retirement-cleanup.yml", "tools/one_shot_figma_retirement_cleanup.py"):
        path = ROOT / rel
        if path.exists():
            path.unlink()


if __name__ == "__main__":
    main()
