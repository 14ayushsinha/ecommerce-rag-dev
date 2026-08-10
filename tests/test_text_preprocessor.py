import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from vector_db.text_preprocessor import TextPreprocessor

sample = {
    "name": "Samsung Galaxy S24 Ultra",

    "brand": "Samsung",

    "main_category": "Electronics",

    "subcategory": "Smartphones",

    "price": 129999,

    "currency": "INR",

    "description": (
        "Samsung Galaxy S24 Ultra features a Snapdragon processor, "
        "excellent battery life, AI camera features, premium build quality, "
        "and Gorilla Glass protection. "
    ) * 50,

    "specifications": {

        "RAM": "12 GB",

        "Storage": "512 GB",

        "Display": "6.8 AMOLED",

        "Camera": "200 MP"

    }
}

text = TextPreprocessor.prepare(sample)

print(len(text))
print()
print(text)