import json

class JSONLStreamReader:

    def __init__(self, file_path):
        self.file_path = file_path

    def stream(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue
                
                yield json.loads(line)