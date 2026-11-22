import unittest

from expense_tracker.validation import (
    ValidationError,
    normalize_category,
    parse_amount,
    parse_date,
)


class ValidationTests(unittest.TestCase):
    def test_amount_valid(self):
        self.assertEqual(parse_amount("12.5"), 12.5)

    def test_amount_rejects_negative_zero_text_nan_inf(self):
        for bad in ["-100", "0", "abc", "", "nan", "inf"]:
            with self.subTest(bad=bad):
                with self.assertRaises(ValidationError):
                    parse_amount(bad)

    def test_date_valid(self):
        self.assertEqual(parse_date("2026-11-01"), "2026-11-01")

    def test_date_rejects_garbage(self):
        for bad in ["not-a-date", "2026-13-01", "2026-02-30", ""]:
            with self.subTest(bad=bad):
                with self.assertRaises(ValidationError):
                    parse_date(bad)

    def test_category_normalized(self):
        self.assertEqual(normalize_category("  Travel "), "travel")

    def test_category_empty_rejected(self):
        with self.assertRaises(ValidationError):
            normalize_category("   ")


if __name__ == "__main__":
    unittest.main()
