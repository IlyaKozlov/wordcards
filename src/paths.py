from pathlib import Path

root = Path(__file__).parent.parent / "db"

path_new = root / "new_words.json"
path_existing = root / "existing_words.json"
dictionary_path = root / "dictionary.json"
path_known = root / "known_words.json"
