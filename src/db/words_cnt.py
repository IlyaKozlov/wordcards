import json
import shutil
from collections import Counter
from pathlib import Path

from db.word_db import WordDB


class WordsCounter:

    def __init__(self):
        self.db = WordDB()


    def put(self, word: str, weight: int = 1) -> None:
        self.db.update_existing_words(cnt=Counter({word: weight}))
