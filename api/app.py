from fastapi import FastAPI
from pydantic import BaseModel
from hybrid_search.search_hybrid import hybrid_search

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
                'score': round(score,4)
            }
        )
    
    return {
        'query': request.query,
        'results': formatted_results

    }