import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from qdrant_client import QdrantClient
from qdrant_client.models import PayloadSchemaType

from config.settings import QDRANT_COLLECTION_NAME

QDRANT_URL = 'http://localhost:6333'

def create_payload_indexes():

    client = QdrantClient(
        url=QDRANT_URL,
        timeout=300
    )

    fields = {
        'brand': PayloadSchemaType.KEYWORD,
        'main_category': PayloadSchemaType.KEYWORD,
        'subcategory': PayloadSchemaType.KEYWORD,
        'price': PayloadSchemaType.FLOAT,
        'rating': PayloadSchemaType.FLOAT,
        'dataset': PayloadSchemaType.KEYWORD
    }

    for field_name, field_schema in fields.items():

        print(f'Creating index for: {field_name}')

        client.create_payload_index(
            collection_name=QDRANT_COLLECTION_NAME,
            field_name=field_name,
            field_schema=field_schema
        )
    
    print('\nAll payload indexes created successfully.')

if __name__=='__main__':
    create_payload_indexes()