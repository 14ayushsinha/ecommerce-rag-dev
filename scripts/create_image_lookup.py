import json
import pandas as pd
import ast
from ingestion.load_data import load_flipkart_dataset

print('Loading dataset...')

dataset = load_flipkart_dataset()
df = dataset['train'].to_pandas()

image_lookup = {}

for _, row in df.iterrows():
    product_id = row['uniq_id']
    images = row['image']

    if pd.notna(images):
        try:
            image_list = ast.literal_eval(images)

            if image_list:
                image_lookup[product_id] = image_list[0]
            
        except:
            pass

print(f'Images extracted: {len(image_lookup)}')

with open('data/images/image_lookup.json', 'w') as f:
    json.dump(image_lookup,f)

print('Saved to data/images/image_lookup..json')