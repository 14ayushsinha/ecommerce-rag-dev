import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import json
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from vector_db.upload_checkpoint_manager import UploadCheckPointManager

from config.settings import(
    VECTOR_DIR,
    METADATA_DIR,
    QDRANT_COLLECTION_NAME,
    READ_BATCH_SIZE
)

QDRANT_URL = 'http://localhost:6333'
QDRANT_UPLOAD_BATCH_SIZE = 500

class VectorUploader:

    def __init__(self):
        self.vector_dir = Path(VECTOR_DIR)
        self.metadata_dir = Path(METADATA_DIR)
        self.client = QdrantClient(url=QDRANT_URL, timeout=300)
        self.collection_name = QDRANT_COLLECTION_NAME
        self.upload_checkpoint = UploadCheckPointManager()
        self.read_batch_size = READ_BATCH_SIZE

    # --------------------------------------------------
    # Load vectors 
    # --------------------------------------------------

    def load_vectors(self, batch_number:int):
        vector_file = self.vector_dir/f'batch_{batch_number:06d}.npy'

        if not vector_file.exists():
            raise FileNotFoundError(
                f'Vector file not found: {vector_file}'
            )
        
        vectors = np.load(vector_file)
        return vectors
    
    # -------------------------------------------------- 
    # Load metadata 
    # --------------------------------------------------

    def load_metadata(self, batch_number:int):
        metadata_file = self.metadata_dir/f'batch_{batch_number:06d}.jsonl'

        if not metadata_file.exists():
            raise FileNotFoundError(
                f'Metadata file not found: {metadata_file}'
            )
        
        metadata = []

        with open(metadata_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                if line:
                    metadata.append(json.loads(line))
        
        return metadata

    
    # -------------------------------------------------- 
    # Validate Batch
    # --------------------------------------------------

    def validate_batch(self, vectors, metadata):

        print('\nValidating batch...')
        print(f'Vector Count: {len(vectors):,}')
        print(f'Metadata Count: {len(metadata):,}')
        print(f'Vector shape: {vectors.shape}')

        # -------------------------------------------------- 
        # Vector/metadata count
        # --------------------------------------------------
        if len(vectors)!=len(metadata):
            raise ValueError(
                'Vector count does not match metadata count.'
            )
        
        # -------------------------------------------------- 
        # Dimension
        # --------------------------------------------------
        if vectors.shape[1]!=384:
            raise ValueError(
                f'Expected vector dimension 384, got {vectors.shape[1]}'
            )
        
        print('Batch validation passed.')

    
    # -------------------------------------------------- 
    # Create Qdrant points
    # --------------------------------------------------
    
    def create_points(self, vectors, metadata, start_id: int=0):

        points = []

        for index, (vector, payload) in enumerate(zip(vectors, metadata)):
            point = PointStruct(
                id=start_id + index,
                vector=vector.tolist(),
                payload=payload
            )

            points.append(point)
        
        return points
    
    # -------------------------------------------------- 
    # Upload Batch
    # --------------------------------------------------

    def upload_batch(self, batch_number: int, start_id: int=0):

        checkpoint = self.upload_checkpoint.load()

        resume_batch = checkpoint['batch_number']
        resume_chunk = checkpoint['chunk_number']

        # ----------------------------------------------
        # Resume Logic
        # ----------------------------------------------
        if batch_number < resume_batch:
            print(f'Batch {batch_number:,} already completed. Skipping...')
            return
        
        if batch_number==resume_batch:
            start_chunk=resume_chunk
        
        else:
            start_chunk=0

        print()
        print('='*70)
        print(f'Uploading Batch: {batch_number:,}')
        print('='*70)

        # ---------------------------------------------- 
        # Load 
        # ----------------------------------------------
        vectors = self.load_vectors(batch_number)
        metadata = self.load_metadata(batch_number)

        # ---------------------------------------------- 
        # Validate
        # ----------------------------------------------
        self.validate_batch(vectors, metadata)

        # ---------------------------------------------- 
        # Create Points 
        # ----------------------------------------------
        print('\nCreating Qdrant points...')
        
        points = self.create_points(vectors, metadata, start_id=start_id)

        print(f'Points created: {len(points):,}')

        # ---------------------------------------------- 
        # Upload 
        # ----------------------------------------------
        print('\nUploading to Qdrant...')

        total_points = len(points)

        for chunk_start in range(0, total_points, QDRANT_UPLOAD_BATCH_SIZE):

            chunk_number = chunk_start//QDRANT_UPLOAD_BATCH_SIZE

            # ---------------------------------------------
            # Resume
            # ---------------------------------------------

            if chunk_number<start_chunk:
                continue

            chunk_end = min(chunk_start+QDRANT_UPLOAD_BATCH_SIZE, total_points)
            chunk = points[chunk_start:chunk_end]

            print(
                f'Uploading Batch {batch_number:,} '
                f'| Chunk {chunk_number:,} '
                f'| Points '
                f'{chunk_start:,}-'
                f'{chunk_end-1:,} '
                f'of {total_points:,}'
            )

            self.client.upsert(collection_name=self.collection_name, 
                points=chunk, 
                wait=True
            )

            # ---------------------------------------------
            # Save checkpoint
            # ---------------------------------------------
            self.upload_checkpoint.save(
                batch_number=batch_number,
                chunk_number=chunk_number+1
            )

        # ---------------------------------------------
        # Batch completed
        # ---------------------------------------------
        self.upload_checkpoint.save(
            batch_number=batch_number + 1,
            chunk_number=0
        )

        print('\nUpload completed successfully.')

        # ---------------------------------------------- 
        # Cleanup 
        # ----------------------------------------------

        del points
        del vectors
        del metadata
    
    # ---------------------------------------------- 
    # Full Batch Upload
    # ----------------------------------------------

    def upload_all(self):

        checkpoint = self.upload_checkpoint.load()
        start_batch = checkpoint['batch_number']

        total_batches = len(list(self.vector_dir.glob('batch_*.npy')))

        print()
        print('='*70)
        print('Starting Full Qdrant Upload')
        print('='*70)
        print(f'Total Batches: {total_batches:,}')
        print(f'Resuming from: Batch {start_batch:,}')
        print('='*70)

        for batch_number in range(start_batch, total_batches+1):
            start_id = (batch_number-1)*self.read_batch_size
            self.upload_batch(batch_number=batch_number, start_id=start_id)
        
        print()
        print('='*70)
        print('FULL QDRANT UPLOAD COMPLETED')
        print('='*70)

    # ---------------------------------------------- 
    # Test 
    # ----------------------------------------------

    def test(self):
        self.upload_batch(batch_number=3, start_id=30000)


if __name__=='__main__':
    uploader=VectorUploader()
    uploader.upload_all()