import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from ingestion.downloader import AmazonDownloader
from ingestion.stream_reader import JSONLStreamReader
from ingestion.cleaner import ProductCleaner

downloader = AmazonDownloader()

file_path = downloader.download('meta_All_Beauty.jsonl')

reader = JSONLStreamReader(file_path)

cleaner = ProductCleaner()

for i, product in enumerate(reader.stream()):

    cleaned = cleaner.clean(product)

    print('='*80)
    print(cleaned)

    if i==2:
        break