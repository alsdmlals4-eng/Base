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
        raise RuntimeError(f"{label}: expected 1 match, got {count}")
    write(rel, text.replace(old, new, 1))


def replace_all(rel: str, old: str, new: str, label: str, expected: int | None = None) -> None:
    text = read(rel)
    count = text.count(old)
    if expected is not None and count != expected:
        raise RuntimeError(f"{label}: expected {expected} matches, got {count}")
    if count == 0:
        raise RuntimeError(f"{label}: no matches")
    write(rel, text.replace(old, new))


def patch_documentation_map() -> None:
    rel = "docs/DOCUMENTATION_MAP.md"
    replace_once(
        rel,
        "| 프로젝트 작업면 현행 권한 | `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json` | `FIGMA_DEFAULT_VISUAL_WORKSPACE`, `REPO_NATIVE_STRUCTURED_DATA`, `GOOGLE_SHEETS_LEGACY_MIGRATION_SOURCE`의 current machine contract; frozen v9 artifact는 호환·역사 증거로 보존 |",
        "| 프로젝트 작업면 현행 권한 | `AGENTS.md`, `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`, `docs/VISUAL_COLLABORATION_TOOL_POLICY.md` | `FIGMA_USAGE: DISABLED_BY_USER`, `LEGACY_FIGMA_REFERENCE`, `REPO_NATIVE_STRUCTURED_DATA`, `GOOGLE_SHEETS_LEGACY_MIGRATION_SOURCE`; 고정 외부 시각 workspace를 강제하지 않음 |",
        "documentation map workspace authority",
    )
    replace_once(
        rel,
        "| 시각 협업 도구 | `docs/VISUAL_COLLABORATION_TOOL_POLICY.md` | `FIGMA_DEFAULT_VISUAL_WORKSPACE`의 화면·컴포넌트·상태·프로토타입·승인 레퍼런스와 `REPO_NATIVE_STRUCTURED_DATA`의 구조화 데이터 경계를 정의; Figma는 게임 규칙·runtime data 정본이 아님 |",
        "| 시각 협업 도구 | `docs/VISUAL_COLLABORATION_TOOL_POLICY.md` | `FIGMA_USAGE: DISABLED_BY_USER`; 과거 Figma 계약은 `LEGACY_FIGMA_REFERENCE`로만 보존하고 현재 시각 작업은 GitHub 정본·repo-native 자산·승인 artifact를 사용 |",
        "documentation map visual policy",
    )
    replace_once(
        rel,
        "| 로컬 Tool 공용 런타임 계약 | `tools/base-tool-contracts/README.md`, `schemas/project-figma-target-registry-v1.schema.json`, `schemas/project-approved-anchor-registry-v1.schema.json` | 단일 Figma parser, project-owned anchor evidence, gitignored vault confinement |",
        "| 로컬 Tool 공용 런타임 계약 | `tools/base-tool-contracts/README.md`, `schemas/project-figma-target-registry-v1.schema.json`, `schemas/project-approved-anchor-registry-v1.schema.json` | legacy Figma parser는 호환성 자료로만 보존; current project-owned anchor evidence와 gitignored vault confinement은 계속 사용 |",
        "documentation map local tool legacy boundary",
    )
    replace_once(
        rel,
        "일반 프로젝트의 기획·상태 확인은 GitHub 정본을 우선하고, 시각 협업은 프로젝트별 `FIGMA_DEFAULT_VISUAL_WORKSPACE`, 밸런스·경제·schema·runtime config는 `REPO_NATIVE_STRUCTURED_DATA`를 사용한다. 기존 구성된 Google Sheets는 migration/proposal reconciliation이 필요한 동안만 `GOOGLE_SHEETS_LEGACY_MIGRATION_SOURCE`로 읽는다. HTML 대시보드는 사용자 명시 요청 또는 기존 유지보수에만 사용한다.",
        "일반 프로젝트의 기획·상태 확인은 GitHub 정본을 우선한다. `FIGMA_USAGE: DISABLED_BY_USER`이므로 시각 협업에 Figma를 사용하지 않고, GitHub 정본에 연결된 프로젝트 문서·repo-native 자산·사용자가 승인한 현재 artifact surface를 사용한다. 밸런스·경제·schema·runtime config는 `REPO_NATIVE_STRUCTURED_DATA`를 사용하며, 기존 구성된 Google Sheets는 migration/proposal reconciliation이 필요한 동안만 `GOOGLE_SHEETS_LEGACY_MIGRATION_SOURCE`로 읽는다. HTML 대시보드는 사용자 명시 요청 또는 기존 유지보수에만 사용한다.",
        "documentation map current project route",
    )


