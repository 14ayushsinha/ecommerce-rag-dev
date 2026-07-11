from llm.followup_classifier import classify_followup

def is_followup(context, query):

    if context.query is None:
        return False

    q = query.lower().strip()

    # Very obvious refinements
    obvious_followups = [
        "cheaper",
        "premium",
        "better",
        "another",
        "similar",
        "show more",
        "for men",
        "for women",
        "same brand",
        "same category"
    ]

    for word in obvious_followups:
        if q == word or q.startswith(word):
            return True

    # Very obvious new searches
    obvious_new = [
        "show me",
        "find",
        "search",
        "looking for",
        "need",
        "want",
        "recommend",
        "suggest",
        "i need",
        "i want",
        "get me"
    ]

    for word in obvious_new:
        if q.startswith(word):
            return False

    # Everything else -> GPT decides
    return classify_followup(
        previous_query=context.to_dict(),
        current_query=query
    )