from typing import Dict, Any

class ProductCleaner:

    """
    Converts raw Amazon metadata into a
    canonical product schema.
    """

    def clean(self, product: Dict[str, Any]) -> Dict[str, Any]:

        images = product.get('images', [])

        image = ''

        if images:
            first = images[0]

            image = (
                first.get('hi_res')
                or first.get('large')
                or first.get('thumb')
                or ''
            )
        
        description = ' '.join(
            product.get('description', [])
        ).strip()

        features = " ".join(
            product.get('features', [])
        ).strip()

        categories = product.get("categories", [])

        subcategory = " > ".join(categories)

        cleaned = {

            'id': product.get('parent_asin'),
            'name': product.get('title', '').strip(),
            'brand': product.get('store') or "",
            'main_category': product.get('main_category') or "",
            'subcategory': subcategory,
            'price': product.get('price'),
            'rating': product.get('average_rating'),
            'rating_count': product.get('rating_number', 0),
            'description': description,
            'features': features,
            'specifications': product.get('details', {}),
            'image': image
        }

        return cleaned