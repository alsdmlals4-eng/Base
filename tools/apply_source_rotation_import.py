#!/usr/bin/env python3
"""Connect the reviewed rotating Source selector to the analysis runner."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "tools" / "periodic_source_analysis.py"
text = TARGET.read_text(encoding="utf-8")
old_import = "from tools.periodic_source_operations_state import update_operations_ledger\nfrom tools.periodic_source_scan_queue import load_ledger, parse_iso_date, select_due_sources\n"
new_import = "from tools.periodic_source_operations_state import update_operations_ledger\nfrom tools.periodic_source_rotation_adapter import select_rotating_batch\nfrom tools.periodic_source_scan_queue import load_ledger, parse_iso_date\n"
old_selection = "    selected = select_due_sources(operations, run_date)[:batch_size]\n"
new_selection = "    selected = select_rotating_batch(operations, run_date, batch_size)\n"
if text.count(old_import) != 1:
    raise SystemExit("unexpected analysis import block")
if text.count(old_selection) != 1:
    raise SystemExit("unexpected analysis selection block")
text = text.replace(old_import, new_import, 1)
text = text.replace(old_selection, new_selection, 1)
TARGET.write_text(text, encoding="utf-8", newline="\n")
