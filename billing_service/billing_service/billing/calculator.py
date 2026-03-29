def calculate_total(line_items):
    total = 0
    for item in line_items:
        qty = item.get("quantity", 1)
        price = item.get("unit_price", 0)
        discount = item.get("discount", 0)

        line_total = qty * price
        line_total = line_total - (line_total * discount)
        total += line_total

    return round(total, 2)


def apply_credit(total, credit_balance):
    if credit_balance <= 0:
        return total

    remaining = total - credit_balance
    if remaining < 0:
        return 0
    return round(remaining, 2)


def is_overdue(invoice, current_date):
    from datetime import datetime
    due_str = invoice.get("due_date", "")
    if not due_str:
        return False
    due = datetime.strptime(due_str, "%Y-%m-%d")
    return current_date > due
