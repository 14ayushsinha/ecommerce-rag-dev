import os
import time
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import(Filter, FieldCondition, Range, MatchValue)

load_dotenv()

QDRANT_URL = os.getenv('QDRANT_URL')
QDRANT_API_KEY=os.getenv('QDRANT_API_KEY')

COLLECTION_NAME='products'

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def search_products(query, max_price=None, brand=None, category=None, limit=5):

    start = time.time()
    query_vector=model.encode(query).tolist()
    print("Embedding time:", time.time()-start)

    conditions=[]

    if max_price is not None:
        conditions.append(
            FieldCondition(
                key='discounted_price',
                range=Range(
                    lte=max_price
                )
            )
        )

    if brand:
        conditions.append(
            FieldCondition(
                key='brand',
                match=MatchValue(
                    value=brand
                )
            )
        )
    
    if category:
        conditions.append(
            FieldCondition(
                key='category',
                match=MatchValue(
                    value=category
                )
            )
        )

    search_filter = None

    if conditions:
        search_filter=Filter(
            must=conditions
        )

    start = time.time()
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=search_filter,
        limit=limit
    )
    print("Qdrant time:", time.time()-start)

    return results.points

if __name__ == '__main__':

    query = 'jewellery'
    results=search_products(query=query, brand='Voylla', max_price=2000)
    print(f'\nQuery: {query}\n')

    for i, result in enumerate(results, start=1):
        payload = result.payload
        print('='*80)

        print(f'Rank #{i}')
        print(f'Score: {result.score:.4f}')
        print(f'Name: {payload['name']}')
        print(f'Brand: {payload['brand']}')
        print(f'Category {payload['category']}')
        print(f'Full Category Path: {payload['full_category_path']}')
        print(f'Price: {payload['discounted_price']}/-')
        print(f"Price Type: {type(payload['discounted_price'])}")
        print(f"Rating Value: {payload['rating']}")
        print(f"Rating Type: {type(payload['rating'])}")

        print()