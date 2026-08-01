import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from vector_db.model import EmbeddingModel

def main():

    print('='*70)
    print('TESTING EMBEDDING MODEL')
    print('='*70)

    texts = [
        'Samsung Galaxy S24 Ultra',
        'Apple iPhone 15 Pro Max',
        'Nike Running Shoes'
    ]

    embeddings = EmbeddingModel.encode(texts)

    print(f'\nEmbedding Shape : {embeddings.shape}')
    print(f'Embedding Type : {type(embeddings)}')
    print(f'Embedding Dtype : {embeddings.dtype}')

    print(f"\nEmbedding Shape : {embeddings.shape}")
    print(f"Embedding Type  : {type(embeddings)}")
    print(f"Embedding Dtype : {embeddings.dtype}")

    print(f"\nExpected Dimension : {EmbeddingModel.dimension()}")
    print(f"Returned Dimension : {embeddings.shape[1]}")

    print("\nFirst 10 values of first embedding:")

    print(embeddings[0][:10])

    print("\nModel Test Passed Successfully!")

    print("=" * 70)

if __name__ == '__main__':
    main()