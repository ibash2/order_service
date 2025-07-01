from decimal import Decimal
from datetime import datetime


def decimal_to_json(value):
    if value is None:
        return None

    return float(value)


def decimal_from_json(value):
    if value is None:
        return None

    return Decimal(value)


def datetime_to_json(value):
    if value is None:
        return None

    return value.isoformat()


def datetime_from_json(value):
    if value is None:
        return None

    return datetime.fromisoformat(value)
