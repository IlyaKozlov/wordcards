import abc
import json
import shutil
from pathlib import Path
from typing import List, Dict


class Database(abc.ABC):
    _directory_path = Path(__file__).parent.parent.parent / "db"

    _path_learning = _directory_path / "learning_words.json"
    _path_known = _directory_path / "known_words.json"
    _path_all_words = _directory_path / "all_words.json"

    @staticmethod
    def save_object(obj: List | Dict, path: Path) -> None:
        tmp_path = path.parent / (path.name + ".tmp")
        with open(tmp_path, "w") as file:
            json.dump(obj=obj, fp=file, indent=4, ensure_ascii=False)
        shutil.move(tmp_path, path)
