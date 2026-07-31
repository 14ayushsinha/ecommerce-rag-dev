from pathlib import Path

#REPO_ID
REPO_ID = "McAuley-Lab/Amazon-Reviews-2023"

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Dataset Directories
DATASET_DIR = PROJECT_ROOT/'datasets'
RAW_DATA_DIR = DATASET_DIR/'raw'
PROCESSED_DATA_DIR = DATASET_DIR/'processed'

#Shared GenAI Root
GENAI_ROOT = PROJECT_ROOT.parent

HF_CACHE_DIR = GENAI_ROOT/'hf_cache'

QDRANT_STORAGE_DIR = GENAI_ROOT/'qdrant_storage'

USD_TO_INR = 87.0