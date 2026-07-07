import json
from pathlib import Path
from hybrid_search.query_parser import parse_query
from llm.llm_query_parser import llm_parse_query
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

#Load known brands
def load_known_brands(metadata_path="data/embeddings/product_metadata.json"):
    """
    Extract unique brands from product metadata.
    """

    with open(metadata_path, 'r', encoding='utf-8') as f:
        products = json.load(f)

    brands = {
        product.get('brand')
        for product in products
        if product.get('brand')
        and product.get('brand').strip()
        and product.get('brand').lower() != 'unknown'
    }

    return sorted(brands)

def parse_user_query(query, known_brands):

    parsed = parse_query(query, known_brands)

    needs_llm = (
        parsed.get("category") is None
        or any(
            phrase in query.lower()
            for phrase in [
                "gift",
                "for my",
                "for mom",
                "for dad",
                "for father",
                "for mother",
                "for husband",
                "for wife",
                "for girlfriend",
                "for boyfriend",
                "wedding",
                "office",
                "college",
                "comfortable",
                "stylish",
                "elegant"
            ]
        )
    )

    if needs_llm:

        llm_result = llm_parse_query(query)

        if llm_result:
            parsed = llm_result
            parser_used = "LLM"

        else:
            parser_used = "Regex"

    else:
        parser_used = "Regex"

    return parsed, parser_used

#Semantic Match
def semantic_match(expected, predicted, threshold=0.75):

    emb = model.encode(
        [expected, predicted]
    )

    similarity = cosine_similarity(
        [emb[0]],
        [emb[1]]
    )[0][0]

    return similarity>=threshold

#Evaluate Parser
def evaluate_parser(test_file='evaluation/test_queries.json'):
    """
    Evaluate parser performance on test queries.
    """

    CATEGORY_MAP = {
        "Jewelry": "Jewellery",
        "Ethnic Wear": "Clothing",
        "Handbags": "Bags",
        "Running Shoes": "Footwear"
    }

    known_brands = load_known_brands()

    with open(test_file, 'r', encoding='utf-8') as f:
        test_cases = json.load(f)
    
    total = len(test_cases)

    query_correct = 0
    brand_correct = 0
    min_price_correct = 0
    max_price_correct = 0
    category_correct = 0
    overall_correct = 0

    failures = []

    for idx, test in enumerate(test_cases, start=1):
        query = test['query']
        expected = test['expected']

        predicted, parser_used = parse_user_query(
            query,
            known_brands
        )

        query_match = semantic_match(
            expected['query'],
            predicted['query']
        )

        brand_match = (
            predicted.get('brand') == expected.get('brand')
        )

        min_price_match = (
            predicted.get('min_price') == expected.get('min_price')
        )

        max_price_match = (
            predicted.get('max_price') == expected.get('max_price')
        )

        expected_cat = CATEGORY_MAP.get(
            expected.get("category"),
            expected.get("category")
        )
        predicted_cat = CATEGORY_MAP.get(
            predicted.get("category"),
            predicted.get("category")
        )
        category_match = (
            expected_cat == predicted_cat
        )

        if query_match:
            query_correct+=1
        
        if brand_match:
            brand_correct+=1

        if min_price_match:
            min_price_correct+=1

        if max_price_match:
            max_price_correct+=1
        
        if category_match:
            category_correct+=1
        
        exact_match = all([
            query_match,
            brand_match,
            min_price_match,
            max_price_match,
            category_match
        ])

        if exact_match:
            overall_correct+=1
        else:
            failures.append({
                "test_case": idx,
                "parser_used": parser_used,
                "original_query": query,
                "expected": expected,
                "predicted": predicted
            })
    

    #Print Metrics

    print("\n" + "=" * 80)
    print("PARSER EVALUATION REPORT")
    print("=" * 80)

    print(f'Total Test Cases     : {total}')

    print(
        f'Query Accuracy        : '
        f'{query_correct}/{total}'
        f'({query_correct/total * 100:.2f}%)'
    )

    print(
        f'Brand Accuracy        : '
        f'{brand_correct}/{total}'
        f'({brand_correct/total * 100:.2f}%)'
    )

    print(
        f'Min Price Accuracy        : '
        f'{min_price_correct}/{total}'
        f'({min_price_correct/total * 100:.2f}%)'
    )

    print(
        f'Max Price Accuracy        : '
        f'{max_price_correct}/{total}'
        f'({max_price_correct/total * 100:.2f}%)'
    )

    print(
        f'Category Accuracy        : '
        f'{category_correct}/{total}'
        f'({category_correct/total * 100:.2f}%)'
    )

    print(
        f'Overall Exact Match        : '
        f'{overall_correct}/{total}'
        f'({overall_correct/total * 100:.2f}%)'
    )

    print("="*80)

    #Print Failures

    if failures:
        print('\n Failed Test Cases')
        print('='*80)

        for failure in failures:

            print(f'\nTest Case #{failure['test_case']}')

            print(
                f'Original Query:\n'
                f'{failure['original_query']}'
            )

            print(
                f'\nExpected:\n'
                f'{json.dumps(failure['expected'], indent=4)}'
            )

            print(
                f'Predicted:\n'
                f'{json.dumps(failure['predicted'], indent=4)}'
            )

            print('-'*80)
    
    else:
        print('\n All test cases passed')

    return {
        'total': total,
        'query_accuracy': query_correct / total,
        'brand_accuracy': brand_correct / total,
        'min_price_accuracy': min_price_correct / total,
        'max_price_accuracy': max_price_correct / total,
        'category_accuracy': category_correct / total,
        'overall_exact_match': overall_correct / total
    }


#Main

if __name__ == '__main__':
    metrics = evaluate_parser()

    with open('evaluation/results.json', 'w') as f:
        json.dump(metrics, f, indent=4)
