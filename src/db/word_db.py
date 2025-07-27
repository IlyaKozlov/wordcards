import json
import os
import time
from pathlib import Path
from typing import List

from db.db_abc import Database
from schemas.word import Word


class WordDB(Database):

    def __init__(self):
        super().__init__(db_name="wordsdb")

    def _create_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Tasks (
                uid TEXT PRIMARY KEY,
                answer TEXT,
                timestamp DATETIME
            )
            """
        )

    def words(self) -> List[Word]:
        with open(self.path, "r") as f:
            words_raw: list = json.load(f)
        words = [Word.model_validate(_) for _ in words_raw]
        return words

    def add_word(self, word: str):
        ts = time.time()
        word = word.strip()
        words = self.words()
        added = False
        result = []
        for old_word in words:
            if old_word.word.lower() == word.lower():
                old_word = Word(
                    word=word,
                    last_touch=ts,
                    in_rotation=old_word.in_rotation,
                    n_occurrences=old_word.n_occurrences + 1,
                )
                added = True
            result.append(old_word)
        if not added:
            result.append(Word(
                    word=word,
                    last_touch=ts,
                    in_rotation=False,
                    n_occurrences=1,
                ))
        result.sort(key=lambda x: x.n_occurrences, reverse=True)
        with open(self.path, "w") as f:
            f.write(json.dumps(result, indent=4))

    def __contains__(self, item: str | Word) -> bool:
        if isinstance(item, Word):
            item = item.word
        return item.strip().lower() in (w.word.lower() for w in self.words())

    def set_to_rotation(self, word: str):
        if word not in self:
            self.add_word(word)
        new_words = []
        for old_word in self.words():
            if old_word.word.lower() == word.lower():
                if old_word.in_rotation:
                    return
                old_word = old_word.copy(update={"in_rotation": True})
            new_words.append(old_word)
        with open(self.path, "w") as f:
            f.write(json.dumps(new_words, indent=4))
