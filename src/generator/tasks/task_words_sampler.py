import heapq
import logging
import random
import uuid
from collections import deque
from typing import Optional, List

from db.task_db import TaskDB
from db.word_db import WordDB
from generator.tasks.task_words import TaskWords
from generator.translator import Translator
from schemas.word_statistic import WordStatistic
from schemas.word_with_explanation import WordWithExplanation


class TaskWordsSampler:

    _new_word_generated = deque(maxlen=5)

    def __init__(self, db: TaskDB, word_db: WordDB) -> None:
        super().__init__()
        self.db = db
        self.word_db = word_db
        self._weight = 5
        self.logger = logging.getLogger(__name__)

    def four_words(self) -> Optional[TaskWords]:
        words_statistics = self.db.get_words_statistics()
        words_key = [item.word for item in words_statistics]
        word_weights = [self._calculate_weight(item) for item in words_statistics]

        words_sample = self._sample(word_weights, words_key)

        cnt = {}
        cnt["hits"] = 0
        cnt["correct"] = 0
        cnt["misses"] = 0
        for word_stat in words_statistics:
            cnt["hits"] += word_stat.hits
            cnt["correct"] += word_stat.correct
            cnt["misses"] += word_stat.misses
        cnt["n_words"] = len(words_statistics)
        self.logger.info(f"Words statistics: {cnt}")

        words = self.db.get_four_words(words_sample)
        if words:
            return TaskWords(
                task_id=str(uuid.uuid4()),
                word1=words[0],
                word2=words[1],
                word3=words[2],
                word4=words[3],
            )
        return None

    def _sample(
        self,
        word_weights: List[float],
        words_key: List[str],
    ) -> Optional[List[str]]:
        # Weighted sampling without replacement (Efraimidis-Spirakis algorithm)
        k = 4
        if len(words_key) < k:
            self.logger.error("Not enough words to sample four unique items")
            return None
        # assign a random key to each item: key = U(0,1) ** (1/weight)
        # then take the k items with largest keys
        samples = heapq.nlargest(
            k,
            ((random.random() ** (1.0 / wt), wk) for wk, wt in zip(words_key, word_weights)),
        )
        words_sample = [wk for _, wk in samples]
        return words_sample

    def _calculate_weight(self, item: WordStatistic) -> float:
        return (item.misses + self._weight) / (item.hits + self._weight)

    def need_new_word(self) -> bool:
        if not self.word_db.get_new_words(1):
            return False
        statistics = self.db.get_words_statistics()
        if len(statistics) < 10:
            return True
        new_words_fraction = 0
        for item in statistics:
            if item.hits < 2:
                new_words_fraction += 1
        new_words_fraction /= len(statistics)
        return random.uniform(0, 0.12) > new_words_fraction

    def new_word(self) -> WordWithExplanation:
        words = self.word_db.get_new_words(1, 50)
        words.sort(key=lambda word: word in self._new_word_generated)
        if len(words) == 0:
            raise ValueError("No new words")
        word = random.choice(words)
        self._new_word_generated.append(word)
        explanation = Translator(None).translate(word, update_cnt=False)
        return WordWithExplanation(word=word, explanation=explanation)
