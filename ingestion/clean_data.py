import pandas as pd
from load_data import load_flipkart_dataset

def clean_rating(value):
    """
    Convert ratings to float.
    Return None if rating is unavailable.
    """

    if pd.isna(value):
        return None
    
    value = str(value).strip()

    if value.lower()=="no rating available":
        return None
    
    try:
        return float(value)
    except ValueError:
        return None

def clean_brand(value):
    """
    Fill missing brands.
    """

    if pd.isna(value):
        return "Unknown"
    
    value = str(value).strip()

    return value if value else "Unknown"

def extract_categories(category_tree):
    """
    Extract:
    - main_category
    - subcategory
    - full_category_path
    """

    if pd.isna(category_tree):
        return {
            "main_category": "Unknown",
            "subcategory": "Unknown",
            "full_category_path": ""
        }

    category_tree = str(category_tree)

    # Remove dataset wrappers
    category_tree = category_tree.replace('["', '')
    category_tree = category_tree.replace('"]', '')

    parts = [part.strip() for part in category_tree.split(">>")]

    main_category = parts[0] if len(parts) > 0 else "Unknown"

    subcategory = parts[1] if len(parts) > 1 else "Unknown"

    return {
        "main_category": main_category,
        "subcategory": subcategory,
        "full_category_path": category_tree
    }

def build_clean_product(row):
    """
    Convert raw dataset row into normalized product document.
    """

    category_data = extract_categories(
        row["product_category_tree"]
    )

    return {
        "id": row["uniq_id"],

        "name": row["product_name"],

        "brand": clean_brand(
            row["brand"]
        ),

        "main_category": category_data["main_category"],

        "subcategory": category_data["subcategory"],

        "full_category_path":
            category_data["full_category_path"],

        "retail_price":
            float(row["retail_price"]),

        "discounted_price":
            float(row["discounted_price"])
            if pd.notna(row["discounted_price"])
            else float(row["retail_price"]),

        "rating":
            clean_rating(
                row["product_rating"]
            ),

        "description":
            str(row["description"])
            if pd.notna(row["description"])
            else "",

        "specifications":
            str(row["product_specifications"])
            if pd.notna(row["product_specifications"])
            else ""
    }

def main():

    dataset = load_flipkart_dataset()

    df = dataset['train'].to_pandas()

    # Drop Product without retail price
    df = df.dropna(subset=['retail_price'])

    cleaned_products = []

    for _, row in df.iterrows():

        cleaned_product = build_clean_product(row)
        cleaned_products.append(cleaned_product)

        cleaned_df = pd.DataFrame(cleaned_products)
        print(cleaned_df.head())

        print(
            f"\nTotal cleaned products: "
            f"{len(cleaned_df)}"
        )

        #Save locally
        cleaned_df.to_json(r"C:\Users\Ayush Sinha\Desktop\Ecommerce Prod Recom\data\processed\products_clean.json",
                           orient="records", indent=2)

if __name__ == "__main__":
    main()
