import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from ingestion.downloader import AmazonDownloader
from ingestion.stream_reader import JSONLStreamReader
from ingestion.cleaner import ProductCleaner
from ingestion.normalizer import ProductNormalizer

downloader = AmazonDownloader()

file_path = downloader.download('meta_All_Beauty.jsonl')

reader = JSONLStreamReader(file_path)

cleaner = ProductCleaner()

normalizer = ProductNormalizer()

count = 0

for product in reader.stream():

    cleaned = cleaner.clean(product)
    normalized = normalizer.normalize(cleaned)

    if normalized["price"] is not None:

        print("=" * 80)
        print(normalized)

        count += 1

    if count == 5:
        break