def patch_sheet_policy() -> None:
    rel = "docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md"
    replace_once(
        rel,
        "FIGMA_DEFAULT_VISUAL_WORKSPACE\nREPO_NATIVE_STRUCTURED_DATA",
        "FIGMA_USAGE: DISABLED_BY_USER\nLEGACY_FIGMA_REFERENCE\nREPO_NATIVE_STRUCTURED_DATA",
        "sheet policy machine contract",
    )
    replace_once(
        rel,
        "새 프로젝트와 새 시각 작업의 기본 협업면은 Figma이며, 승인 Decision·상세 규칙은 GitHub 정본, 밸런스·경제·Schema·runtime config 같은 구조화 데이터는 repo-native source가 소유한다.",
        "`FIGMA_USAGE: DISABLED_BY_USER`가 현재 권위다. 새 프로젝트와 새 시각 작업에는 고정 외부 시각 workspace를 두지 않으며 GitHub 정본에 연결된 프로젝트 문서·repo-native 자산·사용자가 승인한 현재 artifact surface를 사용한다. 과거 Figma 연결은 `LEGACY_FIGMA_REFERENCE`로만 보존한다. 승인 Decision·상세 규칙은 GitHub 정본, 밸런스·경제·Schema·runtime config 같은 구조화 데이터는 repo-native source가 소유한다.",
        "sheet policy active visual workspace",
    )
    replace_once(
        rel,
        "**적응:** 기존 Google Sheets에서는 장문 페이지 대신 카드형 요약·Decision ID·정본 경로·상태를 사용하고, migration 뒤 책임 surface는 GitHub/Figma/repo-native로 분리한다.",
        "**적응:** 기존 Google Sheets에서는 장문 페이지 대신 카드형 요약·Decision ID·정본 경로·상태를 사용하고, migration 뒤 책임 surface는 GitHub/repo-native/승인 project artifact로 분리한다.",
        "sheet policy migration target",
    )
    replace_once(
        rel,
        "- **시각 작업면 색인:** `06_시각_작업면`은 실제 Figma·Whimsical·기타 Artifact가 있을 때만 쓴다. 각 행은 `Artifact ID`, `usage_context`(`GDD|EXTERNAL_COLLABORATION|BOTH`), 목적, Decision ID, 책임 정본, 링크·Snapshot, 상태와 다음 Gate만 가진다. 보드·Frame 전문을 Sheet에 복사하지 않는다. GDD 안·밖 어느 용도도 이 색인을 통해 연결할 수 있으며, 사용하지 않는 프로젝트에 tab을 강제하지 않는다.",
        "- **시각 작업면 색인:** `06_시각_작업면`은 실제 프로젝트-local 또는 사용자가 승인한 외부 Artifact가 있을 때만 쓴다. `FIGMA_USAGE: DISABLED_BY_USER` 동안 과거 Figma link는 `LEGACY_FIGMA_REFERENCE`로만 해석하고 접근·동기화하지 않는다. 각 행은 `Artifact ID`, `usage_context`(`GDD|EXTERNAL_COLLABORATION|BOTH`), 목적, Decision ID, 책임 정본, 링크·Snapshot, 상태와 다음 Gate만 가진다. 보드·Frame 전문을 Sheet에 복사하지 않는다. GDD 안·밖 어느 용도도 이 색인을 통해 연결할 수 있으며, 사용하지 않는 프로젝트에 tab을 강제하지 않는다.",
        "sheet policy visual index",
    )


