import json
from pathlib import Path
from typing import List

from db.db_abc import Database
from schemas.word_explanation import WordExplanation


class WordDB(Database):

    def get_new_words(self, min_cnt: int = 10) -> List[str]:
        with open(self._path_existing) as f1, open(self._path_known) as f2:
            existing_words = set(json.load(f1).keys()) | set(json.load(f2))
        with open(self._path_new) as f:
            words_cnt = [
                (w, cnt)
                for w, cnt in json.load(f).items()
                if w not in existing_words
                if len(w) > 0
                if any(_.isalpha() for _ in w)
                if cnt > min_cnt
            ]
            words_cnt.sort(key=lambda x: x[1], reverse=True)
            words = [w for w, _ in words_cnt]
        return words

    def save_know_word(self, word: str) -> None:
        with open(self._path_known) as file:
            ls = json.load(file)
        if word not in ls:
            ls.append(word)
        self.save_object(ls, self._path_known)

    def get_n_know_word(self) -> int:
        with open(self._path_known) as file:
            ls = json.load(file)
        return len(ls)

    def save_word_explanation(self, word: str, explanations: List[WordExplanation]) -> None:
        with open(self._path_existing) as f:
            data = json.load(f)
        data[word] = [expl.model_dump() for expl in explanations]
        self.save_object(data, self._path_existing)
