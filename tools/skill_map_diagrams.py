from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

DISCIPLINES = [
    "설정·내러티브", "게임 디자인", "UX·UI·접근성", "개발·엔지니어링",
    "테크니컬 아트·파이프라인", "아트", "사운드", "QA", "프로덕션·PM",
    "분석·유저리서치", "통합검수",
]
STATUS_KO = {"ACTIVE": "현행", "SUPPORT": "보조", "HOLD": "보류", "BACKUP": "백업", "REMOVAL_CANDIDATE": "제거 후보", "NOT_INSTALLED": "미설치"}
LAYER_KO = {"foundation": "기초·공용", "discipline": "분야", "specialist": "전문"}
BG, INK, MUTED, ACCENT = "#F5F7FA", "#1F2937", "#667085", "#315EFB"
ACCENT_LIGHT, WARN, BORDER, WHITE = "#E8EEFF", "#B54708", "#D0D5DD", "#FFFFFF"


def font_path(bold: bool = False) -> str:
    candidates = [
        os.environ.get("BASE_FONT_BOLD" if bold else "BASE_FONT_REGULAR", ""),
        "C:/Windows/Fonts/malgunbd.ttf" if bold else "C:/Windows/Fonts/malgun.ttf",
        "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf" if bold else "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/nanum/NanumBarunGothicBold.ttf" if bold else "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]
    for path in candidates:
        if path and Path(path).exists():
            return path
    raise FileNotFoundError(
        "Set BASE_FONT_REGULAR/BASE_FONT_BOLD or install Malgun Gothic, "
        "fonts-nanum, or fonts-noto-cjk before building the skill map."
    )


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(font_path(bold), size=size)


def wrap(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.ImageFont, width: int) -> list[str]:
    words = text.split()
    if not words:
        return [""]
    lines, current = [], words[0]
    for word in words[1:]:
        probe = f"{current} {word}"
        if draw.textbbox((0, 0), probe, font=f)[2] <= width:
            current = probe
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def box(draw: ImageDraw.ImageDraw, xy, fill=WHITE, outline=BORDER, radius=20, width=2) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def centered(draw: ImageDraw.ImageDraw, xy, text: str, f: ImageFont.ImageFont, fill=INK) -> None:
    x1, y1, x2, y2 = xy
    lines = wrap(draw, text, f, x2 - x1 - 24)
    heights = [draw.textbbox((0, 0), line, font=f)[3] for line in lines]
    total = sum(heights) + 6 * (len(lines) - 1)
    y = y1 + (y2 - y1 - total) / 2
    for line, height in zip(lines, heights):
        width = draw.textbbox((0, 0), line, font=f)[2]
        draw.text((x1 + (x2 - x1 - width) / 2, y), line, font=f, fill=fill)
        y += height + 6


def arrow(draw: ImageDraw.ImageDraw, start, end) -> None:
    draw.line([start, end], fill=ACCENT, width=5)
    x, y = end
    draw.polygon([(x, y), (x - 15, y - 8), (x - 15, y + 8)], fill=ACCENT)


def flow_diagram(out: Path) -> None:
    image = Image.new("RGB", (1800, 650), BG)
    draw = ImageDraw.Draw(image)
    draw.text((70, 40), "프로젝트 스킬 선택·실행·학습 흐름", font=font(48, True), fill=INK)
    draw.text((70, 102), "AI는 전체 스킬을 읽지 않고 Registry의 trigger가 일치하는 최소 집합만 호출합니다.", font=font(24), fill=MUTED)
    labels = ["사용자 요청", "분야·영향도 판정", "Skill Registry", "Foundation 최소 호출", "주 책임 분야 스킬", "검증·완료", "Learning Log"]
    boxes, x, y, bw, bh, gap = [], 70, 230, 205, 145, 40
    for i, label in enumerate(labels):
        current = (x + i * (bw + gap), y, x + i * (bw + gap) + bw, y + bh)
        boxes.append(current)
        active = i in (2, 6)
        box(draw, current, ACCENT_LIGHT if active else WHITE, ACCENT if active else BORDER)
        centered(draw, current, label, font(30, True), ACCENT if active else INK)
        if i:
            previous = boxes[i - 1]
            arrow(draw, (previous[2] + 7, (previous[1] + previous[3]) // 2), (current[0] - 7, (current[1] + current[3]) // 2))
    note = (340, 445, 1460, 575)
    box(draw, note)
    centered(draw, note, "후속 스킬은 해당 단계에서만 호출: PDF 발행은 원본 변경 후, Handoff는 작업 경계에서, Health Review는 설치·대규모 변경·게이트 전환 때만 실행", font(24), MUTED)
    image.save(out, quality=95)


def discipline_diagram(registry: dict[str, Any], out: Path) -> None:
    image = Image.new("RGB", (1800, 1050), BG)
    draw = ImageDraw.Draw(image)
    draw.text((70, 40), "분야별 진입 스킬 라우팅", font=font(48, True), fill=INK)
    draw.text((70, 102), "각 분야는 독립 진입 스킬 또는 명시적인 통합 책임을 가집니다.", font=font(22), fill=MUTED)
    entries = registry.get("discipline_entrypoints", {})
    x0, y0, bw, bh, gx, gy = 70, 180, 500, 165, 55, 45
    for index, discipline in enumerate(DISCIPLINES):
        row, col = divmod(index, 3)
        x, y = x0 + col * (bw + gx), y0 + row * (bh + gy)
        current = (x, y, x + bw, y + bh)
        skill_ids = entries.get(discipline, []) or []
        active = bool(skill_ids)
        box(draw, current, ACCENT_LIGHT if active else WHITE, ACCENT if active else BORDER)
        draw.text((x + 24, y + 22), discipline, font=font(28, True), fill=ACCENT if active else INK)
        if active:
            text = ", ".join(skill_ids[:2]) + (f" 외 {len(skill_ids) - 2}개" if len(skill_ids) > 2 else "")
            for line_no, line in enumerate(wrap(draw, text, font(22), bw - 48)[:3]):
                draw.text((x + 24, y + 70 + line_no * 30), line, font=font(22), fill=MUTED)
        else:
            draw.text((x + 24, y + 78), "[설치 필요] 진입 스킬 미등록", font=font(22), fill=WARN)
    image.save(out, quality=95)


def matrix_diagram(registry: dict[str, Any], out: Path) -> None:
    skills = registry.get("skills", [])
    rows = skills or [{"skill_id": "[스킬 등록 필요]", "layer": "-", "discipline": "-", "status": "NOT_INSTALLED", "use_when": ["SKILL_REGISTRY.json에 현행 스킬을 등록하세요."]}]
    image = Image.new("RGB", (1800, max(520, 230 + max(len(rows), 3) * 90)), BG)
    draw = ImageDraw.Draw(image)
    draw.text((70, 40), "현행 스킬 상태 매트릭스", font=font(48, True), fill=INK)
    draw.text((70, 102), "Registry의 상태·계층·호출 조건·학습 경로를 사람용 표로 시각화합니다.", font=font(23), fill=MUTED)
    columns = [(70, 520, "스킬"), (520, 730, "계층"), (730, 1010, "분야"), (1010, 1210, "상태"), (1210, 1730, "호출 조건 요약")]
    y = 175
    for x1, x2, label in columns:
        draw.rectangle((x1, y, x2, y + 55), fill=ACCENT)
        draw.text((x1 + 14, y + 13), label, font=font(25, True), fill=WHITE)
    for index, item in enumerate(rows):
        yy = y + 55 + index * 90
        draw.rectangle((70, yy, 1730, yy + 90), fill=WHITE if index % 2 == 0 else "#F0F3F8", outline=BORDER)
        values = [
            str(item.get("skill_id", "")), LAYER_KO.get(str(item.get("layer", "")), str(item.get("layer", ""))),
            str(item.get("discipline", "")), STATUS_KO.get(str(item.get("status", "")), str(item.get("status", ""))),
            " / ".join(item.get("use_when", [])[:1]) or "-",
        ]
        for (x1, x2, _), value in zip(columns, values):
            for line_no, line in enumerate(wrap(draw, value, font(23), x2 - x1 - 24)[:2]):
                draw.text((x1 + 12, yy + 15 + line_no * 28), line, font=font(23), fill=INK)
    image.save(out, quality=95)
