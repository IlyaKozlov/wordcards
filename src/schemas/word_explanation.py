import re
from typing import List, Optional

from pydantic import BaseModel


class WordExplanation(BaseModel):
    hits: int = 0
    word: str
    meaning: str
    explanation: str
    sentences: List[str]
    translation: str
    audio: Optional[str] = None

    @property
    def explanation_hidden(self) -> str:
        return self._replace_underscore(self.explanation, "***")

    @property
    def sentences_with_placeholder(self) -> List[str]:
        return [self._replace_underscore(_, "PLACEHOLDER") for _ in self.sentences]

    @property
    def word_part(self) -> str:
        if len(self.word) <= 3:
            return "*" * len(self.word)
        else:
            return self.word[0] + ("*" * (len(self.word) - 2)) + self.word[-1]

    @staticmethod
    def _replace_underscore(string: str, replacement: str) -> str:
        result = re.sub(r"_[^_]+_", replacement, string)
        if replacement not in result:
            result += f" ({replacement})"
        return result
