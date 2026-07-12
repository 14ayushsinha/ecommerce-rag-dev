from sentence_transformers import CrossEncoder

print('Loading Cross Encoder...')

cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L6-v2')

print('Cross Encoder Loaded')

def rerank_results(query, results, top_k=10):
    
    if len(results)<=1:
        return results
    
    candidates = results[:top_k]
    remaining = results[top_k:]

    sentence_pairs = []

    for product, _ in candidates:

        text = (
            f'{product.get('name', '')}. '
            f'{product.get('brand', '')}. '
            f'{product.get('main_category', '')}. '
            f'{product.get('subcategory', '')}. '
            f'{product.get('description', '')}'

        )

        sentence_pairs.append((query, text))

    scores = cross_encoder.predict(sentence_pairs)

    reranked = []

    for (product, _), score in zip(candidates, scores):
        reranked.append((product, float(score)))

    reranked.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return reranked+remaining