from typing import Dict, Any

class ProductValidator:

    @staticmethod
    def validate(product: Dict[str, Any]) -> bool:
        """
        Returns True if product is valid.
        Returns False otherwise.
        """

        # ----------------------------
        # Mandatory fields
        # ----------------------------

        if not product.get('id'):
            return False, 'missing_id'
        
        if not product.get('name'):
            return False, 'missing_name'
        
        if not product.get('main_category'):
            return False, 'missing_main_category'
        
        if not product.get('search_text'):
            return False, 'missing_search_text'

        # ----------------------------
        # Rating Validation
        # ----------------------------
        
        rating = product.get('rating')

        if rating is not None:
            if not isinstance(rating, (int, float)):
                return False, 'invalid_rating'
            
            if rating<0 or rating >5:
                return False, 'invalid_rating'
        
        # ----------------------------
        # Rating Count
        # ----------------------------

        rating_count = product.get('rating_count')

        if rating_count is not None:
            if not isinstance(rating_count, int):
                return False, 'invalid_rating_count'
            
            if rating_count<0:
                return False, 'invalid_rating_count'
        
        # ----------------------------
        # Price Validation
        # ----------------------------

        price = product.get('price')

        if price is not None:
            if not isinstance(price, (int, float)):
                return False, 'invalid_price'
            
            if price<=0:
                return False, 'invalid_price'
        
        # ----------------------------
        # Currency
        # ----------------------------

        currency = product.get('currency')
        
        if price is not None and currency!='INR':
            return False, 'invalid_currency'
        
        # ----------------------------
        # Specifications
        # ----------------------------

        specs = product.get('specifications')

        if specs is None:
            return False, 'missing_specifications'
        
        if not isinstance(specs, dict):
            return False, 'missing_specifications'
        
        # ----------------------------
        # Image
        # ----------------------------

        image = product.get('image')

        if image:
            if not image.startswith('http'):
                return False, 'invalid_image_url'
        
        return True, 'valid'