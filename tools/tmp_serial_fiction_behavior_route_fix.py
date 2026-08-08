from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIMARY_PATH = "skills/SKILL_BEHAVIOR_EVALS.json"
COVERAGE_PATH = "skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json"


def main_text(path: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"origin/main:{path}"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    )


def indent_record(record: dict) -> str:
    return "\n".join("    " + line for line in json.dumps(record, ensure_ascii=False, indent=2).splitlines())


def append_records_to_main(path: str, records: list[dict]) -> None:
    base = main_text(path)
    marker = "\n  ]\n}"
    if marker not in base:
        raise RuntimeError(f"tail marker not found in {path}")
    prefix, suffix = base.rsplit(marker, 1)
    addition = ""
    if records:
        addition = ",\n" + ",\n".join(indent_record(record) for record in records)
    (ROOT / path).write_text(prefix + addition + marker + suffix, encoding="utf-8")


def main() -> None:
    coverage = json.loads((ROOT / COVERAGE_PATH).read_text(encoding="utf-8"))
    fiction = next(case for case in coverage["cases"] if case["case_id"] == "SBE-950")
    boundary = next(case for case in coverage["cases"] if case["case_id"] == "SBE-951")

    append_records_to_main(PRIMARY_PATH, [fiction])
    append_records_to_main(COVERAGE_PATH, [boundary])

    test_path = ROOT / "tests/test_skill_behavior_adversarial_boundaries.py"
    text = test_path.read_text(encoding="utf-8")
    old = '''        coverage = json.loads(\n            (ROOT / "skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json").read_text(encoding="utf-8")\n        )\n        cases = {case["case_id"]: case for case in coverage["cases"]}\n        fiction = cases["SBE-950"]\n'''
    new = '''        primary = json.loads(\n            (ROOT / "skills/SKILL_BEHAVIOR_EVALS.json").read_text(encoding="utf-8")\n        )\n        coverage = json.loads(\n            (ROOT / "skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json").read_text(encoding="utf-8")\n        )\n        primary_cases = {case["case_id"]: case for case in primary["cases"]}\n        coverage_cases = {case["case_id"]: case for case in coverage["cases"]}\n        fiction = primary_cases["SBE-950"]\n'''
    if old not in text and 'fiction = primary_cases["SBE-950"]' not in text:
        raise RuntimeError("expected adversarial behavior test block not found")
    if old in text:
        text = text.replace(old, new, 1)
    text = text.replace('        game = cases["SBE-951"]\n', '        game = coverage_cases["SBE-951"]\n', 1)
    test_path.write_text(text, encoding="utf-8")

    subprocess.run(
        ["python", "tools/build_skill_implementation_evidence.py"],
        cwd=ROOT,
        check=True,
    )


if __name__ == "__main__":
    main()
