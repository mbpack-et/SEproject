"""JSON file storage."""
import json
import os


class StorageError(Exception):
    """Raised when the data file cannot be read or has an unexpected shape."""


def data_file():
    # Read at call time so the path can be changed (e.g. in tests).
    return os.environ.get("EXPENSE_FILE", "expenses.json")


def load():
    path = data_file()
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as err:
        raise StorageError(f"cannot read {path}: file is corrupt ({err})") from err
    except OSError as err:
        raise StorageError(f"cannot open {path}: {err}") from err
    if not isinstance(data, list):
        raise StorageError(f"{path} must contain a JSON list of expenses")
    return data


def save(expenses):
    path = data_file()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(expenses, f)
    except OSError as err:
        raise StorageError(f"cannot write {path}: {err}") from err
