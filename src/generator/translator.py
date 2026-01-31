import logging
from typing import Optional

from db.dictionary import Dictionary
from db.words_cnt import WordsCounter
from generator.generate_word_explanation import GenerateWordExplanation

logger = logging.getLogger(__name__)


class Translator:

    def __init__(self, user_id: Optional[str]):
        self.cache_miss_cnt = 0
        self.call_cnt = 0
        self.dictionary = Dictionary()
        if user_id:
            self.counter = WordsCounter(user_id)

    def translate(self, word: str, update_cnt: bool = True) -> str:
        self.call_cnt += 1
        translation = self.dictionary.get(word)
        if translation is None:
            logger.info(f"Not found in dictionary {word}, will update")
            self.cache_miss_cnt += 1
            explanations = GenerateWordExplanation().generate_word_explanation(word)
            translation = ""
            for explanation in explanations:
                translation += f"{explanation.explanation}\n"
                translation += f"{explanation.translation}\n"
            self.dictionary.put(word, translation)
        if update_cnt and self.counter is not None:
            normalized = word.lower().strip()
            self.counter.put(normalized)
        return translation
