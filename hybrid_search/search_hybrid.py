import os
import json
import pickle
from collections import defaultdict
from dotenv import load_dotenv
from vector_db.search import search_products
from hybrid_search.query_parser import parse_query
from llm.llm_query_parser import llm_parse_query

#Load BM25 Artifacts

print('Loading BM25 index...')

with open('hybrid_search/bm25.pkl', 'rb') as f:
    bm25 = pickle.load(f)

print('Loading product metadata...')

with open('data/embeddings/product_metadata.json', 'r') as f:
    products = json.load(f)

print(f'Loaded {len(products)} products')

known_brands = list({
    product['brand']

    for product in products
    if product.get('brand') and product['brand'] != 'Unknown'
})

#Product lookup dictionary

product_lookup = {
    product['id']: product
    for product in products
}

#BM25 Filtering Helper

def passes_filters(product, max_price=None, brand=None, category=None):

    if max_price is not None:
        price = product.get('discounted_price')

        if price is None or price > max_price:
            return False
    
    if brand:
        product_brand = product.get('brand')

        if product_brand is None or product_brand.lower() != brand.lower():
            return False

    if category:
        product_catgoery = product.get('category')

        if product_catgoery is None or product_catgoery.lower() != category.lower():
            return False
    
    return True

#BM25 search

def bm25_search(query, min_price=None, max_price=None, brand=None, category=None, limit=100):
    tokenized_query = query.lower().split()

    scores = bm25.get_scores(tokenized_query)

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )

    filtered_indices = []

    for idx in ranked_indices:
        product = products[idx]

        if passes_filters(
            product,
            max_price=max_price,
            brand=brand,
            category=category
        ):
            filtered_indices.append(idx)

        if len(filtered_indices) == limit:
            break

    return filtered_indices

#Reciprocal Rank Fusion

def reciprocal_rank_fusion(bm25_results, vector_results, k=60):

    fused_scores = defaultdict(float)

    #BM25 Contribution
    for rank, idx in enumerate(bm25_results):
        product_id = products[idx]['id']
        fused_scores[product_id]+=1/(k+rank+1)
    
    #Vector Contribution
    for rank, point in enumerate(vector_results):
        product_id = point.payload['product_id']
        fused_scores[product_id]+=1/(k+rank+1)

    return fused_scores

#Diversification

def diversify_results(fused_scores, limit=5):

    ranked = sorted(
        fused_scores.items(),
        key=lambda x:x[1],
        reverse=True
    )

    final_results = []

    seen_names = set()

    for product_id, score in ranked:
        product = product_lookup.get(product_id)

        if product is None:
            continue

        name = product['name'].lower()

        if name in seen_names:
            continue
        
        seen_names.add(name)
        
        final_results.append((product, score))

        if len(final_results) == limit:
            break
        
    return final_results

#LLM Keywords

def should_use_llm(query):

    keywords = [
        'gift',
        'comfortable',
        'stylish',
        'casual',
        'formal',
        'office',
        'college',
        'wedding',
        'party',
        'winter',
        'summer',
        'festive',
        'elegant',
        'birthday',
        'anniversary',
        'father',
        'mother',
        'husband',
        'wife',
        'brother',
        'sister'
    ]

    query = query.lower()

    return any(
        keyword in query
        for keyword in keywords
    )

#Hybrid Search

def hybrid_search(query, brand=None, category=None, min_price=None, max_price=None, limit=5):

    if(brand is None and category is None and min_price is None and max_price is None):
        parsed = parse_query(
            query,
            known_brands
        )
    
    else:

        parsed = {
            'query': query,
            'brand': brand,
            'category': category,
            'min_price': min_price,
            'max_price': max_price
        }
    
    llm_used = False

    if brand is None and category is None and should_use_llm(query):

        llm_result = llm_parse_query(query)

        if llm_result:

            llm_used = True

            if llm_result['min_price'] is None:
                llm_result['min_price'] = parsed['min_price']
            
            if llm_result['max_price'] is None:
                llm_result['max_price'] = parsed['max_price']

            if llm_result['brand'] is None:
                llm_result['brand'] = parsed['brand']

            parsed = llm_result
            
    print("\n" + "=" * 80)
    print(f"Original Query : {query}")
    print(f"Parser Used    : {'LLM' if llm_used else 'Regex'}")
    print(f"Parsed Query   : {parsed}")
    print("=" * 80)

    bm25_results = bm25_search(
        query=parsed['query'],
        brand=parsed['brand'],
        min_price=parsed['min_price'],
        max_price=parsed['max_price'],
        limit=100
    )

    vector_results = search_products(
        query=parsed['query'],
        brand=parsed['brand'],
        min_price=parsed['min_price'],
        max_price=parsed['max_price'],
        limit=50
    )
    # print(vector_results[0].payload)

    fused_scores = reciprocal_rank_fusion(
        bm25_results,
        vector_results
    )

    final_results = diversify_results(
        fused_scores,
        limit=limit
    )
    print("HYBRID:", parsed)
    
    return final_results, parsed

#Main

if __name__ == '__main__':

    query = input('Query: ')

    results = hybrid_search(query)

    for rank, (product, score) in enumerate(results, start=1):
        print('\n'+'='*80)
        print(f'Rank #{rank}')
        print(f'Hybrid Search: {score:.4f}')
        print(f'ID: {product['id']}')
        print(f'Name: {product['name']}')
        print(f'Brand: {product['brand']}')
        print(f'Main Category: {product.get('main_category', 'Unknown')}')
        print(f'Subcategory: {product.get('subcategory', 'Unknown')}')
        print(f'Prices: {product.get('discounted_price', 'N/A')}')