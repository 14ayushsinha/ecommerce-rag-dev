import json
from pathlib import Path

import numpy as np

from config.settings import(
    VECTOR_DIR,
    METADATA_DIR
)

class BatchWriter:
    """
    Saves embedding batches and metadata batches.

    Output:

    vectors/
        batch_000001.npy

    metadata/
        batch_000001.npy
    """

    def __init__(self):

        self.vector_dir = Path(VECTOR_DIR)
        self.metadata_dir = Path(METADATA_DIR)
    
    def save(self, batch_number: int, embeddings: np.ndarray, metadata: list):

        filename = f'batch_{batch_number:06d}'

        vector_file = (
            self.vector_dir/
            f'{filename}.npy'
        )

        metadata_file = (
            self.metadata_dir/
            f'{filename}.jsonl'
        )

        # -----------------------------
        # Save vectors
        # -----------------------------

        np.save(
            vector_file,
            embeddings
        )

        # -----------------------------
        # Save metadata
        # -----------------------------

        with open(metadata_file, 'w', encoding='utf-8') as f:

            for product in metadata:
                json.dump(product, f, ensure_ascii=False)
                f.write('\n')
        
        return vector_file, metadata_file