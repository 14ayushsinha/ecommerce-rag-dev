import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from ingestion.downloader import AmazonDownloader
from ingestion.stream_reader import JSONLStreamReader
from ingestion.cleaner import ProductCleaner
from ingestion.normalizer import ProductNormalizer
from ingestion.validator import ProductValidator

downloader = AmazonDownloader()

file_path = downloader.download('meta_All_Beauty.jsonl')

reader = JSONLStreamReader(file_path)

cleaner = ProductCleaner()
normalizer = ProductNormalizer()

count=0
valid=0
invalid=0

for raw_product in reader.stream():
    cleaned = cleaner.clean(raw_product)
    normalized = normalizer.normalize(cleaned)

    if ProductValidator.validate(normalized):
        valid+=1
    
    else:
        invalid+=1
    
    count+=1

    if count==1000:
        break
    
print('='*60)
print(f'Checked: {count}')
print(f'Valid: {valid}')
print(f'Invalid: {invalid}')
print('='*60)
