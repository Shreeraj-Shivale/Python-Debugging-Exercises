from datetime import datetime, timedelta


def get_billing_period():
    now = datetime.utcnow()
    return {
        "month": str(now.month).zfill(2),
        "year": str(now.year),
        "label": now.strftime("%B %Y"),
    }


def days_until_due(payment_terms):
    terms_map = {
        "net15": 15,
        "net30": 30,
        "net45": 45,
        "net60": 60,
        "immediate": 0,
    }
    return terms_map.get(payment_terms.lower(), 30)


def format_date(dt):
    if isinstance(dt, str):
        return dt
    return dt.strftime("%Y-%m-%d")


def is_same_month(d1, d2):
    return d1.year == d2.year and d1.month == d2.month


def add_business_days(start_date, num_days):
    current = start_date
    added = 0
    while added < num_days:
        current += timedelta(days=1)
        if current.weekday() < 5:
            added += 1
    return current
