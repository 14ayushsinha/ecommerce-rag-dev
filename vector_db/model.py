from sentence_transformers import SentenceTransformer
import torch

from config.settings import(
    EMBEDDING_MODEL,
    EMBEDDING_DIMENSION,
    MODEL_INFERENCE_BATCH_SIZE
)

class EmbeddingModel:
    """
    Singleton wrapper around the SentenceTransformer model.

    Responsible for:
    - Loading the embedding model once
    - Device selection (GPU/CPU)
    - Encoding text into normalized embeddings
    """

    _model = None

    @classmethod
    def load(cls):
        """
        Load the embedding model only once.
        """

        if cls._model is None:

            device = (
                'cuda'
                if torch.cuda.is_available()
                else 'cpu'
            )

            print(f'\nLoading embedding model...')
            print(f'Model : {EMBEDDING_MODEL}')
            print(f'Device : {device}')

            cls._model = SentenceTransformer(
                EMBEDDING_MODEL,
                device=device
            )

            print('Embedding model loaded successfully.\n')
        
        return cls._model
    
    @classmethod
    def encode(cls, texts, batch_size=MODEL_INFERENCE_BATCH_SIZE):

        """
        Generate normalized embeddings.

        Parameters
        ---------
        texts : list[str]
        batch_size : int

        Returns
        -------
        numpy.ndarray
        """

        model = cls.load()

        embeddings = model.encode(
            texts,
            batch_size=MODEL_INFERENCE_BATCH_SIZE,
            show_progress_bar=False,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        return embeddings
    
    @staticmethod
    def dimension():
        return EMBEDDING_DIMENSION