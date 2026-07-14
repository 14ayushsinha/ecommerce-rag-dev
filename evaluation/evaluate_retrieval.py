import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from hybrid_search.search_hybrid import hybrid_search

GROUND_TRUTH_FILE = 'evaluation/retrieval_ground_truth.json'

def precision_at_k(retrieved, relevant, k):
    retrieved = retrieved[:k]

    hits = sum(1 for  pid in retrieved if pid in relevant)

    return hits/k

def recall_at_k(retrieved, relevant, k):
    retrieved = retrieved[:k]

    hits = sum(1 for pid in retrieved if pid in relevant)

    if len(relevant) == 0:
        return 0
    
    return hits/len(relevant)

def hit_rate_at_k(retrieved, relevant, k):
    retrieved = retrieved[:k]

    for pid in retrieved:
        if pid in relevant:
            return 1
    
    return 0

def mrr(retrieved, relevant):
    for rank, pid in enumerate(retrieved, start=1):
        if pid in relevant:
            return 1/rank
    
    return 0

def evaluate():
    with open(GROUND_TRUTH_FILE, 'r') as f:
        dataset = json.load(f)
    
    precision5=0
    recall5=0
    hit5=0
    mrr_score=0

    precision10=0
    recall10=0
    hit10=0

    total = len(dataset)

    print("=" * 80)
    print('Running Retrieval Evaluation')
    print("=" * 80)

    for sample in dataset:
        query = sample['query']
        relevant = [name.strip().lower() for name in sample['relevant_products']]

        results, parsed = hybrid_search(
            query=query,
            limit=10
        )

        retrieved = [
            product['name'].strip().lower()
            for product, score in results
        ]

        precision5+=precision_at_k(retrieved, relevant, 5)
        recall5+=recall_at_k(retrieved, relevant, 5)
        hit5+=hit_rate_at_k(retrieved, relevant, 5)

        precision10+=precision_at_k(retrieved, relevant, 10)
        recall10+=recall_at_k(retrieved, relevant, 10)
        hit10+=hit_rate_at_k(retrieved, relevant, 10)

        mrr_score+=mrr(retrieved, relevant)

        metrics = {
            'Queries': total,

            'Precision@5': round(precision5/total, 3),
            'Recall@5': round(recall5/total, 3),
            'HitRate@5': round(hit5/total, 3),
           
            "Precision@10": round(precision10 / total, 3),
            "Recall@10": round(recall10 / total, 3),
            "HitRate@10": round(hit10 / total, 3),

            "MRR": round(mrr_score / total, 3),
        }

        print('\n')
        print('='*80)
        print('RESULTS')
        print('='*80)

        for key, value in metrics.items():
            print(f'{key:15}: {value}')
        
        with open('evaluation/retrieval_metrics.json', 'w') as f:
            json.dump(metrics, f, indent=4)
        
        print('\nSaved metrics to:')
        print('evaluation/retrieval_metrics.json')

if __name__ == '__main__':
    evaluate()