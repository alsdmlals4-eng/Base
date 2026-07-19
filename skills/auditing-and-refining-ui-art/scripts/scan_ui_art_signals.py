#!/usr/bin/env python3
"""Report static UI-art risk candidates without modifying source files."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


IGNORED_DIRS = {".git", ".godot", "node_modules", "dist", "build", "coverage"}
WEB_EXTENSIONS = {".html", ".css", ".scss", ".sass", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro"}
GODOT_EXTENSIONS = {".tscn", ".tres", ".theme", ".gd"}
ALLOW_RE = re.compile(r"base-ui-audit:\s*allow\s+([GW]-[A-E]-[A-Z0-9-]+)\s+reason=(.+?)\s*$", re.IGNORECASE)


@dataclass(frozen=True)
class Rule:
    rule_id: str
    adapter: str
    area: str
    severity: str
    confidence: str
    pattern: re.Pattern[str]
    risk: str
    proposal: str
    verification: str


def _rule(rule_id: str, adapter: str, area: str, severity: str, confidence: str, pattern: str,
          risk: str, proposal: str, verification: str) -> Rule:
    return Rule(rule_id, adapter, area, severity, confidence, re.compile(pattern, re.IGNORECASE), risk, proposal, verification)


RULES = (
    _rule("W-A-DECORATIVE-EFFECT", "web", "A", "MEDIUM", "MEDIUM",
          r"backdrop-filter\s*:|background(?:-image)?\s*:\s*(?:linear|radial)-gradient|background-clip\s*:\s*text|box-shadow\s*:",
          "반복 장식이 정보 계층이나 상호작용 상태와 경쟁할 수 있다.",
          "아트 방향과 실행 화면에서 효과의 목적을 확인하고 승인된 경우에만 강도·범위·사용 횟수를 조정한다.",
          "승인된 화면에서 효과가 지정된 강조 대상에만 쓰이고 정보 판독을 방해하지 않는지 렌더로 확인한다."),
    _rule("W-B-FIXED-LAYOUT", "web", "B", "MEDIUM", "LOW",
          r"position\s*:\s*absolute|(?:width|max-width|min-width|height)\s*:\s*\d{3,4}px",
          "고정 크기나 절대 위치가 콘텐츠·번역·viewport 변화에서 구조를 깨뜨릴 수 있다.",
          "해당 고정값의 연출 목적을 확인하고 필요하면 flow, flex, grid 또는 유연한 제약으로 바꾼다.",
          "대표 viewport와 긴 콘텐츠에서 겹침·잘림·가로 스크롤이 없는지 확인한다."),
    _rule("W-C-IRREGULAR-SPACING", "web", "C", "MEDIUM", "MEDIUM",
          r"(?:gap|padding(?:-[a-z]+)?|margin(?:-[a-z]+)?)\s*:[^;]*(?:7|13|17|23|29)px",
          "간격 값이 반복 가능한 리듬보다 임시 미세조정에 의존할 수 있다.",
          "주변 관계와 간격 체계를 대조해 의도 없는 예외만 승인 후 토큰이나 공통 단계로 정렬한다.",
          "수정된 간격이 인접 요소의 관계를 명확히 하고 두 viewport에서 같은 리듬을 유지하는지 확인한다."),
    _rule("W-D-TYPE-EFFECT", "web", "D", "MEDIUM", "HIGH",
          r"font-style\s*:\s*italic|letter-spacing\s*:\s*(?:0\.[2-9]|[2-9])(?:em|rem)|font-size\s*:\s*(?:[0-9]|1[01])px",
          "작은 글자나 과도한 장식이 정보 계층과 가독성을 약화할 수 있다.",
          "텍스트 역할과 사용 언어를 확인하고 승인된 타입 스케일·굵기·행간으로 조정한다.",
          "한글·영문·숫자를 실제 폰트로 렌더해 계층과 판독성을 확인한다."),
    _rule("W-E-COLOR-LITERAL", "web", "E", "LOW", "LOW",
          r"(?:^\s*|[;{]\s*)(?:color|background(?:-color)?|border-color)\s*:\s*(?:#[0-9a-f]{3,8}|rgba?\()",
          "직접 색상 값이 상태 체계와 대비 규칙에서 벗어날 수 있다.",
          "실제 전경·배경과 상태 역할을 확인하고 필요한 경우에만 승인된 토큰으로 연결한다.",
          "실제 조합의 대비와 normal·hover·focus·disabled 상태 구분을 확인한다."),
    _rule("G-A-SURFACE-EFFECT", "godot", "A", "MEDIUM", "MEDIUM",
          r"(?:shadow_size|shadow_offset_[xy]|corner_radius_(?:top_left|top_right|bottom_left|bottom_right))\s*=\s*[1-9]|bg_color\s*=\s*Color\([^)]*,\s*0\.[0-9]+\)",
          "StyleBox 장식이 계층이나 상태와 무관하게 반복될 수 있다.",
          "Theme 상속과 아트 방향을 확인해 목적 없는 효과만 승인 후 축소하거나 통합한다.",
          "실행 화면에서 효과가 계층과 상태를 명확히 하며 텍스트를 방해하지 않는지 확인한다."),
    _rule("G-B-MANUAL-LAYOUT", "godot", "B", "MEDIUM", "LOW",
          r"(?:offset_left|offset_top|offset_right|offset_bottom)\s*=\s*-?\d+(?:\.\d+)?",
          "수동 offset이 Container 계산이나 다양한 해상도에서 깨질 수 있다.",
          "노드의 부모 Container와 anchor 의도를 확인하고 필요한 경우 size flags와 컨테이너 구조로 바꾼다.",
          "프로젝트 stretch 설정의 대표 해상도에서 겹침·잘림 없이 배치되는지 확인한다."),
    _rule("G-C-IRREGULAR-SPACING", "godot", "C", "MEDIUM", "MEDIUM",
          r"(?:separation|content_margin_(?:left|top|right|bottom)|theme_override_constants/[a-z0-9_]+)\s*=\s*(?:7|13|17|23|29)(?:\.0)?",
          "간격 override가 공통 Theme 리듬과 다른 임시 조정일 수 있다.",
          "주변 관계와 Theme 상수를 대조해 의도 없는 예외만 승인 후 공통 간격으로 정렬한다.",
          "긴 텍스트와 대표 해상도에서 그룹 관계와 밀도가 일관적인지 확인한다."),
    _rule("G-D-TYPE-EFFECT", "godot", "D", "MEDIUM", "HIGH",
          r"(?:font_size|theme_override_font_sizes/[a-z0-9_]+)\s*=\s*(?:[0-9]|1[01])(?:\.0)?",
          "작은 텍스트가 실제 폰트와 스케일에서 읽히지 않을 수 있다.",
          "텍스트 역할과 프로젝트 타입 스케일을 확인하고 승인된 최소 크기와 계층으로 조정한다.",
          "Godot 실행 화면에서 한글·영문·숫자의 판독성과 계층을 확인한다."),
    _rule("G-E-COLOR-LITERAL", "godot", "E", "LOW", "LOW",
          r"(?:font_color|bg_color|border_color|theme_override_colors/[a-z0-9_]+)\s*=\s*Color\(|add_theme_color_override\([^,]+,\s*Color\(",
          "직접 색상 override가 Theme 상속과 상태 대비를 우회할 수 있다.",
          "색상의 역할과 상속 경로를 확인하고 필요한 경우에만 승인된 Theme 색상으로 통합한다.",
          "normal·hover·pressed·disabled·focus 상태와 실제 전경·배경 대비를 확인한다."),
)


def _iter_files(root: Path) -> Iterable[Path]:
    if root.is_file():
        yield root
        return
    for path in sorted(root.rglob("*")):
        if path.is_file() and not any(part in IGNORED_DIRS for part in path.parts):
            yield path


def _adapter_for(path: Path) -> str | None:
    suffix = path.suffix.lower()
    if suffix in WEB_EXTENSIONS:
        return "web"
    if suffix in GODOT_EXTENSIONS:
        return "godot"
    return None


def _relative(path: Path, root: Path) -> str:
    if root.is_file():
        return path.name
    return path.relative_to(root).as_posix()


def _finding_id(rule: Rule, relative_path: str, line: int) -> str:
    digest = hashlib.sha1(f"{rule.rule_id}:{relative_path}:{line}".encode("utf-8")).hexdigest()[:10]
    return f"{rule.adapter}-{rule.area.lower()}-{rule.rule_id.lower()}-{digest}"


def scan(root: Path, adapter: str = "auto") -> dict:
    root = root.resolve()
    if not root.exists():
        raise FileNotFoundError(f"scan root does not exist: {root}")
    requested = {"godot", "web"} if adapter in {"auto", "both"} else {adapter}
    findings: list[dict] = []
    suppressions: list[dict] = []
    scanned_files = 0
    seen_adapters: set[str] = set()

    for path in _iter_files(root):
        file_adapter = _adapter_for(path)
        if file_adapter not in requested:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        scanned_files += 1
        seen_adapters.add(file_adapter)
        relative_path = _relative(path, root)
        allow: dict[str, tuple[int, str]] = {}
        for line_number, line in enumerate(text.splitlines(), 1):
            match = ALLOW_RE.search(line)
            if match:
                allow[match.group(1).upper()] = (line_number, match.group(2).strip())

        for rule in RULES:
            if rule.adapter != file_adapter:
                continue
            if rule.rule_id in allow:
                line_number, reason = allow[rule.rule_id]
                suppressions.append({
                    "adapter": file_adapter,
                    "file": relative_path,
                    "line": line_number,
                    "rule_id": rule.rule_id,
                    "reason": reason,
                })
                continue
            for line_number, line in enumerate(text.splitlines(), 1):
                if not rule.pattern.search(line):
                    continue
                evidence = " ".join(line.strip().split())[:240]
                findings.append({
                    "finding_id": _finding_id(rule, relative_path, line_number),
                    "area": rule.area,
                    "adapter": rule.adapter,
                    "severity": rule.severity,
                    "confidence": rule.confidence,
                    "file": relative_path,
                    "line": line_number,
                    "observed_evidence": evidence,
                    "design_risk": rule.risk,
                    "proposed_change": rule.proposal,
                    "verification_predicate": rule.verification,
                    "status": "CANDIDATE",
                })

    findings.sort(key=lambda item: (item["adapter"], item["area"], item["file"], item["line"], item["finding_id"]))
    suppressions.sort(key=lambda item: (item["adapter"], item["file"], item["line"], item["rule_id"]))
    return {
        "schema_version": 1,
        "scanned_root": root.name,
        "adapters": sorted(seen_adapters),
        "scanned_files": scanned_files,
        "suppressions": suppressions,
        "findings": findings,
    }


def render_markdown(report: dict) -> str:
    lines = [
        "# UI 아트 정적 감사 후보",
        "",
        "> 이 보고서는 정적 패턴 후보이며 결함 확정이나 자동 수정 지시가 아닙니다.",
        "",
        f"- 검사 루트: `{report['scanned_root']}`",
        f"- 어댑터: {', '.join(report['adapters']) or '없음'}",
        f"- 검사 파일: {report['scanned_files']}",
        f"- 후보: {len(report['findings'])}",
        f"- 사유 있는 제외: {len(report['suppressions'])}",
        "",
        "## Findings",
        "",
    ]
    if not report["findings"]:
        lines.append("후보가 없습니다.")
    for item in report["findings"]:
        lines.extend([
            f"### {item['finding_id']}",
            "",
            f"- 영역/어댑터: {item['area']} / {item['adapter']}",
            f"- 심각도/신뢰도: {item['severity']} / {item['confidence']}",
            f"- 위치: `{item['file']}:{item['line']}`",
            f"- 관찰: `{item['observed_evidence']}`",
            f"- 위험: {item['design_risk']}",
            f"- 제안: {item['proposed_change']}",
            f"- 검증: {item['verification_predicate']}",
            f"- 상태: {item['status']}",
            "",
        ])
    if report["suppressions"]:
        lines.extend(["## 사유 있는 제외", ""])
        for item in report["suppressions"]:
            lines.append(f"- `{item['file']}:{item['line']}` {item['rule_id']}: {item['reason']}")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--adapter", choices=("auto", "both", "godot", "web"), default="auto")
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-markdown", type=Path)
    args = parser.parse_args()

    report = scan(args.root, args.adapter)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.output_markdown:
        args.output_markdown.parent.mkdir(parents=True, exist_ok=True)
        args.output_markdown.write_text(render_markdown(report), encoding="utf-8")
    print(f"Scanned {report['scanned_files']} files; reported {len(report['findings'])} candidates; preserved {len(report['suppressions'])} justified exclusions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
