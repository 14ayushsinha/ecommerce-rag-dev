import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from vector_db.embedding_generator import EmbeddingGenerator

def main():
    generator = EmbeddingGenerator()
    generator.generate()

if __name__=='__main__':
    main()