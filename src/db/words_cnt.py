from collections import Counter

from db.word_db import WordDB


class WordsCounter:

    def __init__(self, user_id: str):
        self.db = WordDB(user_id)


    def put(self, word: str, weight: int = 1) -> None:
        self.db.update_existing_words(cnt=Counter({word: weight}))
