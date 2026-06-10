from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import PayloadSchemaType

import os

load_dotenv()

client = QdrantClient(
    url=os.getenv('QDRANT_URL'),
    api_key=os.getenv('QDRANT_API_KEY')
)

COLLECTION_NAME='products'

#Price
client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name='discounted_price',
    field_schema=PayloadSchemaType.INTEGER
)

#Rating
client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name='rating',
    field_schema=PayloadSchemaType.FLOAT
)

#Category
client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name='category',
    field_schema=PayloadSchemaType.KEYWORD
)

#Brand
client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name='brand',
    field_schema=PayloadSchemaType.KEYWORD
)

print('Payload indexes created successfully!')