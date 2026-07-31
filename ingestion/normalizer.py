import re
from typing import Dict, Any
from ingestion.currency import convert_to_inr

class ProductNormalizer:
    """
    Normalizes cleaned products into a consistent schema.

    This module:
    - Standardizes text fields
    - Cleans brand/category names
    - Normalizes prices and ratings
    - Cleans specification keys
    """

    @staticmethod
    def normalize_text(text:str) -> str:

        if not text:
            return ""
        
        text = str(text)

        text = text.replace('\n', ' ')
        text = text.replace('\t', ' ')

        text = re.sub(r"\s+", " ", text)

        return text.strip()
    
    @staticmethod
    def normalize_price(price):

        price = convert_to_inr(price)

        if price is None:
            return None
        
        if isinstance(price, (int, float)):
            return float(price)
        
        price = str(price)

        price = price.replace('$', '')
        price = price.replace(',', '')
        price = price.strip()

        try:
            return float(price)
        except:
            return None
    
    @staticmethod
    def normalize_rating(rating):

        if rating is None:
            return None
        
        try:
            return float(rating)
        except:
            return None
    
    @staticmethod
    def normalize_specifications(specs: Dict[str, Any]):

        normalized = {}

        for key, value in specs.items():
            key = ProductNormalizer.normalize_text(key)
            value = ProductNormalizer.normalize_text(str(value))

            normalized[key] = value
        
        return normalized
    
    def build_search_text(slef, product):

        parts = [
            product["name"],
            product["brand"],
            product["main_category"],
            product["subcategory"],
            product["description"],
            product["features"],
            " ".join(
                f"{k} {v}"
                for k, v in product["specifications"].items()
            )
        ]

        return " ".join(
            part.strip()
            for part in parts
            if part
        )

    def normalize(self, product: Dict[str, Any]):

        normalized = {

            'id': product['id'],
            'name': self.normalize_text(product['name']),
            'brand': self.normalize_text(product['brand']).title(),
            'main_category': self.normalize_text(product['main_category']).title(),
            'subcategory': self.normalize_text(product['subcategory']),
            'price': self.normalize_price(product['price']),
            'currency': 'INR' if product['price'] is not None else None,
            'rating': self.normalize_rating(product['rating']),
            'rating_count': product['rating_count'],
            'description': self.normalize_text(product['description']),
            'features': self.normalize_text(product['features']),
            'specifications': self.normalize_specifications(product['specifications']),
            'image': product.get('image', ''),
            'source': 'amazon_reviews_2023'
        }

        normalized['search_text'] = self.build_search_text(normalized)

        return normalized
