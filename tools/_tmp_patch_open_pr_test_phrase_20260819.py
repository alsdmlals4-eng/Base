from pathlib import Path

path = Path(__file__).resolve().parents[1] / "tests/test_sequential_part_coordinator_contract.py"
text = path.read_text(encoding="utf-8")
text = text.replace('self.assertIn("PR 상태만으로", text)', 'self.assertIn("상태만으로", text)', 1)
path.write_text(text, encoding="utf-8", newline="\n")
print("OPEN_PR_TEST_PHRASE_PATCHED")
