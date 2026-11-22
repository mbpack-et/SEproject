import unittest

from expense_tracker import calculator


def exp(category, amount, date="2026-11-01"):
    return {"date": date, "category": category, "amount": amount}


class CalculatorTests(unittest.TestCase):
    def test_travel_90_percent(self):
        self.assertAlmostEqual(calculator.reimbursable_amount(exp("travel", 100)), 90)

    def test_meals_50_percent(self):
        self.assertAlmostEqual(calculator.reimbursable_amount(exp("meals", 80)), 40)

    def test_office_full(self):
        self.assertAlmostEqual(calculator.reimbursable_amount(exp("office", 30)), 30)

    def test_other_not_reimbursed(self):
        self.assertEqual(calculator.reimbursable_amount(exp("gifts", 50)), 0)

    def test_totals(self):
        items = [exp("travel", 100), exp("meals", 100)]
        self.assertEqual(calculator.total(items), 200)
        self.assertAlmostEqual(calculator.total_reimbursable(items), 140)

    def test_report_contains_totals(self):
        text = calculator.build_report([exp("office", 10)])
        self.assertIn("TOTAL: 10.00", text)
        self.assertIn("REIMBURSABLE: 10.00", text)


if __name__ == "__main__":
    unittest.main()
