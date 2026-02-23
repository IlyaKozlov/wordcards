import abc
import json
import os
import shutil
import uuid
from pathlib import Path
from typing import List, Dict


class Database(abc.ABC):

    def __init__(
        self,
        user_id: str,
    ) -> None:
        super().__init__()

        self._directory_path = Path(__file__).parent.parent.parent / "db" / user_id
        os.makedirs(self._directory_path, exist_ok=True)

        self._path_learning = self._directory_path / "learning_words.json"
        self._path_known = self._directory_path / "known_words.json"
        self._path_all_words = self._directory_path / "all_words.json"
        self._path_audio = self._directory_path.parent / "word2audio.json"

        for path, obj in (
            (self._path_known, []),
            (self._path_learning, {}),
            (self._path_all_words, {}),
        ):
            if not path.exists():
                self.save_object(obj, path)

    @staticmethod
    def save_object(obj: List | Dict, path: Path) -> None:
        tmp_path = path.parent / (path.name + f"_{str(uuid.uuid4())}.tmp")
        with open(tmp_path, "w", encoding="utf-8") as file:
            json.dump(obj=obj, fp=file, indent=4, ensure_ascii=False)
        shutil.move(tmp_path, path)
