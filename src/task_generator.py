import random
import uuid
from http.client import HTTPException

from db.task_db import TaskDB
from schemas.tasks.word2explanation import Word2Explanation


class TaskGenerator:

    def __init__(self):
        self.db = TaskDB()

    def new_task(self) -> Word2Explanation:
        return random.choice([self._word2explanation, self._explanation2word])()

    def _explanation2word(self) -> Word2Explanation:
        items = self.db.get_four_words()
        if items is None or len(items) != 4:
            raise HTTPException("Not enough items to fetch new task")
        right_answer_id = random.choice(range(len(items)))
        task_id = str(uuid.uuid4())
        self.db.save_task(
            task_id=task_id,
            word=items[right_answer_id].word,
            explanation=items[right_answer_id].word + "\n" + items[
                right_answer_id].explanation,
            right_answer=str(right_answer_id + 1),
        )
        return Word2Explanation(
            task_id=task_id,
            word1=items[0].explanation,
            word2=items[1].explanation,
            word3=items[2].explanation,
            word4=items[3].explanation,
            explanation=items[right_answer_id].word,
        )

    def _word2explanation(self) -> Word2Explanation:
        items = self.db.get_four_words()
        if items is None or len(items) != 4:
            raise HTTPException("Not enough items to fetch new task")
        right_answer_id = random.choice(range(len(items)))
        task_id = str(uuid.uuid4())
        self.db.save_task(
            task_id=task_id,
            word=items[right_answer_id].word,
            explanation=items[right_answer_id].word + "\n" + items[
                right_answer_id].explanation,
            right_answer=str(right_answer_id + 1),
        )
        return Word2Explanation(
            task_id=task_id,
            word1=items[0].word,
            word2=items[1].word,
            word3=items[2].word,
            word4=items[3].word,
            explanation=items[right_answer_id].explanation,
        )
