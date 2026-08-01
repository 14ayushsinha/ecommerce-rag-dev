import json
from pathlib import Path
from datetime import datetime

from config.settings import CHECKPOINT_DIR

class CheckpointManager:
    """
    Handles saving and loading embedding pipeline checkpoints.
    """

    def __init__(self):
        
        self.checkpoint_file = Path(CHECKPOINT_DIR)/'embedding_checkpoint.json'

    def load(self):
        """
        Load checkpoint if it exists.

        Returns:
            int : Product index to resume from.
        """

        if not self.checkpoint_file.exists():
            return 0
        
        with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
            checkpoint=json.load(f)

        print(
            f'\nResuming from product '
            f'{checkpoint['last_processed']:,}'
        )

        return checkpoint['last_processed']
    
    def save(self, last_processed: int):
        """
        Save current progress.
        """

        checkpoint = {
            'last_processed': last_processed,
            'updated_at': datetime.now().isoformat()
        }

        with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, indent=4)
    
    def reset(self):
        """
        Delete checkpoint.
        """

        if self.checkpoint_file.exists():
            self.checkpoint_file.unlink()
            print('Checkpoint removed.')