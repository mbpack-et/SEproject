import contextlib
import io
import os
import tempfile
import unittest
from unittest import mock

from expense_tracker import cli, storage


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "expenses.json")
        patcher = mock.patch.dict(os.environ, {"EXPENSE_FILE": self.path})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.tmp.cleanup)

    def run_cli(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = cli.main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def test_add_then_report_end_to_end(self):
        code, out, _ = self.run_cli("add", "2026-11-01", "Travel", "100")
        self.assertEqual((code, out.strip()), (0, "Added."))
        code, out, _ = self.run_cli("report")
        self.assertEqual(code, 0)
        self.assertIn("Travel (90% reimbursed) | 100.00 -> 90.00", out)
        self.assertIn("REIMBURSABLE: 90.00", out)

    def test_negative_amount_rejected_and_nothing_saved(self):
        code, _, err = self.run_cli("add", "2026-11-01", "travel", "-100")
        self.assertEqual(code, 1)
        self.assertIn("amount", err)
        self.assertEqual(storage.load(), [])

    def test_bad_date_rejected(self):
        code, _, err = self.run_cli("add", "not-a-date", "office", "5")
        self.assertEqual(code, 1)
        self.assertIn("date", err)

    def test_non_numeric_amount_no_traceback(self):
        code, _, err = self.run_cli("add", "2026-11-01", "travel", "abc")
        self.assertEqual(code, 1)
        self.assertIn("Error:", err)

    def test_corrupt_storage_reports_error_exit_1(self):
        with open(self.path, "w") as f:
            f.write("{broken")
        code, _, err = self.run_cli("report")
        self.assertEqual(code, 1)
        self.assertIn("corrupt", err)

    def test_no_args_prints_usage_exit_2(self):
        code, _, err = self.run_cli()
        self.assertEqual(code, 2)
        self.assertIn("Usage:", err)

    def test_unknown_command_exit_2(self):
        code, _, err = self.run_cli("export", "--csv")
        self.assertEqual(code, 2)
        self.assertIn("Usage:", err)


if __name__ == "__main__":
    unittest.main()
