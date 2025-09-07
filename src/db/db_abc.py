import abc
import json
import shutil
from pathlib import Path
from typing import List, Dict


class Database(abc.ABC):
    _directory_path = Path(__file__).parent.parent.parent / "db"

    _path_existing = _directory_path / "existing_words.json"
    _path_known = _directory_path / "known_words.json"
    _path_new = _directory_path / "new_words.json"

    @staticmethod
    def save_object(obj: List | Dict, path: Path) -> None:
        tmp_path = path.parent / (path.name + ".tmp")
        with open(tmp_path, "w") as file:
            json.dump(obj=obj, fp=file, indent=4, ensure_ascii=False)
        shutil.move(tmp_path, path)
