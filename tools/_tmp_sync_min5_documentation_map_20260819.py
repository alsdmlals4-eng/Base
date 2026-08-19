from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

map_path = ROOT / "docs/DOCUMENTATION_MAP.md"
text = map_path.read_text(encoding="utf-8")
old = "| 장기 작업 | `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md` | 현행조사→>=3 대안→벤치마킹→5회 전체 적대적 개선→장기 최선안 |"
new = "| 장기 작업 | `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md` | 현행조사→>=3 대안→벤치마킹→최소 5회 전체 적대적 개선→5회 이후 오류·충돌·누락·blocker 0까지 추가 전체 루프→장기 최선안 |"
if text.count(old) != 1:
    raise SystemExit(f"DOCUMENTATION_MAP_PATTERN_COUNT={text.count(old)}")
map_path.write_text(text.replace(old, new, 1), encoding="utf-8")

test_path = ROOT / "tests/test_base_long_horizon_work_contract.py"
test = test_path.read_text(encoding="utf-8")
needle = '''        self.assertIn("장기적으로 최선", policy)\n'''
replacement = '''        self.assertIn("장기적으로 최선", policy)\n        documentation_map = read("docs/DOCUMENTATION_MAP.md")\n        self.assertIn("최소 5회 전체 적대적 개선", documentation_map)\n        self.assertIn("5회 이후 오류·충돌·누락·blocker 0까지 추가 전체 루프", documentation_map)\n'''
if test.count(needle) != 1:
    raise SystemExit(f"LONG_HORIZON_TEST_INSERT_COUNT={test.count(needle)}")
test_path.write_text(test.replace(needle, replacement, 1), encoding="utf-8")

Path(__file__).unlink()
print("MIN5_DOCUMENTATION_MAP_SYNCED")
