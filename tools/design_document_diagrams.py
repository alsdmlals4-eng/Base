from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

BG = "#F5F7FA"
WHITE = "#FFFFFF"
INK = "#1F2937"
MUTED = "#667085"
ACCENT = "#315EFB"
ACCENT_LIGHT = "#E8EEFF"
BORDER = "#D0D5DD"
WARN = "#B54708"
SUCCESS = "#027A48"


def _font_path(bold: bool = False) -> str:
    candidates = [
        os.environ.get("BASE_FONT_BOLD" if bold else "BASE_FONT_REGULAR", ""),
        "C:/Windows/Fonts/malgunbd.ttf" if bold else "C:/Windows/Fonts/malgun.ttf",
        "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf" if bold else "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/nanum/NanumBarunGothicBold.ttf" if bold else "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    raise FileNotFoundError(
        "Set BASE_FONT_REGULAR/BASE_FONT_BOLD or install Malgun Gothic, "
        "fonts-nanum, or fonts-noto-cjk before building design documents."
    )


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(_font_path(bold), size=size)


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, width: int) -> list[str]:
    words = str(text).split()
    if not words:
        return [""]
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        probe = f"{current} {word}"
        if draw.textbbox((0, 0), probe, font=font)[2] <= width:
            current = probe
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def _box(draw: ImageDraw.ImageDraw, xy, *, fill=WHITE, outline=BORDER, radius=18, width=2) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def _centered(draw: ImageDraw.ImageDraw, xy, text: str, font: ImageFont.ImageFont, fill=INK) -> None:
    x1, y1, x2, y2 = xy
    lines = _wrap(draw, text, font, x2 - x1 - 24)
    heights = [draw.textbbox((0, 0), line, font=font)[3] for line in lines]
    total = sum(heights) + max(0, len(lines) - 1) * 5
    y = y1 + (y2 - y1 - total) / 2
    for line, height in zip(lines, heights):
        line_width = draw.textbbox((0, 0), line, font=font)[2]
        draw.text((x1 + (x2 - x1 - line_width) / 2, y), line, font=font, fill=fill)
        y += height + 5


def _arrow(draw: ImageDraw.ImageDraw, start, end) -> None:
    draw.line([start, end], fill=ACCENT, width=5)
    x, y = end
    draw.polygon([(x, y), (x - 14, y - 8), (x - 14, y + 8)], fill=ACCENT)


def build_workflow_diagram(document: dict[str, Any], output: Path) -> None:
    workflow = document.get("workflow", [])
    labels = [str(item.get("step", f"단계 {index + 1}")) for index, item in enumerate(workflow)]
    if not labels:
        labels = ["입력", "판단·기획", "제작·구현", "검증", "문서·상태 갱신", "다음 게이트"]
    width = max(1800, 130 + len(labels) * 245)
    image = Image.new("RGB", (width, 650), BG)
    draw = ImageDraw.Draw(image)
    draw.text((70, 38), "분야 전체 작업 흐름", font=_font(48, True), fill=INK)
    draw.text((70, 100), "입력부터 판단·산출물·검증·다음 게이트까지의 최신 책임 흐름", font=_font(24), fill=MUTED)
    x, y, box_width, box_height, gap = 70, 225, 205, 145, 40
    boxes = []
    for index, label in enumerate(labels):
        current = (x + index * (box_width + gap), y, x + index * (box_width + gap) + box_width, y + box_height)
        boxes.append(current)
        active = index in (0, len(labels) - 1)
        _box(draw, current, fill=ACCENT_LIGHT if active else WHITE, outline=ACCENT if active else BORDER)
        _centered(draw, current, label, _font(27, True), ACCENT if active else INK)
        if index:
            previous = boxes[index - 1]
            _arrow(draw, (previous[2] + 7, (previous[1] + previous[3]) // 2), (current[0] - 7, (current[1] + current[3]) // 2))
    note = (250, 455, width - 250, 575)
    _box(draw, note)
    _centered(draw, note, "각 단계는 필수 입력, 전문 판단, 산출물, 실제 경로, 실패·폴백, 검증과 다음 게이트를 JSON에서 추적합니다.", _font(24), MUTED)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, quality=95)


def _state_count(document: dict[str, Any], key: str) -> int:
    count = 0
    for item in document.get("current_state", []):
        value = item.get(key)
        if isinstance(value, bool):
            count += int(value)
        elif value not in (None, "", [], {}):
            count += 1
    return count


def build_status_diagram(document: dict[str, Any], output: Path) -> None:
    categories = [
        ("확정", _state_count(document, "confirmed"), ACCENT),
        ("구현·제작", _state_count(document, "implemented"), "#7A5AF8"),
        ("검증", _state_count(document, "validated"), SUCCESS),
        ("확인 필요", _state_count(document, "unresolved"), WARN),
        ("보류", _state_count(document, "hold"), "#475467"),
    ]
    image = Image.new("RGB", (1800, 650), BG)
    draw = ImageDraw.Draw(image)
    draw.text((70, 38), "현재 상태 분리", font=_font(48, True), fill=INK)
    draw.text((70, 100), "확정·구현·검증·확인 필요·보류를 하나의 완료 상태로 합치지 않습니다.", font=_font(24), fill=MUTED)
    x, y, width, height, gap = 90, 220, 285, 220, 45
    for index, (label, value, color) in enumerate(categories):
        current = (x + index * (width + gap), y, x + index * (width + gap) + width, y + height)
        _box(draw, current, fill=WHITE, outline=color, width=4)
        draw.text((current[0] + 28, current[1] + 28), label, font=_font(30, True), fill=color)
        count_text = str(value)
        text_width = draw.textbbox((0, 0), count_text, font=_font(72, True))[2]
        draw.text((current[0] + (width - text_width) / 2, current[1] + 90), count_text, font=_font(72, True), fill=INK)
        draw.text((current[0] + 28, current[3] - 48), "등록 항목 수", font=_font(21), fill=MUTED)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, quality=95)