def patch_art_skill() -> None:
    rel = "skills/designing-art-prompts-and-technique-cards/SKILL.md"
    replace_once(
        rel,
        "프로젝트용 이미지 후보의 **필요성·우선순위·재사용·제작 방식 선정**은 이 스킬이 새로 판단하지 않는다. `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`의 `Visual Requirement Gate`가 먼저 소유하고, 이 스킬은 선정된 requirement를 실제 생성·편집·검수 계약으로 변환한다.\n\n프로젝트가 Figma Visual Bible을 구성했거나 Visual Artifact Registry가 Figma Artifact를 가리키면 `references/figma-visual-bible-continuity-gate.md`를 적용한다. 이 gate는 최신 프로젝트 정본·Decision보다 우선하지 않으며, 승인된 Figma frame/node를 실제로 읽을 수 있을 때만 시각 일관성 근거로 사용한다.\n\n### Conditional Figma-direct visual modules\n\nFigma continuity gate를 적용한 뒤 현재 작업에 필요한 reference만 추가로 읽는다. 아래 파일은 패키지 무결성을 위해 이 Skill이 직접 소유·색인하지만, 매 이미지 작업에서 전부 로드하지 않는다.",
        "프로젝트용 이미지 후보의 **필요성·우선순위·재사용·제작 방식 선정**은 이 스킬이 새로 판단하지 않는다. `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`의 `Visual Requirement Gate`가 먼저 소유하고, 이 스킬은 선정된 requirement를 실제 생성·편집·검수 계약으로 변환한다.\n\n## Active Figma retirement guard\n\n`FIGMA_USAGE: DISABLED_BY_USER`가 현재 권위다. 사용자가 Figma 재도입을 명시적으로 승인하기 전에는 Figma workspace·Visual Bible·frame/node·connector·MCP를 읽거나 쓰지 않고, Figma continuity/direct reference를 실행 경로로 로드하지 않는다. 프로젝트에 과거 Figma pointer가 남아 있으면 `LEGACY_FIGMA_REFERENCE`로만 분류하고 현재 프로젝트 정본·repo-native 승인 자산·Visual Artifact Registry의 비-Figma 승인 reference를 사용한다.\n\n### Legacy Figma-direct visual modules — inactive\n\n아래 Figma 전용 reference는 과거 패키지·evidence의 provenance와 호환성을 위해 이 Skill이 계속 소유·색인하지만 `FIGMA_USAGE: DISABLED_BY_USER` 동안 정상 이미지 작업에서 로드하거나 실행하지 않는다.",
        "art skill active guard",
    )
    replace_once(
        rel,
        "정상 이미지 작업에서는 기존 image 관련 trigger와 `figma-visual-bible-continuity-gate.md`가 이 모듈을 조건부로 고른다. 별도 Figma/Expression/Sprite broad Skill을 만들거나 Tool Hub·PowerShell·localhost delivery를 기본 경로로 요구하지 않는다.",
        "정상 이미지 작업에서는 기존 image 관련 trigger만 사용하고 Figma 전용 gate/module은 선택하지 않는다. Figma 재도입이 별도 승인되기 전까지 과거 reference는 `LEGACY_FIGMA_REFERENCE`로만 남긴다. 별도 Figma/Expression/Sprite broad Skill을 만들거나 Tool Hub·PowerShell·localhost delivery를 기본 경로로 요구하지 않는다.",
        "art skill module routing",
    )
    replace_once(
        rel,
        "- 구성된 프로젝트라면 Figma Visual Bible 상태, 연결된 `APPROVED_VISUAL_REFERENCE` ID와 frame/node ID, `Keep / Avoid / Do Not Drift`.",
        "- 프로젝트 정본·repo-native 자산 또는 비-Figma Visual Artifact Registry에서 확인한 `APPROVED_VISUAL_REFERENCE` ID·경로·source commit과 `Keep / Avoid / Do Not Drift`. 과거 Figma pointer는 `LEGACY_FIGMA_REFERENCE`로만 기록한다.",
        "art skill required inputs",
    )
    replace_once(
        rel,
        "2. 프로젝트가 Figma Visual Bible을 구성했거나 Registry가 Figma Artifact를 가리키면 `references/figma-visual-bible-continuity-gate.md`로 승인 reference를 확인한다. 실제 frame/node 접근이 실패하면 `LINK_UNVERIFIED / AUTH_REQUIRED / ACCESS_DENIED / BLOCKED_UNVERIFIED`를 기록하고 WIP·Rejected·과거 대화를 승인 기준으로 추정 사용하지 않는다.",
        "2. 프로젝트 정본·repo-native 승인 자산·Visual Artifact Registry에서 현재 승인 reference를 확인한다. Registry가 과거 Figma Artifact를 가리키면 접근하지 않고 `LEGACY_FIGMA_REFERENCE`로 분류한 뒤 비-Figma 현재 reference가 없으면 `MISSING_CANON / BLOCKED_UNVERIFIED`를 기록한다. WIP·Rejected·과거 대화를 승인 기준으로 추정 사용하지 않는다.",
        "art skill process step 2",
    )
    replace_once(
        rel,
        "5. 원본에서 유지할 요소와 변경할 요소를 분리한다. Figma 승인 reference가 있으면 `Keep / Avoid / Do Not Drift`를 이 계약에 병합한다.",
        "5. 원본에서 유지할 요소와 변경할 요소를 분리한다. 현재 승인 visual reference가 있으면 `Keep / Avoid / Do Not Drift`를 이 계약에 병합한다.",
        "art skill process step 5",
    )
    replace_once(
        rel,
        "→ 승인된 Figma reference ID·Keep/Avoid/Do Not Drift (구성된 경우)",
        "→ 승인된 visual reference ID·경로·source commit·Keep/Avoid/Do Not Drift (있는 경우)",
        "art skill prompt architecture",
    )
    replace_once(
        rel,
        "12. 생성 뒤 `visual-qa-and-approval`을 실행하고 `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`에 기록한다. Figma를 쓰는 프로젝트에서는 새 결과를 기본 WIP/review 후보로 두고 승인 reference와 일관성을 비교한다.\n13. 승인된 Decision만 정본·GitHub·Sheet·Asset Ledger와 Visual Artifact Registry에 동기화한다. 사용자 승인 전 Figma `01_APPROVED_REFERENCE` 또는 `04_FINAL`로 자동 승격하지 않는다.\n14. 모델·버전·입력 이미지·확인일 또는 Figma 승인 reference가 달라지면 재검증한다.",
        "12. 생성 뒤 `visual-qa-and-approval`을 실행하고 `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`에 기록한다. 새 결과를 WIP/review 후보로 두고 현재 승인 reference와 일관성을 비교한다.\n13. 승인된 Decision만 정본·GitHub·Sheet·Asset Ledger와 Visual Artifact Registry에 동기화한다. 과거 Figma Artifact는 `LEGACY_FIGMA_REFERENCE`로 유지하고 새 Figma 상태를 만들거나 동기화하지 않는다.\n14. 모델·버전·입력 이미지·확인일 또는 현재 승인 visual reference가 달라지면 재검증한다.",
        "art skill post generation flow",
    )
    replace_once(
        rel,
        "이미지 생성 도구가 없거나 권한이 없으면 텍스트 와이어프레임·Mermaid·Figma 대체안을 쓴다.",
        "이미지 생성 도구가 없거나 권한이 없으면 텍스트 와이어프레임·Mermaid 또는 프로젝트-local 구조화 artifact를 쓴다.",
        "art skill intermediate fallback",
    )
    replace_once(
        rel,
        "이 mode의 결과는 `DRAFT_VISUAL`이며 최종 리소스·라이선스 승인·Figma 구현 명세·Godot 구현·런타임/사람 검증을 뜻하지 않는다.",
        "이 mode의 결과는 `DRAFT_VISUAL`이며 최종 리소스·라이선스 승인·제품 구현 명세·Godot 구현·런타임/사람 검증을 뜻하지 않는다.",
        "art skill intermediate evidence ceiling",
    )
    replace_once(
        rel,
        "- Figma Visual Bible을 쓰는 프로젝트라면 실제로 확인한 `APPROVED_VISUAL_REFERENCE`와 비율·실루엣·palette·재질·광원·camera·UI hierarchy가 일관적인가.",
        "- 현재 프로젝트에 `APPROVED_VISUAL_REFERENCE`가 있으면 실제로 확인한 비-Figma reference와 비율·실루엣·palette·재질·광원·camera·UI hierarchy가 일관적인가.",
        "art skill QA checklist",
    )
    replace_once(
        rel,
        "- Figma Visual Bible 적용 시 확인한 승인 reference ID·일관성 판정·미검증 상태.",
        "- 현재 승인 visual reference ID·경로·source commit·일관성 판정·미검증 상태.",
        "art skill expected outputs",
    )
    replace_once(
        rel,
        "- Figma Visual Bible이 구성됐는데 연결된 승인 reference를 확인하지 않고 과거 대화나 WIP를 기준으로 삼는다.\n- 읽을 수 없는 Figma frame/node를 확인했다고 보고한다.\n- Figma `04_FINAL`을 `PROJECT_ASSET_APPROVED`나 Godot runtime proof로 간주한다.",
        "- 현재 승인 visual reference를 확인하지 않고 과거 대화나 WIP를 기준으로 삼는다.\n- `LEGACY_FIGMA_REFERENCE`를 현재 reference로 사용하거나 Figma frame/node를 읽었다고 보고한다.\n- 과거 Figma `04_FINAL` 기록을 `PROJECT_ASSET_APPROVED`나 Godot runtime proof로 간주한다.",
        "art skill failure conditions",
    )
    replace_once(
        rel,
        "8. Figma 승인 reference가 있는 프로젝트의 새 이미지가 `Keep / Avoid / Do Not Drift`에서 벗어나면 `REVISION_REQUIRED`로 돌리고, 최신 정본과 Figma가 충돌하면 `VISUAL_CANONICAL_CONFLICT`로 분리한다.",
        "8. 현재 승인 visual reference가 있는 프로젝트의 새 이미지가 `Keep / Avoid / Do Not Drift`에서 벗어나면 `REVISION_REQUIRED`로 돌리고, 최신 정본과 승인 reference가 충돌하면 `VISUAL_CANONICAL_CONFLICT`로 분리한다.",
        "art skill test scenario",
    )
    replace_once(
        rel,
        "- Figma가 구성된 프로젝트는 승인 reference 확인·접근 상태·일관성 판정이 기록됐다.",
        "- 승인 visual reference가 있는 프로젝트는 reference ID·경로·source commit·일관성 판정이 기록됐다. `LEGACY_FIGMA_REFERENCE`는 현재 근거로 쓰지 않는다.",
        "art skill quality gate",
    )


