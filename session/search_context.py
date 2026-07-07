class SearchContext:

    def __init__(self):
        self.reset()
    
    def reset(self):
        self.query = None

        self.brand = None
        self.category = None

        self.min_price = None
        self.max_price = None

        self.limit = 5
    
    def update(self, parsed_query):
        if parsed_query.get('query'):
            self.query = parsed_query['query']
        
        if parsed_query.get('brand'):
            self.brand = parsed_query['brand']
        
        if parsed_query.get('category')    :
            self.category = parsed_query['category']
        
        if parsed_query.get('min_price') is not None:
            self.min_price = parsed_query['min_price']
        
        if parsed_query.get('max_price') is not None:
            self.max_price = parsed_query['max_price']
    
    def to_dict(self):
        return {
            'query': self.query,
            'brand': self.brand,
            'category': self.category,
            'min_price': self.min_price,
            'max_price': self.max_price,
            'limit': self.limit
        }