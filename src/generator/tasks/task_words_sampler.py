import logging
import random
import uuid
from typing import Optional, Counter

from db.task_db import TaskDB
from generator.tasks.task_words import TaskWords
from schemas.word_statistic import WordStatistic


class TaskWordsSampler:



    def __init__(self, db: TaskDB):
        super().__init__()
        self.db = db
        self._weight = 5
        self.logger = logging.getLogger(__name__)

    def four_words(self) -> Optional[TaskWords]:
        words_statistics = self.db.get_words_statistics()
        words_key = [item.word for item in words_statistics]
        word_weights = [self._calculate_weight(item) for item in words_statistics]
        words_sample = random.choices(words_key, weights=word_weights, k=4)

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

    def _calculate_weight(self, item: WordStatistic) -> float:
        return (item.misses + self._weight) / (item.hits + self._weight)
