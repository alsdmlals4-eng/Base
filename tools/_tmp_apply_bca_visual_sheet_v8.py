from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V7 = "templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md"
V8 = "templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md"

OLD_ORDER = """00 프로젝트 기반·현재 상태
→ 10 제품 방향·시장 약속
→ 20 코어 경험·메인게임·데모 목표
→ 30 데모 범위·품질 기준·제작 기반
→ 40 시스템·성장·경제
→ 50 메인 콘텐츠
→ 51 미니게임(해당 프로젝트만)
→ 52 글쓰기·서사(해당 프로젝트만)
→ 60 UX·UI·접근성
→ 70 아트·오디오·에셋
→ 80 완성 품질 Vertical Slice 데모·플레이테스트
→ 90 본제작·출시·사업
→ 98 Base 반영 후보
→ 99 변경 이력·회고"""
NEW_ORDER = """00 프로젝트 기반·현재 상태
→ 10 제품 방향·시장 약속
→ 11 세계관
→ 12 핵심루프
→ 13 주요인물
→ 14 조연·세력·관계
→ 20 코어 경험·메인게임·데모 목표
→ 30 데모 범위·품질 기준·제작 기반
→ 40 핵심시스템·메인콘텐츠
→ 41 성장·경제
→ 50 메인 콘텐츠
→ 51 미니게임(해당 프로젝트만)
→ 52 글쓰기·서사(해당 프로젝트만)
→ 60 UX·UI·접근성
→ 70 아트·오디오·에셋
→ 71 기획 이미지·목업 생성
→ 72 이미지 검수·승인
→ 80 완성 품질 Vertical Slice 데모·플레이테스트
→ 90 본제작·출시·사업
→ 98 Base 반영 후보
→ 99 변경 이력·회고"""
OLD_TABS = """00_프로젝트_허브
01_작업순서
02_현재_확정결정
03_근거_라이브러리
04_누락_충돌_감사
10_제품방향
20_코어경험_데모목표
30_데모범위_품질기준_제작기반
40_시스템_성장_경제
50_메인콘텐츠
51_미니게임
52_글쓰기_서사
60_UX_UI_접근성
70_아트_오디오_에셋
80_데모_버티컬슬라이스_플레이테스트
90_본제작_출시_사업
98_Base_반영후보
99_변경이력"""
NEW_TABS = """00_프로젝트_허브
01_작업순서
02_현재_확정결정
03_근거_라이브러리
04_누락_충돌_감사
10_제품방향
11_세계관
12_핵심루프
13_주요인물
14_조연_세력_관계
20_코어경험_데모목표
30_데모범위_품질기준_제작기반
40_핵심시스템_메인콘텐츠
41_성장_경제
50_메인콘텐츠
51_미니게임
52_글쓰기_서사
60_UX_UI_접근성
70_아트_오디오_에셋
71_이미지기획_생성목록
72_이미지검수_승인로그
80_데모_버티컬슬라이스_플레이테스트
90_본제작_출시_사업
98_Base_반영후보
99_변경이력"""


def replace_if_present(text: str, old: str, new: str) -> str:
    return text.replace(old, new, 1) if old in text else text


def update_text(path: str, transform) -> None:
    file = ROOT / path
    text = file.read_text(encoding="utf-8")
    file.write_text(transform(text), encoding="utf-8")


