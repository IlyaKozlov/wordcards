import json
from typing import List, Dict
from collections import Counter

from db.db_abc import Database
from schemas.word_explanation import WordExplanation


class WordDB(Database):

    def get_new_words(self, min_cnt: int = 10) -> List[str]:
        with open(self._path_learning, encoding="utf-8") as f1, open(self._path_known, encoding="utf-8") as f2:
            existing_words = set(json.load(f1).keys()) | set(json.load(f2))
        with open(self._path_all_words, encoding="utf-8") as f:
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
        with open(self._path_known, encoding="utf-8") as file:
            ls = json.load(file)
        if word not in ls:
            ls.append(word)
        self.save_object(ls, self._path_known)

    def get_n_know_word(self) -> int:
        with open(self._path_known, encoding="utf-8") as file:
            ls = json.load(file)
        return len(ls)

    def get_learning_words(self) -> Dict[str, list]:
        with open(self._path_learning, encoding="utf-8") as file:
            learning_word_data = json.load(file)
        return learning_word_data

    def save_word_explanation(self, word: str, explanations: List[WordExplanation]) -> None:
        with open(self._path_learning, encoding="utf-8") as f:
            data = json.load(f)
        data[word] = [expl.model_dump() for expl in explanations]
        self.save_object(data, self._path_learning)

    def update_existing_words(self, cnt: Counter) -> None:

        with open(self._path_all_words, "r", encoding="utf-8") as file:
            all_words = json.load(file)
        all_words = Counter(all_words)

        for k, v in cnt.items():
            all_words[k] += v
        self.save_object(all_words, self._path_all_words)
