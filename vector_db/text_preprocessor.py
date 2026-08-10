import re
from config.settings import (
    MAX_EMBEDDING_CHARACTERS,
    MAX_DESCRIPTION_CHARS,
    MAX_SPECIFICATION_CHARS
)

class TextPreprocessor:

    @staticmethod
    def prepare(product: dict) -> str:

        sections = []

        # ----------------------------
        # Name
        # ----------------------------

        if product.get('name'):
            sections.append(f'Product: {product['name']}')

        # ----------------------------
        # Brand
        # ----------------------------

        if product.get('brand'):
            sections.append(f'Brand: {product['brand']}')
        
        # ----------------------------
        # Category
        # ----------------------------

        if product.get('main_category'):
            sections.append(f'Category: {product['main_category']}')

        if product.get('subcategory'):
            sections.append(f'Subcategory: {product['subcategory']}')
        
        # ----------------------------
        # Price
        # ----------------------------

        if product.get('price'):
            sections.append(f'Price: {product['price']} {product.get('currency', '')}')
        
        # ----------------------------
        # Description
        # ----------------------------

        description = product.get('description')
        if description:
            sections.append('Description:\n' + description[:MAX_DESCRIPTION_CHARS])
        
        # ----------------------------
        # Specifications
        # ----------------------------

        specs = product.get('specifications')

        if isinstance(specs, dict):
            spec_lines=[]
            curr_length=0
            
            for key, value in specs.items():
                if not value:
                    continue
                
                line = f'{key}: {value}'

                if (curr_length+len(line)>MAX_SPECIFICATION_CHARS):
                    break
                
                spec_lines.append(line)
                curr_length+=len(line)+1

            
            if spec_lines:
                sections.append('Specifications:\n'+ '\n'.join(spec_lines))
            
        
        # ----------------------------
        # Join
        # ----------------------------

        text = '\n\n'.join(sections)

        # ----------------------------
        # Remove Excessive WhiteSpace
        # ----------------------------

        # Collapse multiple spaces/tabs but preserve newlines
        text = re.sub(r"[ \t]+", " ", text)

        # Collapse excessive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        text = text.strip()

        # ----------------------------
        # Length Limit
        # ----------------------------

        if len(text)>MAX_EMBEDDING_CHARACTERS:

            cutoff = text.rfind(" ", 0, MAX_EMBEDDING_CHARACTERS)

            if cutoff==-1:
                cutoff=MAX_EMBEDDING_CHARACTERS

            text=text[:cutoff]

        return text