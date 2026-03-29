def format_currency(amount, symbol="$"):
    return f"{symbol}{amount:,.2f}"


def render_invoice_text(invoice):
    lines = [
        f"Invoice ID:  {invoice['invoice_id']}",
        f"Customer:    {invoice['customer_name']}",
        f"Period:      {invoice['billing_period']['label']}",
        f"",
        f"LINE ITEMS",
        f"----------",
    ]

    for item in invoice.get("line_items", []):
        name = item.get("name", "Service")
        qty = item.get("quantity", 1)
        price = item.get("unit_price", 0)
        lines.append(f"  {name} x{qty} @ ${price:.2f}")

    lines += [
        f"",
        f"Subtotal:    {invoice['subtotal']}",
        f"Tax:         {invoice['tax']}",
        f"Total Due:   {invoice['total']}",
        f"",
        f"Payment due in {invoice['due_in_days']} days.",
        f"Thank you for your business.",
    ]

    return "\n".join(lines)


def truncate(text, max_len=80):
    if len(text) > max_len:
        return text[:max_len - 3] + "..."
    return text


def snake_to_title(s):
    return s.replace("_", " ").title()
