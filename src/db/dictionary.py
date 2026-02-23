import json
import shutil
from pathlib import Path
from typing import Optional


class Dictionary:

    def __init__(self) -> None:
        self.path = Path(__file__).parent.parent.parent / "db" / "dictionary.json"
        self.path_tmp = (
            Path(__file__).parent.parent.parent / "db" / "dictionary.json.tmp"
        )

    def get(self, word: str) -> Optional[str]:
        word = self._to_key(word)
        if not self.path.is_file():
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(obj={}, fp=file)
        with open(self.path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data.get(word.lower())

    def put(self, word: str, translation: str) -> None:
        word = self._to_key(word)
        with open(self.path, "r", encoding="utf-8") as file:
            data = json.load(file)
        data[word] = translation
        with open(self.path_tmp, "w", encoding="utf-8") as file:
            json.dump(obj=data, fp=file, indent=4, ensure_ascii=False)
        shutil.move(self.path_tmp, self.path)

    @staticmethod
    def _to_key(word: str) -> str:
        return word.strip().lower()
