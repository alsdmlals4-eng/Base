from __future__ import annotations

import base64
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPORTS = {
    "SKILL_REGISTRY": ROOT / "skills/SKILL_REGISTRY.json",
    "BASE_ACTIVE_SKILLS": ROOT / "docs/generated/BASE_ACTIVE_SKILLS.md",
}


class TemporaryRegistryExportTests(unittest.TestCase):
    def test_export_exact_registry_sources_for_bounded_correction(self) -> None:
        for name, path in EXPORTS.items():
            data = path.read_bytes()
            encoded = base64.b64encode(data).decode("ascii")
            print(f"TEMP_EXPORT_BEGIN:{name}:{len(data)}")
            for index in range(0, len(encoded), 120):
                chunk = encoded[index : index + 120]
                print(f"TEMP_EXPORT_CHUNK:{name}:{index // 120:05d}:{chunk}")
            print(f"TEMP_EXPORT_END:{name}")
        self.fail("TEMP_REGISTRY_EXPORT_COMPLETE_REMOVE_BEFORE_MERGE")


if __name__ == "__main__":
    unittest.main()
