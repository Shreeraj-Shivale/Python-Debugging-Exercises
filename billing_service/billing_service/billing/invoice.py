from utils.date_helpers import get_billing_period, days_until_due
from utils.formatters import format_currency
from billing.calculator import calculate_total


def build_invoice(customer):
    period = get_billing_period()
    items = customer.get("line_items", [])

    subtotal = calculate_total(items)
    tax = round(subtotal * customer.get("tax_rate", 0.0), 2)
    total = subtotal + tax

    due_days = days_until_due(customer.get("payment_terms", "net30"))

    invoice = {
        "invoice_id": _generate_invoice_id(customer["id"], period),
        "customer_id": customer["id"],
        "customer_name": customer["name"],
        "email": customer.get("email", ""),
        "billing_period": period,
        "line_items": items,
        "subtotal": format_currency(subtotal),
        "tax": format_currency(tax),
        "total": format_currency(total),
        "due_in_days": due_days,
        "status": "pending",
    }

    return invoice


def _generate_invoice_id(customer_id, period):
    month_str = period["month"]
    year_str = period["year"]
    return f"INV-{customer_id}-{year_str}{month_str}"