def build_v8() -> None:
    source = (ROOT / V7).read_text(encoding="utf-8")
    clean_source = source
    if "status: SUPERSEDED_COMPATIBILITY" in clean_source:
        clean_source = clean_source.replace(
            'contract_version: "7.0"\nactive_authority: false\nstatus: SUPERSEDED_COMPATIBILITY\nreplacement_execution_prompt: templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md',
            'contract_version: "7.0"',
            1,
        )
        clean_source = clean_source.replace(
            "# 버티컬 슬라이스 중심 게임 기획·제작·검수 통합 실행 계약 — v7 호환본",
            "# 버티컬 슬라이스 중심 게임 기획·제작·검수 통합 실행 계약",
            1,
        )
        clean_source = clean_source.replace(
            "이 파일은 v8 이전의 호환 기록이다. 새 작업은 `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md`를 사용한다. v7의 본문은 마이그레이션 비교와 과거 프로젝트 호환을 위해 보존한다.",
            "이 파일은 **상세 정본과 실행 지시를 합친 단일 첨부용 통합 실행문**이다.",
            1,
        )
    v8 = clean_source.replace('contract_version: "7.0"', 'contract_version: "8.0"', 1)
    v8 = v8.replace(
        "  - LEGACY_REQUIREMENT_TRACEABILITY\n",
        "  - LEGACY_REQUIREMENT_TRACEABILITY\n  - PROJECT_SHEET_SEMANTIC_TABS\n  - GPT_PLANNING_VISUALIZATION\n  - GPT_FINAL_VISUAL_CANDIDATE_REVIEW\n  - VISUAL_ASSET_APPROVAL_LEDGER\n",
        1,
    )
    v8 = v8.replace(
        "# 버티컬 슬라이스 중심 게임 기획·제작·검수 통합 실행 계약",
        "# 버티컬 슬라이스 중심 게임 기획·제작·검수 통합 실행 계약 v8",
        1,
    )
    v8 = replace_if_present(v8, OLD_ORDER, NEW_ORDER)
    v8 = replace_if_present(v8, OLD_TABS, NEW_TABS)
    visual_section = """# 10A. BCA 기획 산출물 운영 순서

이 계약은 다음 순서를 사용한다.

```text
B. 프로젝트 Google Sheets 의미 구조 설치·갱신
→ C. 기획 중·기획 종료 GPT 이미지·목업 생성과 검수
→ A. 승인 결과를 Base 공용 정책·Skill·정본·소비처에 반영
```

B 단계에서 세계관·핵심루프·주요인물·조연·세력·관계·핵심시스템·메인콘텐츠의 책임 원본과 Sheet tab을 연결한다. 정확한 Sheet URL이 없으면 `NOT_CONFIGURED`로 두고 중복 Sheet를 만들지 않는다.

C 단계의 이미지 상태는 다음을 사용한다.

```text
PLANNED
→ GENERATED_EXPLORATION
→ IN_REVIEW
├─ REVISION_REQUIRED
├─ REJECTED
└─ APPROVED_CANDIDATE
   → PROJECT_ASSET_APPROVED
   → APPLIED_AND_RUNTIME_VERIFIED
```

기획 중 이미지는 방향 비교·모순 발견·실제 화면 가설 검증용이다. 기획 종료 이미지는 Demo-First Vertical Slice·상점·홍보·UI·캐릭터·시스템 설명에 사용할 후보지만, 검수 전에는 최종 자산이 아니다.

필수 기록:

- Image ID, 목적, 관련 Decision·정본, 단계와 사용처
- 프롬프트, 모델·서비스·버전, 생성일, 입력 이미지
- 레퍼런스·원작자·원출처·라이선스·유사성 검토
- 실제 화면비·해상도·크롭·HUD·VFX 위 가독성
- 구현 난이도·제작 비용·재사용·편집·현지화 가능성
- 검수 Finding·수정 이력·승인자·승인 상태
- GitHub 경로·Sheet row·Asset Ledger·실제 적용 경로

"""
    if "# 10A. BCA 기획 산출물 운영 순서" not in v8:
        v8 = v8.replace("# 11. UI·UX·이미지·사운드·에셋 조달", visual_section + "# 11. UI·UX·이미지·사운드·에셋 조달", 1)
    mode_section = """## 11.0 GPT 기획 시각화와 최종 후보 생성

`designing-art-prompts-and-technique-cards`의 `planning-visualization`, `final-visual-candidate`, `visual-qa-and-approval` mode를 사용한다.

- 기획 중: 세계관·장소·인물·핵심루프·핵심시스템·UI·대표 장면의 탐색 이미지와 목업을 생성한다.
- 기획 종료: 승인된 기획을 바탕으로 키아트·캐릭터 시트·UI 고도화 목업·시스템 소개·상점·홍보 후보를 만든다.
- 생성 결과는 `APPROVED_CANDIDATE`까지이며, 권리·규격·후처리·실제 화면·런타임 검증 뒤에만 `PROJECT_ASSET_APPROVED`로 승격한다.
- 사용자가 이미지 생성 권한을 명시했거나 현재 계약에 포함된 경우 GPT가 생성한다. 생성 도구가 없으면 생성 완료를 주장하지 않고 브리프·프롬프트·검수 계약만 남긴다.
- 이미지가 기존 정본을 바꾸는 경우 이미지가 아니라 사용자 Decision이 권한을 가진다.

"""
    if "## 11.0 GPT 기획 시각화와 최종 후보 생성" not in v8:
        v8 = v8.replace("## 11.1 생성 순서\n", mode_section + "## 11.1 생성 순서\n", 1)
    v8 = v8.replace(
        "이 파일은 사용자가 제공한 `VERTICAL_SLICE_MASTER_REFERENCE_v6`의 상세 설계·시스템·UX·에셋·출시·검증·인계·완전성 내용을 보존하고, 당시의 별도 축약 실행문 책임을 통합했다.",
        "이 파일은 v7의 상세 계약과 사용자가 제공한 `VERTICAL_SLICE_MASTER_REFERENCE_v6`의 설계·시스템·UX·에셋·출시·검증·인계·완전성 내용을 무손실 승계하고, BCA 프로젝트 Sheet·GPT 이미지 생성·검수·승인 책임을 추가했다.",
        1,
    )
    if "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md" not in v8:
        v8 = v8.replace(
            "- `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md`",
            "- `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`\n- `templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md`\n- `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`\n- `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md`",
            1,
        )
    (ROOT / V8).write_text(v8, encoding="utf-8")

    legacy = clean_source.replace(
        'contract_version: "7.0"',
        'contract_version: "7.0"\nactive_authority: false\nstatus: SUPERSEDED_COMPATIBILITY\nreplacement_execution_prompt: templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md',
        1,
    )
    legacy = legacy.replace(
        "# 버티컬 슬라이스 중심 게임 기획·제작·검수 통합 실행 계약",
        "# 버티컬 슬라이스 중심 게임 기획·제작·검수 통합 실행 계약 — v7 호환본",
        1,
    )
    legacy = legacy.replace(
        "이 파일은 **상세 정본과 실행 지시를 합친 단일 첨부용 통합 실행문**이다.",
        "이 파일은 v8 이전의 호환 기록이다. 새 작업은 `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md`를 사용한다. v7의 본문은 마이그레이션 비교와 과거 프로젝트 호환을 위해 보존한다.",
        1,
    )
    (ROOT / V7).write_text(legacy, encoding="utf-8")


