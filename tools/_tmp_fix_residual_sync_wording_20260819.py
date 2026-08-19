from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "skills/running-adversarial-review-and-refinement/SKILL.md"
text = p.read_text(encoding="utf-8")
old = "- `BLOCKED_UNVERIFIED`: 필요한 도구·권한·정본·CI·런타임·Sheets 증거가 없어 완료 판정할 수 없다."
new = "- `BLOCKED_UNVERIFIED`: 필요한 도구·권한·정본·CI·런타임·Notion readback/sync 증거가 없어 완료 판정할 수 없다."
if old not in text:
    raise SystemExit("RESIDUAL_SHEETS_EVIDENCE_PATTERN_MISSING")
p.write_text(text.replace(old, new), encoding="utf-8")
Path(__file__).unlink()
print("RESIDUAL_SYNC_WORDING_FIXED")
