import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from vector_db.checkpoint_manager import CheckpointManager

def main():

    checkpoint = CheckpointManager()

    print('Current checkpoint:')
    print(checkpoint.load())

    checkpoint.save(123456)

    print('\nSaved checkpoint.')
    print('\nReloading...')

    print(checkpoint.load())
    checkpoint.reset()


if __name__=='__main__':
    main()