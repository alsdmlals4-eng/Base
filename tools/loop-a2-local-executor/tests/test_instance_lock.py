from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from loop_a2_local_executor.instance_lock import InstanceLock, InstanceLockError


class InstanceLockTests(unittest.TestCase):
    def test_second_executor_instance_is_rejected_until_first_releases(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "executor.lock"
            first = InstanceLock(path)
            first.acquire()
            try:
                second = InstanceLock(path)
                with self.assertRaises(InstanceLockError) as caught:
                    second.acquire()
                self.assertEqual(caught.exception.code, "LOCAL_EXECUTOR_ALREADY_RUNNING")
            finally:
                first.release()

            third = InstanceLock(path)
            third.acquire()
            third.release()

    def test_context_manager_releases_lock(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "executor.lock"
            with InstanceLock(path):
                self.assertTrue(path.exists())
            with InstanceLock(path):
                self.assertTrue(path.exists())


if __name__ == "__main__":
    unittest.main()
