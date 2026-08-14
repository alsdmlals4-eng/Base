#!/usr/bin/env python3
from pathlib import Path

path = Path("tools/run_periodic_source_scan_queue.sh")
text = path.read_text(encoding="utf-8")
old = "python tools/periodic_source_analysis.py \\\n"
new = "python -m tools.periodic_source_analysis \\\n"
if text.count(old) != 1:
    raise SystemExit(f"expected exactly one runner invocation, found {text.count(old)}")
path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