def build_responsibility_diagram(document: dict[str, Any], output: Path) -> None:
    responsibilities = document.get("responsibilities", {})
    owns = responsibilities.get("owns", []) or ["[작성 필요]"]
    does_not_own = responsibilities.get("does_not_own", []) or ["[작성 필요]"]
    interfaces = responsibilities.get("interfaces", [])
    image = Image.new("RGB", (1800, 900), BG)
    draw = ImageDraw.Draw(image)
    draw.text((70, 38), "책임·협업 경계", font=_font(48, True), fill=INK)
    draw.text((70, 100), "이 분야가 소유하는 결정과 다른 분야에서 받아야 하는 입력·제공할 출력을 구분합니다.", font=_font(24), fill=MUTED)
    left = (70, 185, 820, 505)
    right = (980, 185, 1730, 505)
    _box(draw, left, fill=ACCENT_LIGHT, outline=ACCENT)
    _box(draw, right, fill=WHITE, outline=WARN)
    draw.text((100, 215), "이 분야가 소유", font=_font(31, True), fill=ACCENT)
    draw.text((1010, 215), "이 분야가 소유하지 않음", font=_font(31, True), fill=WARN)
    for index, item in enumerate(owns[:7]):
        draw.text((110, 275 + index * 36), f"• {item}", font=_font(23), fill=INK)
    for index, item in enumerate(does_not_own[:7]):
        draw.text((1020, 275 + index * 36), f"• {item}", font=_font(23), fill=INK)
    y = 570
    draw.text((70, y), "주요 분야 간 계약", font=_font(32, True), fill=INK)
    if not interfaces:
        interfaces = [{"discipline": "[상대 분야]", "receives": "[입력]", "provides": "[출력]"}]
    for index, item in enumerate(interfaces[:4]):
        if not isinstance(item, dict):
            item = {"discipline": str(item), "receives": "-", "provides": "-"}
        x = 70 + index * 425
        current = (x, y + 65, x + 385, y + 250)
        _box(draw, current)
        draw.text((x + 20, y + 85), str(item.get("discipline", "[분야]")), font=_font(25, True), fill=ACCENT)
        receive = f"받음: {item.get('receives', '-') }"
        provide = f"제공: {item.get('provides', '-') }"
        for line_index, line in enumerate(_wrap(draw, receive, _font(20), 345)[:2]):
            draw.text((x + 20, y + 130 + line_index * 25), line, font=_font(20), fill=MUTED)
        for line_index, line in enumerate(_wrap(draw, provide, _font(20), 345)[:2]):
            draw.text((x + 20, y + 185 + line_index * 25), line, font=_font(20), fill=MUTED)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, quality=95)
