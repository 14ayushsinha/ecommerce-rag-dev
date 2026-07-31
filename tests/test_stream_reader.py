import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from ingestion.downloader import AmazonDownloader
from ingestion.stream_reader import JSONLStreamReader

downloader = AmazonDownloader()

file_path = downloader.download(
    'meta_All_Beauty.jsonl'
)

print(file_path)

reader = JSONLStreamReader(file_path)

for i, product in enumerate(reader.stream()):
    print('='*80)
    print(product['title'])

    if i==4:
        break