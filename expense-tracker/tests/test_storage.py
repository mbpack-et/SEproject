import os
import tempfile
import unittest
from unittest import mock

from expense_tracker import storage
from expense_tracker.storage import StorageError


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "e.json")
        patcher = mock.patch.dict(os.environ, {"EXPENSE_FILE": self.path})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.tmp.cleanup)

    def test_missing_file_is_empty_list(self):
        self.assertEqual(storage.load(), [])

    def test_round_trip(self):
        data = [{"date": "2026-11-01", "category": "office", "amount": 5.0}]
        storage.save(data)
        self.assertEqual(storage.load(), data)

    def test_corrupt_json_raises_storage_error(self):
        with open(self.path, "w") as f:
            f.write("{broken")
        with self.assertRaises(StorageError):
            storage.load()

    def test_wrong_shape_raises_storage_error(self):
        with open(self.path, "w") as f:
            f.write('{"a": 1}')
        with self.assertRaises(StorageError):
            storage.load()


if __name__ == "__main__":
    unittest.main()
