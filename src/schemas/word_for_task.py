from typing import List

from pydantic import BaseModel


class WordForTask(BaseModel):
    word: str
    explanation: str
    translation: str
    examples: List[str]
