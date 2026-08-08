from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main_text(path: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"origin/main:{path}"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    )


def indent_record(record: dict) -> str:
    return "\n".join("    " + line for line in json.dumps(record, ensure_ascii=False, indent=2).splitlines())


def append_records_from_current(path: str, selector) -> None:
    current = json.loads((ROOT / path).read_text(encoding="utf-8"))
    records = selector(current)
    base = main_text(path)
    marker = "\n  ]\n}"
    if marker not in base:
        raise RuntimeError(f"tail marker not found in {path}")
    prefix, suffix = base.rsplit(marker, 1)
    addition = ",\n" + ",\n".join(indent_record(record) for record in records)
    (ROOT / path).write_text(prefix + addition + marker + suffix, encoding="utf-8")


def main() -> None:
    append_records_from_current(
        "skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json",
        lambda doc: [case for case in doc["cases"] if case["case_id"] in {"SBE-950", "SBE-951"}],
    )
    append_records_from_current(
        "skills/SKILL_IMPLEMENTATION_EVIDENCE.json",
        lambda doc: [
            entry
            for entry in doc["entries"]
            if entry["skill_id"] == "developing-and-revising-serial-fiction"
        ],
    )
    subprocess.run(
        ["python", "tools/build_skill_implementation_evidence.py"],
        cwd=ROOT,
        check=True,
    )


if __name__ == "__main__":
    main()
