import json
import shutil
from collections import Counter
from pathlib import Path


class WordsCounter:

    def __init__(self):
        self.path = Path(__file__).parent.parent.parent / "db" / "new_words.json"
        self.path_tmp = Path(__file__).parent.parent.parent / "db" / "new_words.json.tmp"

    def put(self, word: str, weight: int = 1) -> None:
        with open(self.path, "r") as file:
            data = json.load(file)
        data = Counter(data)
        data[word] += weight
        res = {}
        for k, v in data.most_common():
            res[k] = v
        with open(self.path_tmp, "w") as file:
            json.dump(obj=res, fp=file, indent=4, ensure_ascii=False)
        shutil.move(self.path_tmp, self.path)
