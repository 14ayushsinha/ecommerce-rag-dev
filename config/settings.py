from pathlib import Path

# ==========================================================
# Project
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GENAI_ROOT = PROJECT_ROOT.parent

# ==========================================================
# Dataset
# ==========================================================

REPO_ID = "McAuley-Lab/Amazon-Reviews-2023"

DATASET_DIR = PROJECT_ROOT / "datasets"
RAW_DATA_DIR = DATASET_DIR / "raw"
PROCESSED_DATA_DIR = DATASET_DIR / "processed"

# ==========================================================
# Data
# ==========================================================

DATA_DIR = PROJECT_ROOT / "data"

# ==========================================================
# Embeddings
# ==========================================================

EMBEDDING_DIR = DATA_DIR / "embeddings"
VECTOR_DIR = EMBEDDING_DIR / "vectors"
METADATA_DIR = EMBEDDING_DIR / "metadata"
CHECKPOINT_DIR = EMBEDDING_DIR / "checkpoints"

# ==========================================================
# Shared Resources
# ==========================================================

HF_CACHE_DIR = GENAI_ROOT / "hf_cache"
QDRANT_STORAGE_DIR = GENAI_ROOT / "qdrant_storage"

# ==========================================================
# Constants
# ==========================================================

USD_TO_INR = 87.0

# ==========================================================
# Create Required Directories
# ==========================================================

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

DATA_DIR.mkdir(parents=True, exist_ok=True)

HF_CACHE_DIR.mkdir(parents=True, exist_ok=True)
QDRANT_STORAGE_DIR.mkdir(parents=True, exist_ok=True)

VECTOR_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DIR.mkdir(parents=True, exist_ok=True)
CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================================
# Embedding Configuration
# ==========================================================

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIMENSION = 384
EMBEDDING_GENERATION_BATCH_SIZE = 10000

# ==========================================================
# Qdrant Configuration
# ==========================================================

QDRANT_COLLECTION = "products"
UPLOAD_BATCH_SIZE = 5000

# ==========================================================
# Model Inference
# ==========================================================

MODEL_INFERENCE_BATCH_SIZE = 256