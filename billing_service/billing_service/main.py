import json
from billing.processor import InvoiceProcessor
from billing.invoice import build_invoice
from utils.validators import validate_customer


def load_customers(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def run_billing_cycle(customers_file):
    customers = load_customers(customers_file)
    processor = InvoiceProcessor()

    results = {"sent": [], "failed": [], "skipped": []}

    for customer in customers:
        if not validate_customer(customer):
            results["skipped"].append(customer.get("id", "unknown"))
            continue

        invoice = build_invoice(customer)
        success = processor.process(invoice)

        if success:
            results["sent"].append(customer["id"])
        else:
            results["failed"].append(customer["id"])

    print(f"Billing cycle complete.")
    print(f"  Sent:    {len(results['sent'])}")
    print(f"  Failed:  {len(results['failed'])}")
    print(f"  Skipped: {len(results['skipped'])}")
    return results


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python main.py <customers.json>")
        sys.exit(1)

    run_billing_cycle(sys.argv[1])
