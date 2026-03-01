import re
from typing import List, Optional

from pydantic import BaseModel


_placeholder_regexp = r"_[^_]+_"


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
        result = []
        for sentence in self.sentences:
            replacement = "PLACEHOLDER"
            sentence_with_placeholder = self._replace_underscore(
                sentence,
                replacement,
            )
            if replacement not in sentence_with_placeholder:
                sentence_with_placeholder += f" ({self.word})"
            result.append(sentence_with_placeholder)
        return result

    @property
    def word_part(self) -> str:
        if len(self.word) <= 3:
            return "*" * len(self.word)
        else:
            return self.word[0] + ("*" * (len(self.word) - 2)) + self.word[-1]

    @staticmethod
    def _replace_underscore(string: str, replacement: str) -> str:
        result = re.sub(_placeholder_regexp, replacement, string)
        if replacement not in result:
            result += f" ({replacement})"
        return result

    @property
    def placeholders(self) -> List[str]:
        result = [
            match[1:-1]
            for match in re.findall(_placeholder_regexp, self.explanation)
            if len(match) > 2
        ]
        if len(result) == 0:
            return [self.word]
        return result
