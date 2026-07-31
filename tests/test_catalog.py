# import sys
# from pathlib import Path
# ROOT_DIR = Path(__file__).resolve().parent.parent
# sys.path.append(str(ROOT_DIR))

# from utils.sqlite_catalog import ProductCatalog

# ProductCatalog().create_database()

import sqlite3

conn = sqlite3.connect("catalog/products.db")

cursor = conn.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='index'
""")

for row in cursor.fetchall():
    print(row[0])

conn.close()