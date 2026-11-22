"""Command-line interface: python -m expense_tracker.cli add|report"""
import sys

from . import calculator, storage


def add(date, category, amount):
    expenses = storage.load()
    expenses.append({"date": date, "category": category, "amount": float(amount)})
    storage.save(expenses)
    print("Added.")


def report():
    print(calculator.build_report(storage.load()))


def main(argv):
    if argv[0] == "add":
        add(argv[1], argv[2], argv[3])
    elif argv[0] == "report":
        report()
    else:
        print("Unknown command")


if __name__ == "__main__":
    main(sys.argv[1:])
