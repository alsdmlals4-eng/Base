from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "tools/apply_archive_governance_base_rollout.py"

spec = importlib.util.spec_from_file_location("archive_rollout", TARGET)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def safe_replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old in text:
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
        return
    if new in text:
        return
    raise RuntimeError(f"expected text not found in {path}: {old!r}")


module.replace_once = safe_replace_once
module.main()
