import json
import pickle
import numpy as np

with open('data/embeddings/product_metadata.json', 'r') as f:
    products = json.load(f)

with open('hybrid_search/bm25.pkl', 'rb') as f:
    bm25 = pickle.load(f)

query = input("Query: ")
tokens = query.lower().split()
scores = bm25.get_scores(tokens)
top_indices = np.argsort(scores)[::-1][:5]

for rank, idx in enumerate(top_indices, 1):
    product = products[idx]
    print('\n' + '='*80)
    print(f'Rank #{rank}')
    print("Score:", round(scores[idx],4))
    print("ID:", product["id"])
    print("Name:", product['name'])
    print("Brand", product['brand'])
    print("Main Category:", product['main_category'])
    print("Subcategory:", product['subcategory'])
    print("Price:", product['discounted_price'])