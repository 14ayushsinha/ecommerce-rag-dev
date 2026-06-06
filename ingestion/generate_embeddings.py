import pandas as pd
import re
import json
import numpy as np
from sentence_transformers import SentenceTransformer

def clean_specifications(spec_text):
    if pd.isna(spec_text):
        return ""
    
    spec_text = str(spec_text)

    pairs = re.findall(r'"key"=>"([^"]+)".*?"value"=>"([^"]+)"', spec_text)

    return  "\n".join(
        f"{key}: {value}"
        for key, value in pairs
    )

def build_embedding_text(product):

    specs = clean_specifications(product['specifications'])

    return f"""
Product Name: {product['name']}
Brand: {product['brand']}
Category: {product['full_category_path']}

Description:
{product['description']}

Specifications:
{specs}
""".strip()

def main():

    print("\nLoading cleaned products...")

    df = pd.read_json("data/processed/products_clean.json")

    print(f"Loaded {len(df)} products")

    print("\nBuilding embedding texts...")

    texts = []

    for _, row in df.iterrows():
        text = build_embedding_text(row)
        texts.append(text)

    print(f"Built {len(texts)} embedding texts")
    print("\nLoading embedding model...")

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    print("\nGenerating embeddings...")

    embeddings = model.encode(
        texts,
        batch_size = 64,
        show_progress_bar = True,
        convert_to_numpy=True
    )

    print("\nEmbedding generation complete")
    print(f"Embedding shape {embeddings.shape}")
    print("\nSaving embeddings...")

    np.save("data/embeddings/product_embeddings.npy", embeddings)

    print("Saved product_embeddings.npy")
    print("\nSaving metadata...")

    metadata = df.to_dict(orient="records")

    with open(
        "data/embeddings/product_metadata.json",
        "w",
        encoding="utf-8"
    ) as f:
        
        json.dump(
            metadata,
            f,
            ensure_ascii=False,
            indent=2
        )

    print("Saved product_metadata.json")
    print("\nPipeline Complete!")

    print(f"Products Indexed: {len(df)}")
    print(f"Vector Dimension: {embeddings.shape[1]}")

if __name__ == "__main__":
    main()