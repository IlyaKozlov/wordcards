import logging
from pathlib import Path
from typing import Iterable, Tuple

from db.words_cnt import WordsCounter
from llm.llm_model import LLMModel
from schemas.chunk import Chunk

logger = logging.getLogger(__name__)


class TranslatorStream:

    def __init__(self, model: LLMModel) -> None:
        self.model = model
        self._cyrillic = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        self._latin = "abcdefghijklmnopqrstuvwxyz"
        self._templates = Path(__file__).parent / "prompts"
        assert self._templates.is_dir()
        self.counter = WordsCounter()

    @staticmethod
    def from_env() -> "TranslatorStream":
        model = LLMModel.from_env()
        return TranslatorStream(model)

    def handle(self, message: str) -> Iterable[Chunk]:
        if len(message) == 0:
            return

        latin_cnt, cyrillic_cnt, word_cnt = self._cnt_letters(message)

        if cyrillic_cnt > latin_cnt:
            logger.info("Assume need translate from russian to english")
            yield from self._translate_ru_en(message)
        else:
            logger.info("Assume need translate from english to russian")

            yield from self._translate_en_ru(message)

    @staticmethod
    def _batch(stream: Iterable[str], max_len: int = 300) -> Iterable[str]:
        batch = ""
        letters = (letter for chunk in stream for letter in chunk)
        for letter in letters:
            batch += letter
            if len(batch) > max_len or letter == "\n":
                if batch.strip() != "```":
                    yield batch
                batch = ""
        if len(batch) > 0 and batch.strip() != "```":
            yield batch

    def _cnt_letters(self, message: str) -> Tuple[int, int, int]:
        message = message.lower()
        word_cnt = len(message.strip().split())
        if len(message) == 0:
            return 0, 0, 0
        latin_cnt = sum(letter in self._latin for letter in message)
        cyrillic_cnt = sum(letter in self._cyrillic for letter in message)
        return latin_cnt, cyrillic_cnt, word_cnt

    def _translate_en_ru(self, message: str):
        with open(self._templates / "translate_en_ru.txt") as f:
            template = f.read()
        prompt = template.format(message=message)
        yield from (
            Chunk(text)
            for text in self._batch(self.model.invoke(prompt))
            if len(text) > 0
        )

    def _translate_ru_en(self, message: str):
        with open(self._templates / "translate_ru_en.txt") as f:
            template = f.read()
        prompt = template.format(message=message)
        yield from (
            Chunk(text)
            for text in self._batch(self.model.invoke(prompt))
            if len(text) > 0
        )
