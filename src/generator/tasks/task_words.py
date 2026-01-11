from typing import List

from pydantic import BaseModel

from schemas.word_explanation import WordExplanation


class TaskWords(BaseModel):

    task_id: str
    word1: WordExplanation
    word2: WordExplanation
    word3: WordExplanation
    word4: WordExplanation

    @property
    def words(self) -> List[WordExplanation]:
        return [
            self.word1,
            self.word2,
            self.word3,
            self.word4,
        ]

