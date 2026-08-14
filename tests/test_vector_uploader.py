import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from vector_db.vector_uploader import VectorUploader

def main():
    uploader = VectorUploader()
    uploader.test()

    print()
    print('='*70)
    print('Vector Uploader Test Passed')
    print('='*70)

if __name__=='__main__':
    main()