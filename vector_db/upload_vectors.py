import json
import os
import numpy as np
import time

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

COLLECTION_NAME = 'products'

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

def load_data():
    embeddings = np.load(
        'data/embeddings/product_embeddings.npy'
    )

    with open(
        'data/embeddings/product_metadata.json'
    ) as f:
        
        metadata = json.load(f)

    return embeddings,metadata

def create_points(embeddings, metadata):
    points=[]

    for idx, (vector,product) in enumerate(
        zip(embeddings, metadata)
    ):
        
        payload = {
            "product_id": product['id'],
            'name': product['name'],
            'brand': product['brand'],
            'category': product['main_category'],
            'subcategory': product['subcategory'],
            'full_category_path': product['full_category_path'],
            'retail_price': product['retail_price'],
            'discounted_price': product['discounted_price'],
            'rating': product['rating'],
            'description': product['description']
        }

        points.append(
            PointStruct(
                id=idx,
                vector=vector.tolist(),
                payload=payload
            )
        )

    return points

def upload_in_batches(points, batch_size=100):
    total_points=len(points)

    for start in range(0, total_points, batch_size):
        end=min(start+batch_size, total_points)

        batch = points[start:end]

        uploaded = False

        while not uploaded:
            try:
                client.upsert(
                    collection_name=COLLECTION_NAME,
                    points=batch
                )

                uploaded=True

                print(f'Uploaded {end}/{total_points}')
            
            except Exception as e:
                print(f'Retrying batch {start}-{end}')
                print(e)
                time.sleep(5)
    
def main():
    print('Loading embeddings...')

    embeddings,metadata = load_data()

    print(f'Embedding Shape: {embeddings.shape}')

    print('Creating points...')

    points = create_points(embeddings, metadata)

    print(f'Created {len(points)} points')

    print('Uploading to Qdrant...')

    upload_in_batches(points)

    print("\nUpload Complete!")

if __name__ == "__main__":
    main()