def patch_image_policy() -> None:
    rel = "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md"
    replace_once(
        rel,
        "# GPT 이미지 생성·검수 및 프로젝트 Google Sheets 운영 정책\n",
        "# GPT 이미지 생성·검수 및 프로젝트 Google Sheets 운영 정책\n\n`FIGMA_USAGE: DISABLED_BY_USER`. 과거 Figma Visual Bible·reuse reference·workspace 정보는 `LEGACY_FIGMA_REFERENCE`이며 현재 이미지 생성·검수의 입력·동기화·fallback 경로로 사용하지 않는다. 현재 시각 근거는 프로젝트 정본·repo-native 승인 자산·비-Figma 승인 artifact가 소유한다.\n",
        "image policy active status",
    )
    replace_once(rel, "기존 승인 자산 / Figma Visual Bible 조회", "기존 승인 자산 / 프로젝트-local 승인 visual reference 조회", "image policy harvest input")
    replace_once(rel, "Figma Component/Variant, Godot Theme/Scene/Resource 등 semantic rebuild", "Godot Theme/Scene/Resource 또는 프로젝트-local reusable component 등 semantic rebuild", "image policy rebuild method")
    replace_once(
        rel,
        "Harvest 완료나 Figma reuse reference 등록만으로 제품 자산 승인 상태를 올리지 않는다. `Reusable Visual Harvest Gate`는 `PROJECT_ASSET_APPROVED`, `promote`, Figma `04_FINAL`, tracked asset, Godot runtime proof를 자동 생성하거나 대체하지 않는다.",
        "Harvest 완료나 재사용 reference 등록만으로 제품 자산 승인 상태를 올리지 않는다. `Reusable Visual Harvest Gate`는 `PROJECT_ASSET_APPROVED`, `promote`, tracked asset, Godot runtime proof를 자동 생성하거나 대체하지 않는다. 과거 Figma reuse/`04_FINAL` 기록은 `LEGACY_FIGMA_REFERENCE`일 뿐 현재 승인 근거가 아니다.",
        "image policy harvest authority",
    )


