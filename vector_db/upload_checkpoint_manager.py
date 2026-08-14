import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import json
from datetime import datetime
from config.settings import CHECKPOINT_DIR

class UploadCheckPointManager:
    """
    Handles checkpointing for the Qdrant vector upload process.

    Checkpoint format:

    {
        "batch_number": 12,
        "chunk_number": 7,
        "updated_at": "..."
    }

    Meaning:
        Batch 12 is currently being uploaded.
        Chunks 0-6 are already completed.
        Resume from chunk 7.
    """

    def __init__(self):
        self.checkpoint_file = Path(CHECKPOINT_DIR)/'qdrant_upload_checkpoint.json'
        self.checkpoint_file.parent.mkdir(parents=True, exist_ok=True)

    
    # --------------------------------------------------
    # Load
    # --------------------------------------------------

    def load(self):
        """
        Load the latest upload checkpoint.
        Returns:
            dict
        """
        
        if not self.checkpoint_file.exists():
            return {
                'batch_number': 1,
                'chunk_number': 0
            }
        
        with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
            checkpoint = json.load(f)
        
        print(
            f'\nResuming Qdrant from '
            f'Batch {checkpoint['batch_number']:,} '
            f'Chunk {checkpoint['chunk_number']:,}'
        )

        return checkpoint

    # --------------------------------------------------
    # Save
    # --------------------------------------------------

    def save(self, batch_number: int, chunk_number: int):
        """
        Save upload progress.

        chunk_number represents the NEXT chunk
        that needs to be uploaded.
        """

        checkpoint = {
            'batch_number': batch_number,
            'chunk_number': chunk_number,
            'updated_at': datetime.now().isoformat()
        }

        with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, indent=4)
    
    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    def reset(self):
        """
        Delete the upload checkpoint.
        """

        if self.checkpoint_file.exists():
            self.checkpoint_file.unlink()

            print('Qdrant upload checkpoint removed.')