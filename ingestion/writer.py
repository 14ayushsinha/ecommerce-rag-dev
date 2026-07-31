import json
from pathlib import Path
from typing import Dict, Any

class ProductWriter:

    def __init__(self, output_path: str):

        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        self.file = open(self.output_path, 'w', encoding='utf-8')
        self.total_written=0
    
    def write(self, product: Dict[str, Any]):
        json.dump(
            product,
            self.file,
            ensure_ascii=False
        )

        self.file.write('\n')
        self.total_written+=1
    
    def close(self):
        self.file.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()