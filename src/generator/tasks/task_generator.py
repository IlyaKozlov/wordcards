import logging
import random
from http.client import HTTPException
from typing import Optional

from db.task_db import TaskDB
from generator.tasks.task_words import TaskWords
from generator.tasks.task_words_sampler import TaskWordsSampler
from schemas.tasks.match_word2audio import MatchWordAudio
from schemas.tasks.match_word_explanation import MatchWordExplanation
from schemas.tasks.no_new_words import NoNewWords
from schemas.tasks.sentence_with_placeholder import SentenceWithPlaceholder
from schemas.tasks.word2explanation import Word2Explanation
from schemas.word_explanation import WordExplanation


class TaskGenerator:

    def __init__(self, user_id: str) -> None:
        self.db = TaskDB(user_id)
        self.word_sampler = TaskWordsSampler(self.db)
        self.logger = logging.getLogger(__name__)
        self._tasks_generators = {
            "Word2Explanation": [
                self._word2explanation,
                self._word2translation,
                self._explanation2word,
            ],
            "SentenceWithPlaceholder": [self._sentence_with_placeholder],
            "MatchWordExplanation": [
                self._match_word2explanation,
                self._match_word2sentence,
                self._match_word2translation,
            ],
            "MatchWordAudio": [self._match_word2audio]
        }

    def new_task(
        self,
        task_type: Optional[str] = None,
    ) -> Word2Explanation | SentenceWithPlaceholder | NoNewWords:
        words = self.word_sampler.four_words()
        if words is None:
            return NoNewWords()
        if task_type is not None:
            generators = self._tasks_generators.get(task_type)
        elif min(word.hits for word in words.words) < -2:
            generators = [
                self._match_word2explanation,
                self._match_word2translation,
            ]
        else:
            tasks_generators = dict(**self._tasks_generators) 
            has_audio = all(_.audio is not None for _ in words.words)
            if not has_audio:
                tasks_generators.pop("MatchWordAudio")
            generators = [
                gen for item in tasks_generators.values() for gen in item
            ]
        result = random.choice(generators)(words)
        return result

    def _match_word2sentence(self, words: TaskWords) -> MatchWordExplanation:
        self.logger.info("Generated task explanation2word")
        items = words.words
        sentences = [
            random.choice(item.sentences_with_placeholder).replace("PLACEHOLDER", "***")
            for item in items
        ]
        return MatchWordExplanation(
            task_id=words.task_id,
            word1=items[0].word,
            explanation1=sentences[0],
            word2=items[1].word,
            explanation2=sentences[1],
            word3=items[2].word,
            explanation3=sentences[2],
            word4=items[3].word,
            explanation4=sentences[3],
        )

    def _match_word2translation(self, words: TaskWords) -> MatchWordExplanation:
        items = words.words
        self.logger.info("Generated task word2translation")
        return MatchWordExplanation(
            task_id=words.task_id,
            word1=items[0].word,
            explanation1=items[0].translation,
            word2=items[1].word,
            explanation2=items[1].translation,
            word3=items[2].word,
            explanation3=items[2].translation,
            word4=items[3].word,
            explanation4=items[3].translation,
        )

    def _match_word2explanation(self, words: TaskWords) -> MatchWordExplanation:
        items = words.words
        self.logger.info("Generated task explanation2word")
        return MatchWordExplanation(
            task_id=words.task_id,
            word1=items[0].word,
            explanation1=items[0].explanation_hidden,
            word2=items[1].word,
            explanation2=items[1].explanation_hidden,
            word3=items[2].word,
            explanation3=items[2].explanation_hidden,
            word4=items[3].word,
            explanation4=items[3].explanation_hidden,
        )

    def _explanation2word(self, words: TaskWords) -> Word2Explanation:
        items = words.words
        right_answer_id = random.choice(range(len(items)))
        task_id = words.task_id
        self.db.save_task(
            task_id=task_id,
            word=items[right_answer_id].word,
            explanation=items[right_answer_id].word
            + "\n"
            + items[right_answer_id].explanation,
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
            right_answer_id=right_answer_id + 1,
            target_word=items[right_answer_id].word,
        )

    def _sentence_with_placeholder(self, words: TaskWords) -> SentenceWithPlaceholder:
        item: WordExplanation = random.choice(words.words)
        sentence: str = random.choice(item.sentences_with_placeholder)
        self.db.save_task(
            task_id=words.task_id,
            word="",
            explanation="",
            right_answer=item.word.lower(),
        )
        self.logger.info("Generated task sentence_with_placeholder")
        return SentenceWithPlaceholder(
            task_id=words.task_id,
            explanation=item.explanation_hidden,
            word=item.word,
            word_part=item.word_part,
            sentence=sentence,
        )

    def _word2explanation(self, words: TaskWords) -> Word2Explanation:
        items = words.words
        right_answer_id = random.choice(range(len(items)))
        self.db.save_task(
            task_id=words.task_id,
            word=items[right_answer_id].word,
            explanation=items[right_answer_id].word
            + "\n"
            + items[right_answer_id].explanation,
            right_answer=str(right_answer_id + 1),
        )
        self.logger.info("Generated task word2explanation")
        return Word2Explanation(
            task_id=words.task_id,
            word1=items[0].word,
            word2=items[1].word,
            word3=items[2].word,
            word4=items[3].word,
            explanation=items[right_answer_id].explanation_hidden,
            right_answer_id=right_answer_id + 1,
            target_word=items[right_answer_id].word,
        )

    def _word2translation(self, words: TaskWords) -> Word2Explanation:

        items = words.words
        if items is None or len(items) != 4:
            raise HTTPException("Not enough items to fetch new task")
        right_answer_id = random.choice(range(len(items)))

        self.db.save_task(
            task_id=words.task_id,
            word=items[right_answer_id].word,
            explanation=items[right_answer_id].word
            + "\n"
            + items[right_answer_id].explanation,
            right_answer=str(right_answer_id + 1),
        )
        self.logger.info("Generated task word2translation")
        return Word2Explanation(
            task_id=words.task_id,
            word1=items[0].word,
            word2=items[1].word,
            word3=items[2].word,
            word4=items[3].word,
            explanation=items[right_answer_id].translation,
            right_answer_id=right_answer_id + 1,
            target_word=items[right_answer_id].word,
        )

    def _match_word2audio(self, words: TaskWords) -> MatchWordAudio:
        return MatchWordAudio(
            task_id=words.task_id,
            word1=words.words[0].word,
            audio1=words.words[0].audio if words.words[0].audio else words.words[0].word,
            word2=words.words[1].word,
            audio2=words.words[1].audio if words.words[1].audio else words.words[1].word,
            word3=words.words[2].word,
            audio3=words.words[2].audio if words.words[2].audio else words.words[2].word,
            word4=words.words[3].word,
            audio4=words.words[3].audio if words.words[3].audio else words.words[3].word,
        )
