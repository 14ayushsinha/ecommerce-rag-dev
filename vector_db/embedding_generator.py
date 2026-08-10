from pathlib import Path

from config.settings import(
    PROCESSED_DATA_DIR,
    READ_BATCH_SIZE,
    MODEL_INFERENCE_BATCH_SIZE
)

from ingestion.stream_reader import JSONLStreamReader

from vector_db.checkpoint_manager import CheckpointManager
from vector_db.text_preprocessor import TextPreprocessor
from vector_db.model import EmbeddingModel
from vector_db.batch_writer import BatchWriter

class EmbeddingGenerator:

    def __init__(self):
        self.input_file = Path(PROCESSED_DATA_DIR)/'all_products.jsonl'
        self.reader = JSONLStreamReader(self.input_file)
        self.checkpoint = CheckpointManager()
        self.read_batch_size = READ_BATCH_SIZE
        self.embedding_model = EmbeddingModel()
        self.model_inference_batch_size = MODEL_INFERENCE_BATCH_SIZE
        self.writer = BatchWriter()
    
    def generate(self):
        resume_index = self.checkpoint.load()

        current_index=0

        texts=[]
        metadata=[]

        # ----------------------------------
        # Resume Information
        # ----------------------------------

        if resume_index > 0:
            print()
            print("=" * 70)
            print(f"Resuming from product : {resume_index:,}")
            print(
                f"Starting batch        : "
                f"{(resume_index // self.read_batch_size) + 1:,}"
            )
            print("=" * 70)

        for product in self.reader.stream():

            # ----------------------------------
            # Resume
            # ----------------------------------
            if current_index<resume_index:
                current_index+=1
                continue
            
            # ----------------------------------
            # Prepare Embedding text
            # ----------------------------------
            embedding_text = TextPreprocessor.prepare(product)
            texts.append(embedding_text)
            metadata.append(product)
            current_index+=1

            # ----------------------------------
            # Batch Ready
            # ----------------------------------
            if len(texts)==self.read_batch_size:

                batch_number = current_index // self.read_batch_size

                print()
                print('='*70)
                print(f'Batch : {batch_number:,}')
                print(f'Products : {len(texts):,}')
                print(f'Processed : {current_index:,}')
                print()

                print('First Product:')
                print(metadata[0]['name'])
                print()
                
                print('Embedding Text Preview:')
                print(texts[0][:300])
                print('='*70)

                embeddings = self.embedding_model.encode(texts, batch_size=self.model_inference_batch_size)

                try:

                    vector_file, metadata_file = self.writer.save(
                        batch_number=batch_number,
                        embeddings=embeddings,
                        metadata=metadata
                    )

                    self.checkpoint.save(current_index)
                
                except Exception:
                    raise

                print()
                print(f'Embedding Shape : {embeddings.shape}')
                print(f'Vectors Saved : {vector_file.name}')
                print(f'Metadata Saved : {metadata_file.name}')
                print(f'Checkpoint : {current_index:,}')

                texts.clear()
                metadata.clear()
                
                del embeddings
        
        # ----------------------------------
        # Remaining products
        # ----------------------------------
        if texts:

            batch_number = (
                current_index // self.read_batch_size
                if current_index % self.read_batch_size == 0
                else (current_index // self.read_batch_size) + 1
            )

            embeddings = self.embedding_model.encode(
                texts,
                batch_size=self.model_inference_batch_size
            )

            vector_file, metadata_file = self.writer.save(
                batch_number=batch_number,
                embeddings=embeddings,
                metadata=metadata
            )
            

            self.checkpoint.save(current_index)

            print()
            print('='*70)
            print(f'Final Batch : {batch_number}')
            print(f'Products : {len(texts):,}')
            print(f'Vectors Saved : {vector_file.name}')
            print(f'Metadata Saved : {metadata_file.name}')
            print(f'Checkpoint : {current_index}')
            print('='*70)