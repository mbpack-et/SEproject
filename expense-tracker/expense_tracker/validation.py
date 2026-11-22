"""Input validation for values entered through the CLI."""
import math
from datetime import date as _date


class ValidationError(ValueError):
    """Raised when user input is not acceptable."""


def parse_amount(text):
    try:
        value = float(text)
    except (TypeError, ValueError):
        raise ValidationError(f"amount must be a number, got {text!r}") from None
    if not math.isfinite(value) or value <= 0:
        raise ValidationError(f"amount must be a positive finite number, got {text!r}")
    return value


def parse_date(text):
    try:
        return _date.fromisoformat(text).isoformat()
    except (TypeError, ValueError):
        raise ValidationError(f"date must be YYYY-MM-DD, got {text!r}") from None


def normalize_category(text):
    value = (text or "").strip().lower()
    if not value:
        raise ValidationError("category must not be empty")
    return value
