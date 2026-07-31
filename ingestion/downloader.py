from pathlib import Path

from config.settings import RAW_DATA_DIR, HF_CACHE_DIR
from config.settings import REPO_ID
from huggingface_hub import hf_hub_download

class AmazonDownloader:
    def __init__(self):
        self.cache_dir = RAW_DATA_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def download(self, category: str) -> str:
        local_file = hf_hub_download(
            repo_id=REPO_ID,
            repo_type='dataset',
            filename=f'raw/meta_categories/{category}',
            local_dir=self.cache_dir,
            cache_dir=str(HF_CACHE_DIR),
            local_dir_use_symlinks=False,
        )

        return local_file