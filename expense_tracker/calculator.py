"""Business logic for the expense tracker."""


def reimbursable_amount(expense):
    """How much of an expense the company reimburses."""
    category = expense["category"]
    amount = expense["amount"]
    if category == "travel":
        return amount * 0.9
    elif category == "meals":
        return amount * 0.5
    elif category == "office":
        return amount
    else:
        return 0


def category_label(expense):
    category = expense["category"]
    if category == "travel":
        return "Travel (90% reimbursed)"
    elif category == "meals":
        return "Meals (50% reimbursed)"
    elif category == "office":
        return "Office (100% reimbursed)"
    else:
        return "Other (not reimbursed)"


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
