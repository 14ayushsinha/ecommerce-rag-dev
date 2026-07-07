import re


def parse_query(user_query, known_brands):

    parsed = {
        'query': user_query,
        'brand': None,
        'min_price': None,
        'max_price': None,
        'category': None
    }

    query = user_query.lower()

    # ======================================
    # Normalize price symbols
    # ======================================

    query = re.sub(r'₹', '', query)
    query = re.sub(r'/-', '', query)

    # ======================================
    # Between Price
    # Examples:
    # between 300 and 500
    # between 300 to 500
    # between ₹300/- and ₹500/-
    # ======================================

    match = re.search(
        r'between\s+(\d+)\s*(?:and|to)\s*(\d+)',
        query
    )

    if match:

        parsed['min_price'] = int(match.group(1))
        parsed['max_price'] = int(match.group(2))

        query = re.sub(
            re.escape(match.group(0)),
            '',
            query,
            count=1
        )

    else:

        # ======================================
        # Under / Below Price
        # ======================================

        match = re.search(
            r'(?:under|below|less than)\s*(\d+)',
            query
        )

        if match:

            parsed['max_price'] = int(match.group(1))

            query = re.sub(
                re.escape(match.group(0)),
                '',
                query,
                count=1
            )

        # ======================================
        # Above / Over Price
        # ======================================

        match = re.search(
            r'(?:above|over|greater than|more than)\s*(\d+)',
            query
        )

        if match:

            parsed['min_price'] = int(match.group(1))

            query = re.sub(
                re.escape(match.group(0)),
                '',
                query,
                count=1
            )

    # ======================================
    # Brand Detection
    # Uses word boundaries to avoid:
    # notebook → OK
    # classmate → SSM
    # ======================================

    for brand in known_brands:

        if not brand:
            continue

        pattern = rf'\b{re.escape(brand.lower())}\b'

        if re.search(pattern, query):

            parsed['brand'] = brand

            query = re.sub(
                pattern,
                '',
                query,
                count=1
            )

            break

    # ======================================
    # Final Query Cleanup
    # ======================================

    query = re.sub(r'\s+', ' ', query).strip()

    parsed['query'] = query

    return parsed