import json
import random
import time
from http.client import HTTPException
from typing import List, Optional, Dict
from uuid import UUID

from db.db_abc import Database
from schemas.tasks.task_answer import TaskAnswer
from schemas.tasks.word_statistics_update import WordsStatisticUpdate
from schemas.word_explanation import WordExplanation
from schemas.word_statistic import WordStatistic


class TaskDB(Database):

    def __init__(self, user_id: str) -> None:
        super().__init__(user_id)
        self._task_path = self._directory_path / "tasks.json"
        self._task_statistic_path = self._directory_path / "tasks_statistic.json"

    def get_four_words(
        self,
        words: Optional[List[str]] = None,
    ) -> Optional[List[WordExplanation]]:
        with open(self._path_learning) as file, open(
            self._task_statistic_path
        ) as statistic_file:
            data: dict = json.load(file)
            statistics = json.load(statistic_file)
        if len(data) < 4:
            return None
        if words is None:
            words = random.sample(list(data.keys()), 4)
        result = []
        for word in words:
            explanation = random.choice(data[word])
            explanation["hits"] = statistics.get(word, {}).get("hits", 0)
            result.append(WordExplanation.model_validate(explanation))
        if result is None or len(result) != 4:
            raise HTTPException("Not enough items to fetch new task")
        return result

    def update_task_statistic(
        self,
        statistics: WordsStatisticUpdate,
    ) -> None:
        if self._task_statistic_path.exists():
            with open(self._task_statistic_path) as file:
                data: dict = json.load(file)
        else:
            data = {}
        for word_update in statistics.statistics:
            word = word_update.word
            is_correct = word_update.is_true
            item = data.get(word, {"hits": 0, "misses": 0, "correct": 0})
            if is_correct:
                item["correct"] += 1
            else:
                item["misses"] += 1
            item["hits"] += 1
            data[word] = item
        self.save_object(data, self._task_statistic_path)

    def save_task(
        self,
        task_id: UUID | str,
        right_answer: str,
        word: str,
        explanation: str,
    ) -> None:
        task_id = str(task_id)
        data = self._get_data()
        ts = int(time.time())
        item = dict(
            task_id=task_id,
            right_answer=right_answer,
            word=word,
            timestamp=ts,
            explanation=explanation,
        )
        data[task_id] = item
        self.save_object(data, self._task_path)

    def _get_data(self) -> Dict[str, Dict]:
        if self._task_path.exists():
            data: dict = json.load(open(self._task_path))
            ts_threshold = time.time() - 7 * 24 * 3600
            data = {k: v for k, v in data.items() if v["timestamp"] > ts_threshold}
        else:
            data = {}
        return data

    def get_task(self, task_id: UUID | str) -> Optional[TaskAnswer]:
        task_id = str(task_id)
        return TaskAnswer.model_validate(self._get_data()[task_id])

    def get_words_statistics(self) -> List[WordStatistic]:
        if not self._task_statistic_path.exists():
            self.save_object({}, self._task_statistic_path)
        with open(self._task_statistic_path) as statistic_file, open(
            self._path_learning
        ) as words_file:
            statistics: dict = json.load(statistic_file)
            words: dict = json.load(words_file)
        result = []
        for word in sorted(words.keys()):
            statistic = statistics.get(word, {"hits": 0, "misses": 0, "correct": 0})
            result.append(
                WordStatistic(
                    word=word,
                    hits=statistic.get("hits", 0),
                    misses=statistic.get("misses", 0),
                    correct=statistic.get("correct", 0),
                )
            )
        return result
