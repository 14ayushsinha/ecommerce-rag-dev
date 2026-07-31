import re

USD_TO_INR = 87.0


def convert_to_inr(price):

    if price is None:
        return None

    if isinstance(price, (int, float)):
        return round(float(price) * USD_TO_INR, 2)

    price = str(price).strip()

    # Remove symbols
    price = (
        price.replace("$", "")
             .replace("USD", "")
             .replace(",", "")
             .replace("₹", "")
             .replace("Rs.", "")
             .replace("Rs", "")
             .strip()
    )

    try:
        return round(float(price) * USD_TO_INR, 2)
    except ValueError:
        return None