def update_policy() -> None:
    def transform(text: str) -> str:
        if "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md" not in text:
            text = text.replace(
                "데모 제작 Gate는 `docs/knowledge/vertical-slice/INTEGRATED_DEMO_STAGE_GATES.md`가 책임진다.",
                "데모 제작 Gate는 `docs/knowledge/vertical-slice/INTEGRATED_DEMO_STAGE_GATES.md`, 프로젝트 Sheet와 GPT 이미지 생성·검수는 `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`가 책임진다.",
                1,
            )
        text = replace_if_present(text, OLD_ORDER, NEW_ORDER)
        text = replace_if_present(text, OLD_TABS, NEW_TABS)
        return text
    update_text("docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md", transform)


def update_registry() -> None:
    path = ROOT / "skills/SKILL_REGISTRY.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    by_id = {item["skill_id"]: item for item in data["skills"]}
    art = by_id["designing-art-prompts-and-technique-cards"]
    for tag in ("planning-visualization", "final-visual-candidate", "visual-qa-and-approval", "image-mockup", "image-approval", "image-review-ledger"):
        if tag not in art["trigger_tags"]:
            art["trigger_tags"].append(tag)
    art["use_when"] = ["기획 중 세계관·인물·핵심루프·시스템·UI를 GPT 이미지·목업으로 시각화하거나, 기획 종료 후 Demo-First·상점·홍보용 후보를 생성하고 실제 화면·구현·권리·승인 상태를 검수한다."]
    for trigger in ("생성 이미지를 자동 최종 자산으로 사용함", "기획 변경 뒤 stale 이미지 유지", "이미지 승인 로그·Sheet·Asset Ledger 전파 누락", "원출처·라이선스·유사성 검토 누락"):
        if trigger not in art["review_triggers"]:
            art["review_triggers"].append(trigger)
    for skill_id, tags in {
        "managing-project-intake-and-work-contract": ("project-sheet-semantic-tabs", "image-approval-bundle"),
        "managing-game-project-operating-system": ("project-sheet-workbook", "visual-workflow-install"),
        "managing-design-documents": ("image-approval-ledger", "visual-canonical-sync"),
    }.items():
        entry = by_id[skill_id]
        for tag in tags:
            if tag not in entry["trigger_tags"]:
                entry["trigger_tags"].append(tag)
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def update_reference_freshness() -> None:
    path = ROOT / ".github/reference-freshness.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for entry in data.get("canonical_references", []):
        if entry.get("name") == "integrated-vertical-slice-prompt-entrypoints":
            entry["canonical_path"] = V8
            entry["reference_tokens"] = [V8, "VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md"]
    rules = data.setdefault("coupled_change_rules", [])
    for rule in rules:
        if rule.get("name") == "integrated-prompt-contract-test-sync":
            rule["when_changed"] = [V8]
            rule["require_any_changed"] = ["tests/test_bca_visual_sheet_workflow.py"]
    if not any(rule.get("name") == "bca-visual-sheet-policy-sync" for rule in rules):
        rules.append({
            "name": "bca-visual-sheet-policy-sync",
            "when_changed": ["docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md", "templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md"],
            "exclude_when_changed": [],
            "require_all_changed": [],
            "require_any_changed": ["tests/test_bca_visual_sheet_workflow.py"],
        })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_consumers() -> None:
    for path in ("START_HERE.md", "docs/DOCUMENTATION_MAP.md", "templates/project-operations/README.md", "docs/knowledge/VERTICAL_SLICE_V6_REQUIREMENT_COVERAGE.md"):
        update_text(path, lambda text: text.replace("VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md", "VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md"))

    def template_readme(text: str) -> str:
        addition = "\n- `PROJECT_GOOGLE_SHEET_WORKBOOK_CONTRACT.md`: 세계관·핵심루프·인물·핵심시스템·이미지 검수 tab 설치 계약.\n- `../planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`: 기획 중·기획 종료 GPT 이미지 생성과 승인 기록 Template.\n"
        return text if "PROJECT_GOOGLE_SHEET_WORKBOOK_CONTRACT.md" in text else text.rstrip() + "\n" + addition
    update_text("templates/project-operations/README.md", template_readme)

    def doc_map(text: str) -> str:
        if "GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md" not in text:
            anchor = "| 기획 작업순서·근거·데모 우선 | `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md`"
            line = "| GPT 이미지 생성·검수·Sheet 구조 | `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md` | 기획 중 시각화, 기획 종료 후보, 이미지 QA·승인 원장, 의미 구조 Sheet tab |\n"
            idx = text.find(anchor)
            if idx >= 0:
                end = text.find("\n", idx)
                text = text[: end + 1] + line + text[end + 1 :]
            else:
                text = text.rstrip() + "\n\n" + line
        return text
    update_text("docs/DOCUMENTATION_MAP.md", doc_map)

    def art_matrix(text: str) -> str:
        addition = "\n## 10. GPT 기획 시각화·최종 후보·승인 Mode\n\n- `planning-visualization`: 세계관·핵심루프·인물·시스템·UI 탐색 이미지와 목업.\n- `final-visual-candidate`: Demo-First·상점·홍보·키아트·UI 고도화 후보.\n- `visual-qa-and-approval`: 실제 화면·구현·권리·오류·재사용성과 승인 원장 검수.\n- 공용 정책: `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`.\n"
        return text if "GPT 기획 시각화·최종 후보·승인 Mode" in text else text.rstrip() + addition + "\n"
    update_text("docs/knowledge/skills/ART_DIRECTION_SKILL_MATRIX.md", art_matrix)

    def art_brief(text: str) -> str:
        addition = "\n## GPT 이미지 생성·검수 연결\n\n- 이미지 단계: `PLANNING_VISUALIZATION / FINAL_VISUAL_CANDIDATE`\n- 기록 Template: `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`\n- 승인 전 생성 결과는 최종 자산이 아니다.\n"
        return text if "GPT 이미지 생성·검수 연결" in text else text.rstrip() + addition + "\n"
    update_text("templates/planning/ART_DIRECTION_BRIEF.md", art_brief)


