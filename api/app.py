import json
from fastapi import FastAPI
from pydantic import BaseModel
from hybrid_search.search_hybrid import hybrid_search
from llm.recommender import generate_recommendation

app = FastAPI(
    title = 'E-Commerce Product Search API',
    description = 'Hybrid search using BM25 + Vector Search',
    version = '1.0.0'
)

class SearchRequest(BaseModel):
    query: str
    limit: int = 5

@app.get('/')
def home():
    return {
        'message': 'E-Commerce Product Search API is running'
    }

@app.post('/search')
def search(request: SearchRequest):

    with open('data/images/image_lookup.json', 'r') as f:
        image_lookup = json.load(f)

    results = hybrid_search(
        query=request.query,
        limit=request.limit
    )

    formatted_results = []

    for product, score in results:
        
        formatted_results.append(
            {
                'id': product['id'],
                'name': product['name'],
                'brand': product['brand'],
                'category': product.get('main_category'),
                'subcategory': product.get('subcategory'),
                'price': product.get('discounted_price'),
                'image': image_lookup.get(product['id']),
                'score': round(score,4)
            }
        )

        summary = generate_recommendation(
            request.query,
            formatted_results
        )
    
    return {
        'query': request.query,
        'summary': summary,
        'results': formatted_results

    }