import json
import random
import time
from typing import List, Optional, Dict
from uuid import UUID

from db.db_abc import Database
from schemas.tasks.task_answer import TaskAnswer
from schemas.word_explanation import WordExplanation


class TaskDB(Database):
    _task_path = Database._directory_path / "tasks.json"
    _task_statistic_path = Database._directory_path / "tasks_statistic.json"

    def get_four_words(self) -> Optional[List[WordExplanation]]:
        with open(self._path_existing) as file:
            data: dict = json.load(file)
        if len(data) < 4:
            return None
        words = random.sample(list(data.keys()), 4)
        result = []
        for word in words:
            explanation = random.choice(data[word])
            result.append(WordExplanation.model_validate(explanation))
        return result

    def update_task_statistic(self, word: str, is_correct: bool) -> None:
        if self._task_statistic_path.exists():
            with open(self._task_statistic_path) as file:
                data: dict = json.load(file)
        else:
            data = {}
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