def patch_image_plan() -> None:
    rel = "templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md"
    replace_once(
        rel,
        "# GPT Image Generation and Review Plan\n",
        "# GPT Image Generation and Review Plan\n\n`FIGMA_USAGE: DISABLED_BY_USER`. 이 Template에서 과거 Figma 전용 필드는 사용하지 않으며 기존 Figma 기록은 `LEGACY_FIGMA_REFERENCE`로만 해석한다.\n",
        "image plan active status",
    )
    old_fields = """figma_visual_bible_status: CONFIGURED | NOT_CONFIGURED | AUTH_REQUIRED | ACCESS_DENIED | READ_ONLY | LINK_UNVERIFIED | UNVERIFIED
figma_file_url:
figma_approved_reference_ids: []
figma_approved_frame_or_node_ids: []
figma_wip_target:
figma_interpretation_record_id:
figma_sync_status: NOT_APPLICABLE | UNVERIFIED | WIP_SYNCED | INTERPRETATION_SYNCED | FLOW_SYNCED | APPROVED_REFERENCE_SYNCED | FINAL_VISUAL_SYNCED
"""
    new_fields = """approved_visual_reference_status: CONFIGURED | NOT_CONFIGURED | LINK_UNVERIFIED | UNVERIFIED
approved_visual_reference_ids: []
approved_visual_reference_paths_or_urls: []
visual_reference_source_commits: []
interpretation_record_id:
visual_reference_sync_status: NOT_APPLICABLE | UNVERIFIED | REFERENCE_VERIFIED | REVIEW_SYNCED
"""
    replace_once(rel, old_fields, new_fields, "image plan generic reference fields")
    replace_once(
        rel,
        "Figma Visual Bible이 `CONFIGURED`이면 이미지 생성·편집 전에 Visual Artifact Registry와 연결된 `APPROVED_VISUAL_REFERENCE`의 실제 frame/node를 확인하고 `Keep / Avoid / Do Not Drift`를 작업 계약에 반영한다. 접근할 수 없으면 `AUTH_REQUIRED / ACCESS_DENIED / READ_ONLY / LINK_UNVERIFIED / UNVERIFIED`를 유지하며 내용을 확인했다고 추정하지 않는다. 상세 절차는 `skills/designing-art-prompts-and-technique-cards/references/figma-visual-bible-continuity-gate.md`를 따른다.",
        "`approved_visual_reference_status: CONFIGURED`이면 이미지 생성·편집 전에 프로젝트 정본·repo-native 승인 자산·Visual Artifact Registry에서 `APPROVED_VISUAL_REFERENCE`의 실제 경로/ID/source commit을 확인하고 `Keep / Avoid / Do Not Drift`를 작업 계약에 반영한다. 접근할 수 없으면 `LINK_UNVERIFIED / UNVERIFIED`를 유지하며 내용을 확인했다고 추정하지 않는다. 과거 Figma pointer는 `LEGACY_FIGMA_REFERENCE`로만 남기고 접근하지 않는다.",
        "image plan reference precheck",
    )
    replace_once(
        rel,
        "보존소가 `ENABLED`이면 `GENERATED_EXPLORATION / IN_REVIEW / APPROVED_CANDIDATE`는 기본적으로 `.asset-vault/library/`와 `assets/_vault_local/`의 local-only 후보로 유지한다. `PROJECT_ASSET_APPROVED` 뒤에만 `promotion_target`을 확정하고 `promote`를 실행하여 `promoted_path`를 만든다. Figma `04_FINAL`과 제품 자산 승격은 서로 다른 상태다.",
        "보존소가 `ENABLED`이면 `GENERATED_EXPLORATION / IN_REVIEW / APPROVED_CANDIDATE`는 기본적으로 `.asset-vault/library/`와 `assets/_vault_local/`의 local-only 후보로 유지한다. `PROJECT_ASSET_APPROVED` 뒤에만 `promotion_target`을 확정하고 `promote`를 실행하여 `promoted_path`를 만든다. 과거 Figma `04_FINAL` 기록은 `LEGACY_FIGMA_REFERENCE`이며 제품 자산 승격과 무관하다.",
        "image plan vault authority",
    )
    replace_once(rel, "Figma 승인 Reference", "승인 Visual Reference", "image plan backlog header")
    replace_once(
        rel,
        "`Figma 승인 Reference`는 실제로 확인한 `APPROVED_VISUAL_REFERENCE` ID만 기록한다.",
        "`승인 Visual Reference`는 실제로 확인한 `APPROVED_VISUAL_REFERENCE` ID·경로·source commit만 기록한다.",
        "image plan backlog reference rule",
    )
    replace_once(rel, "→ 승인된 Figma reference ID·Keep/Avoid/Do Not Drift (구성된 경우)", "→ 승인된 visual reference ID·경로·source commit·Keep/Avoid/Do Not Drift (있는 경우)", "image plan prompt")
    replace_once(rel, "| Review ID | Image ID | 기획 일치 | Figma 승인 Reference 일관성 |", "| Review ID | Image ID | 기획 일치 | 승인 Visual Reference 일관성 |", "image plan review header")
    replace_once(
        rel,
        "Figma 일관성은 비율·실루엣·palette·line/texture/material·lighting·camera/composition·UI hierarchy·icon/VFX visual grammar를 최소 비교한다. 정본과 Figma가 충돌하면 `VISUAL_CANONICAL_CONFLICT`, Figma를 확인할 수 없으면 `BLOCKED_UNVERIFIED` 또는 정확한 접근 상태로 분리한다.",
        "승인 Visual Reference 일관성은 비율·실루엣·palette·line/texture/material·lighting·camera/composition·UI hierarchy·icon/VFX visual grammar를 최소 비교한다. 정본과 승인 reference가 충돌하면 `VISUAL_CANONICAL_CONFLICT`, reference를 확인할 수 없으면 `BLOCKED_UNVERIFIED` 또는 정확한 접근 상태로 분리한다.",
        "image plan review rule",
    )
    replace_once(
        rel,
        "중요한 AI 생성 화면은 이미지 자체와 별개로 해석 기록을 남긴다. Figma가 쓰기 가능하면 화면 옆 편집 가능한 text/annotation `INTERPRETATION_RECORD`로 동기화하고, 불가능하면 책임 GitHub 기록 또는 프로젝트 Sheet에 남긴 뒤 실제 접근 상태를 유지한다.",
        "중요한 AI 생성 화면은 이미지 자체와 별개로 해석 기록을 남긴다. `INTERPRETATION_RECORD`는 책임 GitHub 기록, 프로젝트 Sheet 또는 repo/project artifact에 남기고 실제 접근 상태를 유지한다. Figma에는 동기화하지 않는다.",
        "image plan interpretation route",
    )
    replace_once(rel, "| Review ID | Screen ID | Flow ID | Figma Interpretation ID |", "| Review ID | Screen ID | Flow ID | Interpretation Record ID |", "image plan interpretation header")
    old_sync = """- [ ] Figma가 구성된 경우 실제 `APPROVED_VISUAL_REFERENCE` frame/node를 확인했거나 정확한 접근 실패 상태를 기록
- [ ] 신규 결과를 먼저 `02_WIP`/review candidate로 두고 사용자 승인 전 `01_APPROVED_REFERENCE`·`04_FINAL` 자동 승격 금지
- [ ] 중요 AI 화면은 필요 시 `INTERPRETATION_RECORD`와 `screen_id / flow_id`를 연결
- [ ] 연결된 화면은 `FLOW_MAP`을 갱신하고 필요한 경우에만 `PROTOTYPE_FLOW` 사용
- [ ] 승인 시 Visual Artifact Registry의 file/page/frame/node·Decision·status·snapshot·interpretation/runtime compare 관계와 Figma 위치를 동기화
- [ ] Figma `04_FINAL`을 `PROJECT_ASSET_APPROVED`·tracked asset·Godot runtime proof로 간주하지 않음
"""
    new_sync = """- [ ] 현재 `APPROVED_VISUAL_REFERENCE`의 ID·경로·source commit을 확인했거나 정확한 `LINK_UNVERIFIED / UNVERIFIED` 상태를 기록
- [ ] 신규 결과를 review candidate로 두고 사용자 승인 전 `APPROVED_VISUAL_REFERENCE`·`PROJECT_ASSET_APPROVED` 자동 승격 금지
- [ ] 중요 AI 화면은 필요 시 `INTERPRETATION_RECORD`와 `screen_id / flow_id`를 연결
- [ ] 연결된 화면은 `FLOW_MAP`을 갱신하고 필요한 경우에만 `PROTOTYPE_FLOW` 사용
- [ ] 승인 시 Visual Artifact Registry의 Decision·status·snapshot·source commit·interpretation/runtime compare 관계를 동기화
- [ ] `LEGACY_FIGMA_REFERENCE`를 현재 승인 reference·tracked asset·Godot runtime proof로 간주하지 않음
"""
    replace_once(rel, old_sync, new_sync, "image plan approval sync")


