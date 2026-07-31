import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from ingestion.pipeline import ProductPipeline

categories = [
    "All_Beauty",
    "Electronics",
    "Appliances",
    "Health_and_Personal_Care",
    "Amazon_Fashion"
    'Cell_Phones_and_Accessories'
]

for category in categories:
    ProductPipeline(category).run()