"""JSON file storage."""
import json
import os

DATA_FILE = os.environ.get("EXPENSE_FILE", "expenses.json")


def load():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f)


def save(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f)
