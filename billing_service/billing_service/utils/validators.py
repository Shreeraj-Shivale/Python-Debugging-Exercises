import re


def validate_customer(customer):
    required_fields = ["id", "name", "email"]
    for field in required_fields:
        if not customer.get(field):
            return False

    if not _is_valid_email(customer["email"]):
        return False

    if not isinstance(customer.get("line_items", []), list):
        return False

    return True


def _is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return re.match(pattern, email) is not None


def validate_line_item(item):
    if not item.get("name"):
        return False
    if item.get("quantity", 0) <= 0:
        return False
    if item.get("unit_price", -1) < 0:
        return False
    return True


def sanitize_string(value, max_length=255):
    if not isinstance(value, str):
        value = str(value)
    return value.strip()[:max_length]
