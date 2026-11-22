"""Business logic for the expense tracker."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ReimbursementRule:
    """One reimbursement policy: the share paid back and how it is displayed."""

    rate: float
    label: str

    def amount(self, spent):
        return spent * self.rate


# Single source of truth: adding a category means adding one line here.
RULES = {
    "travel": ReimbursementRule(0.9, "Travel (90% reimbursed)"),
    "meals": ReimbursementRule(0.5, "Meals (50% reimbursed)"),
    "office": ReimbursementRule(1.0, "Office (100% reimbursed)"),
}
DEFAULT_RULE = ReimbursementRule(0.0, "Other (not reimbursed)")


def rule_for(expense):
    return RULES.get(expense["category"], DEFAULT_RULE)


def reimbursable_amount(expense):
    """How much of an expense the company reimburses."""
    return rule_for(expense).amount(expense["amount"])


def category_label(expense):
    return rule_for(expense).label


def total(expenses):
    return sum(e["amount"] for e in expenses)


def total_reimbursable(expenses):
    return sum(reimbursable_amount(e) for e in expenses)


def build_report(expenses):
    lines = []
    for e in expenses:
        lines.append(
            f"{e['date']} | {category_label(e)} | {e['amount']:.2f} -> {reimbursable_amount(e):.2f}"
        )
    lines.append(f"TOTAL: {total(expenses):.2f}")
    lines.append(f"REIMBURSABLE: {total_reimbursable(expenses):.2f}")
    return "\n".join(lines)
