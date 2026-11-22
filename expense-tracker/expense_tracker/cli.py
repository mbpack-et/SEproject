"""Command-line interface: python -m expense_tracker add|report"""
import sys

from . import calculator, storage
from .storage import StorageError
from .validation import ValidationError, normalize_category, parse_amount, parse_date


def add(date, category, amount):
    expense = {
        "date": parse_date(date),
        "category": normalize_category(category),
        "amount": parse_amount(amount),
    }
    expenses = storage.load()
    expenses.append(expense)
    storage.save(expenses)
    print("Added.")


def report():
    print(calculator.build_report(storage.load()))


USAGE = "Usage: python -m expense_tracker add DATE CATEGORY AMOUNT | report"


def main(argv):
    try:
        if len(argv) == 4 and argv[0] == "add":
            add(argv[1], argv[2], argv[3])
        elif len(argv) == 1 and argv[0] == "report":
            report()
        else:
            print(USAGE, file=sys.stderr)
            return 2
    except (ValidationError, StorageError) as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