def patch_preferred_visual_library() -> None:
    rel = "docs/knowledge/game-development/PREFERRED_VISUAL_STYLE_REFERENCE_LIBRARY.md"
    old_header = """> 연결: `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md` → `PIXEL_ART_STYLE_SYSTEM.md` → 이 Library → 프로젝트 Art Bible / Visual Bible Decision
> 지속 탐색: `VISUAL_STYLE_SOURCE_RADAR.md` — 기존 `PERIODIC_SPECIALTY_SOURCE_RADAR.md`의 bounded child reference
> Figma workspace: https://www.figma.com/design/AEYEulNSiobxpCZckun27I
> Figma structure: `FIGMA_STRUCTURE_READY`
> Figma raster sync: `FIGMA_SYNC_PENDING_TRANSPORT`
"""
    new_header = """> 연결: `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md` → `PIXEL_ART_STYLE_SYSTEM.md` → 이 Library → 프로젝트 Art Bible / approved visual reference Decision
> 지속 탐색: `VISUAL_STYLE_SOURCE_RADAR.md` — 기존 `PERIODIC_SPECIALTY_SOURCE_RADAR.md`의 bounded child reference
> `FIGMA_USAGE: DISABLED_BY_USER`
> `LEGACY_FIGMA_REFERENCE`: 과거 Figma workspace/page metadata는 현재 Reference에서 제거했으며 Git 이력으로만 복원한다.
"""
    replace_once(rel, old_header, new_header, "preferred visual library header")
    replace_once(rel, "현재 Art Bible·Figma 승인 Reference·핵심 시스템", "현재 Art Bible·repo/project 승인 visual reference·핵심 시스템", "preferred library reference comparison")
    replace_once(rel, "PC/mobile, Figma 재사용, localization", "PC/mobile, repo/project 재사용, localization", "preferred library long-term fit")
    for idx in range(1, 6):
        replace_once(rel, f"BASE_OVERVIEW_AND_FIGMA_PAGE_0{idx}", "BASE_OVERVIEW_REFERENCE_U01_U13", f"preferred library figma page {idx}")