def update_logs() -> None:
    learning = ROOT / "skills/SKILL_LEARNING_LOG.md"
    text = learning.read_text(encoding="utf-8")
    entry = "\n## 2026-07-28 — BCA Sheet·GPT 이미지 생성·검수 통합\n\n- `designing-art-prompts-and-technique-cards`에 `planning-visualization`, `final-visual-candidate`, `visual-qa-and-approval` mode를 통합했다.\n- 프로젝트 Sheet 의미 구조에 세계관·핵심루프·주요인물·조연·핵심시스템·이미지 계획·검수 tab을 추가했다.\n- 정확한 Sheet URL이 없으면 `NOT_CONFIGURED`로 유지하며 중복 생성을 금지한다.\n- v7은 호환본, v8은 활성 통합 실행문으로 전환한다.\n"
    if "BCA Sheet·GPT 이미지 생성·검수 통합" not in text:
        learning.write_text(text.rstrip() + entry + "\n", encoding="utf-8")
    changelog = ROOT / "docs/CHANGELOG.md"
    text = changelog.read_text(encoding="utf-8")
    entry = "- 2026-07-28: BCA 프로젝트 Sheet 의미 구조, GPT 기획 시각화·최종 후보 이미지 검수, 통합 실행문 v8을 추가하고 v7을 호환본으로 전환.\n"
    if "통합 실행문 v8" not in text:
        changelog.write_text(text.rstrip() + "\n" + entry, encoding="utf-8")


def main() -> None:
    build_v8()
    update_policy()
    update_registry()
    update_reference_freshness()
    update_consumers()
    update_logs()


if __name__ == "__main__":
    main()
