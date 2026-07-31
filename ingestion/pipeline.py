import time

from config.settings import PROCESSED_DATA_DIR
from ingestion.downloader import AmazonDownloader
from ingestion.stream_reader import JSONLStreamReader
from ingestion.cleaner import ProductCleaner
from ingestion.normalizer import ProductNormalizer
from ingestion.validator import ProductValidator
from ingestion.writer import ProductWriter

from collections import defaultdict

class ProductPipeline:

    def __init__(self, category: str):
        self.downloader = AmazonDownloader()
        self.category = category
        file_path = self.downloader.download(f'meta_{category}.jsonl')
        self.reader = JSONLStreamReader(file_path)
        self.cleaner = ProductCleaner()
        self.normalizer = ProductNormalizer()
        self.validator = ProductValidator()
    
    def run(self):
        output_file = f'{PROCESSED_DATA_DIR}/{self.category.lower()}.jsonl'

        rejection_counter = defaultdict(int)


        processed=0
        written=0
        rejected=0

        start = time.time()

        with ProductWriter(output_file) as writer:
            
            for raw_products in self.reader.stream():
                processed+=1
                cleaned = self.cleaner.clean(raw_products)
                normalized = self.normalizer.normalize(cleaned)

                valid, reason = self.validator.validate(normalized)

                if valid:
                    writer.write(normalized)
                    written+=1
                
                else:
                    rejected+=1
                    rejection_counter[reason]+=1
                
                if processed%10000==0:
                    print(
                        f'Processed: {processed:,} | '
                        f'Written: {written:,}'
                    )
        
        end = time.time()

        print('\n'+'='*70)
        print('PIPELINE COMPLETE')
        print('='*70)
        print(f'Category        : {self.category}')
        print(f'Processed       : {processed:,}')
        print(f'Written         : {written}')
        print(f'Rejected        : {rejected:,}')

        print('\nRejected Reasons')
        for reason, count in rejection_counter.items():
            print(f'{reason:<25} {count}')
            
        print(f'Output File     : {output_file}')
        print(f'Time Taken      : {end-start:.2f} sec')
        print('='*70)