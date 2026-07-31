import json
from pathlib import Path

from config.settings import PROCESSED_DATA_DIR

class DatasetMerger:
    
    def __init__(self):
        self.processed_dir = Path(PROCESSED_DATA_DIR)

        self.output_file = (
            self.processed_dir/'all_products.jsonl'
        )
    
    def merge(self):

        jsonl_files = sorted(self.processed_dir.glob('*.jsonl'))

        jsonl_files = [
            file
            for file in jsonl_files
            if file.name!='all_products.jsonl'
        ]

        unique_ids = set()

        total_read=0
        total_written=0
        duplicates=0

        with open(self.output_file, 'w', encoding='utf-8') as outfile:

            for file in jsonl_files:
                print(f'Merging: {file.name}')

                with open(file, 'r', encoding='utf-8') as infile:

                    for line in infile:

                        total_read+=1

                        product = json.loads(line)

                        product_id = product['id']

                        if product_id in unique_ids:
                            duplicates+=1
                            continue
                        
                        unique_ids.add(product_id)

                        product['dataset'] = file.stem

                        json.dump(
                            product,
                            outfile,
                            ensure_ascii=False
                        )

                        outfile.write('\n')

                        total_written+=1
        

        print('\n'+'='*65)
        print('DATASET MERGE COMPLETE')
        print('='*65)
        print(f'Files Processed: {len(jsonl_files)}')
        print(f'Products Read: {total_read:,}')
        print(f'Duplicates: {duplicates:,}')
        print(f'Products Saved: {total_written:,}')
        print(f'Output File: {self.output_file}')
        print('='*65)