import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from config.categories import CATEGORIES
from ingestion.downloader import AmazonDownloader
from ingestion.stream_reader import JSONLStreamReader

def main():

    downloader = AmazonDownloader()

    for category in CATEGORIES:
        print('='*80)
        print(f'Processing {category['name']}')
        print('='*80)

        file_path = downloader.download(category['file'])
        print(f'Download to: {file_path}')

        reader = JSONLStreamReader(file_path)

        count = 0

        for product in reader.stream():
            count += 1

            if count <= 5:
                print(product["title"])

        print(f"\nTotal streamed: {count}")

if __name__ == '__main__':
    main()