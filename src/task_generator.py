import logging
import random
import uuid
from http.client import HTTPException
from typing import Optional

from db.task_db import TaskDB
from schemas.tasks.match_word_explanation import MatchWordExplanation
from schemas.tasks.sentence_with_placeholder import SentenceWithPlaceholder
from schemas.tasks.word2explanation import Word2Explanation
from schemas.word_explanation import WordExplanation


class TaskGenerator:

    def __init__(self):
        self.db = TaskDB()
        self.logger = logging.getLogger(__name__)
        self._tasks_generators = {
            "Word2Explanation": [self._word2explanation, self._explanation2word],
            "SentenceWithPlaceholder": [self._sentence_with_placeholder],
            "MatchWordExplanation": [self._match_word2explanation, self._match_word2sentence],
        }

    def new_task(self, task_type: Optional[str] = None) -> Word2Explanation | SentenceWithPlaceholder:
        if task_type is None:
            generators = [gen for item in self._tasks_generators.values() for gen in item]
        else:
            generators = self._tasks_generators.get(task_type)
        return random.choice(generators)()

    def _match_word2sentence(self) -> MatchWordExplanation:
        items, task_id = self._match_word2()
        self.logger.info("Generated task explanation2word")
        sentences = [
            random.choice(item.sentences_with_placeholder).replace("PLACEHOLDER", "***")
             for item in items
        ]
        return MatchWordExplanation(
            task_id=task_id,
            word1=items[0].word,
            explanation1=sentences[0],
            word2=items[1].word,
            explanation2=sentences[1],
            word3=items[2].word,
            explanation3=sentences[2],
            word4=items[3].word,
            explanation4=sentences[3],
        )

    def _match_word2(self):
        items = self.db.get_four_words()
        if items is None or len(items) != 4:
            raise HTTPException("Not enough items to fetch new task")
        task_id = str(uuid.uuid4())
        self.db.save_task(
            task_id=task_id,
            word="",
            explanation="",
            right_answer="ok",
        )
        return items, task_id

    def _match_word2explanation(self) -> MatchWordExplanation:
        items, task_id = self._match_word2()
        self.logger.info("Generated task explanation2word")
        return MatchWordExplanation(
            task_id=task_id,
            word1=items[0].word,
            explanation1=items[0].explanation_hidden,
            word2=items[1].word,
            explanation2=items[1].explanation_hidden,
            word3=items[2].word,
            explanation3=items[2].explanation_hidden,
            word4=items[3].word,
            explanation4=items[3].explanation_hidden,
        )

    def _explanation2word(self) -> Word2Explanation:
        items = self.db.get_four_words()
        right_answer_id = random.choice(range(len(items)))
        task_id = str(uuid.uuid4())
        self.db.save_task(
            task_id=task_id,
            word=items[right_answer_id].word,
            explanation=items[right_answer_id].word + "\n" + items[
                right_answer_id].explanation,
            right_answer=str(right_answer_id + 1),
        )
        self.logger.info("Generated task explanation2word")
        return Word2Explanation(
            task_id=task_id,
            word1=items[0].explanation_hidden,
            word2=items[1].explanation_hidden,
            word3=items[2].explanation_hidden,
            word4=items[3].explanation_hidden,
            explanation=items[right_answer_id].word,
        )

    def _sentence_with_placeholder(self) -> SentenceWithPlaceholder:
        task_id = str(uuid.uuid4())
        items = self.db.get_four_words()
        item: WordExplanation = random.choice(items)
        sentence: str = random.choice(item.sentences_with_placeholder)
        self.db.save_task(
            task_id=task_id,
            word="",
            explanation="",
            right_answer=item.word.lower(),
        )
        self.logger.info("Generated task sentence_with_placeholder")
        return SentenceWithPlaceholder(
            task_id=task_id,
            explanation=item.explanation_hidden,
            word=item.word,
            word_part=item.word_part,
            sentence=sentence,
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
        self.logger.info("Generated task word2explanation")
        return Word2Explanation(
            task_id=task_id,
            word1=items[0].word,
            word2=items[1].word,
            word3=items[2].word,
            word4=items[3].word,
            explanation=items[right_answer_id].explanation_hidden,
        )
