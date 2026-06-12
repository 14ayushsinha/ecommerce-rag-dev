import json
import pickle
from rank_bm25 import BM25Okapi

def build_search_text(product):

    return f"""
    {product['name']}
    {product['brand']}
    {product['main_category']}
    {product['subcategory']}
    {product['full_category_path']}
    {product['description']}
    """.lower()

def main():

    print('Loading metadata...')

    with open("data/embeddings/product_metadata.json", 'r') as f:
        products = json.load(f)

    print(f'Loaded {len(products)}, products')

    # seen = set()
    # unique_products = []

    # for product in products:
    #     pid = product['id']

    #     if pid not in seen:
    #         seen.add(pid)
    #         unique_products.append(product)
    
    # products = unique_products

    # print(f'After deduplication: {len(products)} products')

    # from collections import Counter

    # counter = Counter(product["id"] for product in products)

    # duplicates = sum(count > 1 for count in counter.values())

    # print(f"Duplicate products: {duplicates}")

    print('Building BM25 corpus...')

    corpus = []

    for product in products:
        text = build_search_text(product)
        corpus.append(text.split())
    
    print('Training BM25...')

    bm25 = BM25Okapi(corpus)

    print('Saving BM25 index...')

    with open("hybrid_search/bm25.pkl", 'wb') as f:
        pickle.dump(bm25, f)
    
    print('Done.')

if __name__ == '__main__':
    main()