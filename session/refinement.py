def is_refinement(query: str):
    query = query.lower().strip()

    refinement_keywords = [

        "only",

        "cheaper",
        "more expensive",

        "for women",
        "for men",

        "show more",

        "same brand",
        "same category",

        "these",
        "those",

        "instead",
        "also"
    ]

    return any(
        keyword in query
        for keyword in refinement_keywords
    )

def apply_refinement(query, context):
    q = query.lower().strip()

    if 'show more' in q:
        context.limit += 5

        return context.to_dict()
    
    if 'cheaper' in q:
        if context.max_price:
            context.max_price = int(context.max_price*0.7)
        return context.to_dict()
    
    if 'for women' in q:
        context.query = (f'women {context.query}')
        return context.to_dict()

    if 'for men' in q:
        context.query = (f'men {context.query}')
        return context.to_dict()
    
    if q.startswith('only'):
        brand = q.replace('only', '').strip()
        context.brand = brand.title()
        return context.to_dict()
    
    return None