import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import numpy as np
from vector_db.batch_writer import BatchWriter

def main():

    writer = BatchWriter()

    embeddings = np.random.rand(
        5,
        394,
    ).astype('float32')

    metadata = [
        {
            'id': str(1),
            'name': f'product {1}'
        }

        for i in range(5)
    ]

    writer.save(
        batch_number=1,
        embeddings=embeddings,
        metadata=metadata
    )

    print('\nBatch Writer Test Passed')

if __name__=='__main__':
    main()