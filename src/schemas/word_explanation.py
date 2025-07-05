from typing import List

from pydantic import BaseModel


class WordExplanation(BaseModel):
    word: str
    meaning: str
    explanation: str
    sentences: List[str]
    translation: str