def patch_regression_tests() -> None:
    rel = "tests/test_resilient_execution_narrative_reference_contract.py"
    replace_once(
        rel,
        '''        for term in (\n            "FIGMA_DEFAULT_VISUAL_WORKSPACE",\n            "REPO_NATIVE_STRUCTURED_DATA",\n            "GOOGLE_SHEETS_LEGACY_MIGRATION_SOURCE",\n            "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json",\n            "docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md",\n        ):\n''',
        '''        for term in (\n            "FIGMA_USAGE: DISABLED_BY_USER",\n            "LEGACY_FIGMA_REFERENCE",\n            "REPO_NATIVE_STRUCTURED_DATA",\n            "GOOGLE_SHEETS_LEGACY_MIGRATION_SOURCE",\n            "docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md",\n            "docs/VISUAL_COLLABORATION_TOOL_POLICY.md",\n            "docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md",\n        ):\n''',
        "resilient documentation map contract",
    )
    replace_once(
        rel,
        '''        self.assertNotIn(\n            "일반 프로젝트의 기획·상태 확인은 GitHub 정본과 구성된 프로젝트 GDD Google Sheets를 우선한다.",\n            docs,\n        )\n''',
        '''        self.assertNotIn("docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json", docs)\n        self.assertNotIn(\n            "일반 프로젝트의 기획·상태 확인은 GitHub 정본과 구성된 프로젝트 GDD Google Sheets를 우선한다.",\n            docs,\n        )\n''',
        "resilient stale workspace path assertion",
    )

    rel = "tests/test_project_gdd_google_sheets_contract.py"
    replace_once(rel, '            "FIGMA_DEFAULT_VISUAL_WORKSPACE",\n            "REPO_NATIVE_STRUCTURED_DATA",', '            "FIGMA_USAGE: DISABLED_BY_USER",\n            "LEGACY_FIGMA_REFERENCE",\n            "REPO_NATIVE_STRUCTURED_DATA",', "sheet contract current visual tokens")
    replace_once(rel, "    def test_visual_policy_uses_figma_first_and_sheet_compatibility_boundary(self) -> None:", "    def test_visual_policy_disables_figma_and_keeps_sheet_compatibility_boundary(self) -> None:", "sheet visual test name")
    replace_once(rel, '            "FIGMA_DEFAULT_VISUAL_WORKSPACE",\n            "REPO_NATIVE_STRUCTURED_DATA",', '            "FIGMA_USAGE: DISABLED_BY_USER",\n            "LEGACY_FIGMA_REFERENCE",\n            "REPO_NATIVE_STRUCTURED_DATA",', "visual policy test current tokens")

    rel = "tests/test_figma_direct_visual_skill_modules.py"
    replace_once(rel, "    def test_existing_art_skill_routes_figma_direct_modules_without_registry_expansion(self) -> None:", "    def test_existing_art_skill_retains_figma_modules_as_inactive_legacy_without_registry_expansion(self) -> None:", "figma module test name")
    replace_once(
        rel,
        '        self.assertIn("references/figma-visual-bible-continuity-gate.md", art_skill)\n        self.assertIn("FIGMA_DIRECT_VISUAL_ORGANIZATION", gate)\n',
        '        self.assertIn("references/figma-visual-bible-continuity-gate.md", art_skill)\n        self.assertIn("FIGMA_USAGE: DISABLED_BY_USER", art_skill)\n        self.assertIn("LEGACY_FIGMA_REFERENCE", art_skill)\n        self.assertIn("Legacy Figma-direct visual modules — inactive", art_skill)\n        self.assertIn("FIGMA_DIRECT_VISUAL_ORGANIZATION", gate)\n',
        "figma module inactive assertions",
    )

    rel = "tests/test_visual_collaboration_capability_contract.py"
    replace_once(rel, "    def test_art_generation_routes_through_figma_continuity_gate(self):", "    def test_art_generation_keeps_figma_continuity_material_legacy_only(self):", "visual collaboration art test name")
    replace_once(
        rel,
        '        self.assertIn("references/figma-visual-bible-continuity-gate.md", skill)\n        self.assertIn("APPROVED_VISUAL_REFERENCE", skill)\n        self.assertIn("Keep / Avoid / Do Not Drift", skill)\n',
        '        self.assertIn("references/figma-visual-bible-continuity-gate.md", skill)\n        self.assertIn("FIGMA_USAGE: DISABLED_BY_USER", skill)\n        self.assertIn("LEGACY_FIGMA_REFERENCE", skill)\n        self.assertIn("APPROVED_VISUAL_REFERENCE", skill)\n        self.assertIn("Keep / Avoid / Do Not Drift", skill)\n',
        "visual collaboration legacy skill assertions",
    )
    old_fields_test = '''        for token in (\n            "figma_visual_bible_status",\n            "figma_approved_reference_ids",\n            "figma_approved_frame_or_node_ids",\n            "figma_wip_target",\n            "figma_sync_status",\n        ):\n            self.assertIn(token, plan)\n\n        self.assertIn("Figma `04_FINAL`", plan)\n        self.assertIn("PROJECT_ASSET_APPROVED", plan)\n'''
    new_fields_test = '''        for token in (\n            "approved_visual_reference_status",\n            "approved_visual_reference_ids",\n            "approved_visual_reference_paths_or_urls",\n            "visual_reference_source_commits",\n            "visual_reference_sync_status",\n        ):\n            self.assertIn(token, plan)\n        self.assertNotIn("figma_visual_bible_status", plan)\n        self.assertIn("FIGMA_USAGE: DISABLED_BY_USER", plan)\n        self.assertIn("LEGACY_FIGMA_REFERENCE", plan)\n        self.assertIn("PROJECT_ASSET_APPROVED", plan)\n'''
    replace_once(rel, old_fields_test, new_fields_test, "visual collaboration image plan assertions")
    replace_once(rel, '            "figma_interpretation_record_id",\n', '            "interpretation_record_id",\n', "visual flow generic interpretation id")


def verify() -> None:
    subprocess.run(
        [
            "python", "-m", "unittest",
            "tests.test_uiux_external_reference_absorption",
            "tests.test_base_long_horizon_work_contract",
            "tests.test_project_gdd_google_sheets_contract",
            "tests.test_resilient_execution_narrative_reference_contract",
            "tests.test_figma_direct_visual_skill_modules",
            "tests.test_visual_collaboration_capability_contract",
            "tests.test_bca_visual_sheet_workflow",
        ],
        cwd=ROOT,
        check=True,
    )
    subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)


def main() -> None:
    patch_documentation_map()
    patch_sheet_policy()
    patch_art_skill()
    patch_image_policy()
    patch_image_plan()
    patch_preferred_visual_library()
    patch_regression_tests()
    verify()

    for rel in (".github/workflows/one-shot-active-figma-owner-retirement.yml", "tools/one_shot_active_figma_owner_retirement.py"):
        path = ROOT / rel
        if path.exists():
            path.unlink()


if __name__ == "__main__":
    main()
