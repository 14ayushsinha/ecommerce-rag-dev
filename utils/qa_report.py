import sqlite3
from pathlib import Path

class QAReport:

    def __init__(self, db_path='catalog/products.db'):
        self.db_path = Path(db_path)
    
    def query(self, sql):

        cursor = self.conn.cursor()
        cursor.execute(sql)

        return cursor.fetchall()
    
    def generate(self):

        self.conn = sqlite3.connect(self.db_path)

        print('\n'+'='*70)
        print('PRODUCT DATA QUALITY REPORT')
        print('='*70)

        # ---------------------------------------------------------
        # Total Products
        # ---------------------------------------------------------

        total = self.query(
            'SELECT COUNT(*) FROM products'
        )[0][0]

        print(f'\nTotal Products: {total:,}')

        # ---------------------------------------------------------
        # Dataset Distribution
        # ---------------------------------------------------------

        print('\nDataset Distribution')
        print('-'*80)

        rows = self.query("""
        SELECT dataset,
        COUNT(*)
        FROM products
        GROUP BY dataset
        ORDER BY COUNT(*) DESC
        """)

        for dataset, count in rows:
            print(f'{dataset:<35} {count:,}')

        # ---------------------------------------------------------
        # Category Distribution
        # ---------------------------------------------------------

        print('\nCategory Distribution')
        print('-'*40)

        rows = self.query("""
        SELECT main_category,
        COUNT(*)
        FROM products
        GROUP BY main_category
        ORDER BY COUNT(*) DESC
        """)

        for category, count in rows:
            print(f'{category:<35} {count:,}')

        # ---------------------------------------------------------
        # Missing Values
        # ---------------------------------------------------------

        print('\nMissing Values')
        print('-'*40)

        checks = {
             "Brand":
            """
            SELECT COUNT(*)
            FROM products
            WHERE brand=''
            """,

            "Price":
            """
            SELECT COUNT(*)
            FROM products
            WHERE price IS NULL
            """,

            "Rating":
            """
            SELECT COUNT(*)
            FROM products
            WHERE rating IS NULL
            """,

            "Image":
            """
            SELECT COUNT(*)
            FROM products
            WHERE image=''
            """,

            "Search Text":
            """
            SELECT COUNT(*)
            FROM products
            WHERE search_text=''
            """
        }

        for name, sql in checks.items():

            count = self.query(sql)[0][0]
            print(f'{name:<20} {count:,}')
        
        # ---------------------------------------------------------
        # Price Statistics
        # ---------------------------------------------------------

        print('\nPrice Statistics')
        print('-'*40)

        stats = self.query("""
        SELECT
            MIN(price),
            MAX(price),
            AVG(price)
        FROM products
        WHERE price IS NOT NULL
        """)[0]

        print(f"Minimum Price : ₹{stats[0]:,.2f}")
        print(f"Maximum Price : ₹{stats[1]:,.2f}")
        print(f"Average Price : ₹{stats[2]:,.2f}")

        # ---------------------------------------------------------
        # Rating Statistics
        # ---------------------------------------------------------

        print('\nRating Statistics')
        print('-'*40)

        stats = self.query("""
        SELECT
            MIN(rating),
            MAX(rating),
            AVG(rating)
        FROM products
        WHERE rating IS NOT NULL
        """)[0]

        print(f'Minimum Rating : {stats[0]:.2f}')
        print(f'Maximum Rating : {stats[1]:.2f}')
        print(f'Average Rating : {stats[2]:.2f}')

        # ---------------------------------------------------------
        # Top Brands
        # ---------------------------------------------------------

        print('\nTop 20 Brands')
        print('-'*40)

        rows = self.query("""
        SELECT
            brand,
            COUNT(*)
        FROM products
        WHERE brand!=''
        GROUP BY brand
        ORDER BY COUNT(*) DESC
        LIMIT 20
        """)

        for brand, count in rows:
            print(f'{brand:<30} {count:,}')
        
        # ---------------------------------------------------------
        # Search Text Length
        # ---------------------------------------------------------

        print('\nSearch Text Statistics')
        print('-'*40)

        stats = self.query("""
        SELECT
            MIN(LENGTH(search_text)),
            MAX(LENGTH(search_text)),
            AVG(LENGTH(search_text))
        FROM products
        """)[0]

        print(f'Minimum Length : {stats[0]}')
        print(f'Maximum Length : {stats[1]}')
        print(f'Average Length : {stats[2]:.2f}')

        # ---------------------------------------------------------
        # Duplicate Check
        # ---------------------------------------------------------

        print('\nDuplicate IDs')
        print('-'*40)

        duplicates = self.query("""
        SELECT COUNT(*)
        FROM (
            SELECT id
            FROM products
            GROUP BY id
            HAVING COUNT(*)>1
        )
        """)[0][0]

        print(f'Duplicate IDs : {duplicates}')

        self.conn.close()

        print('\n'+'='*70)
        print('REPORT COMPLETE')
        print('='*70)