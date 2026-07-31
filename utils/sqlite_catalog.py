import json
import sqlite3
from pathlib import Path

from config.settings import PROCESSED_DATA_DIR

class ProductCatalog:

    def __init__(self):

        self.input_file = Path(PROCESSED_DATA_DIR)/'all_products.jsonl'

        self.catalog_dir = Path('catalog')
        self.catalog_dir.mkdir(exist_ok=True)
        
        self.db_path = self.catalog_dir/'products.db'
    
    def create_database(self):

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DROP TABLE IF EXISTS products')

        cursor.execute("""
        CREATE TABLE products(
            id TEXT PRIMARY KEY,
            name TEXT,
            brand TEXT,
            main_category TEXT,
            sub_category TEXT,
            dataset TEXT,
            price REAL,
            currency TEXT,
            rating REAL,
            rating_count INTEGER,
            image TEXT,
            search_text TEXT
        )
        """)

        conn.commit()

        total=0

        with open(self.input_file, 'r', encoding='utf-8') as f:

            for line in f:

                product = json.loads(line)

                cursor.execute("""
                INSERT INTO products VALUES
                (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                """, (
                    product["id"],
                    product["name"],
                    product["brand"],
                    product["main_category"],
                    product["subcategory"],
                    product["dataset"],
                    product["price"],
                    product["currency"],
                    product["rating"],
                    product["rating_count"],
                    product["image"],
                    product["search_text"]
                ))

                total+=1

                if total%10000==0:
                    conn.commit()

                    print(f'Inserted: {total:,}')
        
        print('\nCreating Indexes...')

        cursor.execute(
            'CREATE INDEX IF NOT EXISTS idx_brand ON products(brand)'
        )

        cursor.execute(
            'CREATE INDEX IF NOT EXISTS idx_category ON products(main_category)'
        )

        cursor.execute(
            'CREATE INDEX IF NOT EXISTS idx_dataset ON products(dataset)'
        )

        cursor.execute(
            'CREATE INDEX IF NOT EXISTS idx_price ON products(price)'
        )

        cursor.execute(
            'CREATE INDEX IF NOT EXISTS idx_rating ON products(rating)'
        )

        conn.commit()

        print('\n'+'='*65)
        print('SQLITE CATALOG CREATED')
        print('='*65)
        print(f'Products: {total:,}')
        print(f'Database: {self.db_path}')
        print('='*65)

        conn.close()