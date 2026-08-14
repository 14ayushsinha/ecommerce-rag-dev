import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from config.settings import QDRANT_COLLECTION_NAME

QDRANT_URL = 'http://localhost:6333'

def create_collection():

    client = QdrantClient(
        url=QDRANT_URL
    )

    # Check if collection already exists

    collections = client.get_collections()

    existing_names = [
        collection.name
        for collection in collections.collections
    ]

    if QDRANT_COLLECTION_NAME in existing_names:

        print(
            f"Collection '{QDRANT_COLLECTION_NAME}' "
            f'already exists.'
        )

    # Create Collection

    client.create_collection(
        collection_name=QDRANT_COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

    print(
        f"Collection '{QDRANT_COLLECTION_NAME}' "
        f'created successfully.'
    )

if __name__=='__main__':
    create_collection()