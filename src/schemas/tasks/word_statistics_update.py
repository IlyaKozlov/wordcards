from typing import List, Iterator

from openai import BaseModel


class WordStatisticUpdate(BaseModel):
    word: str
    is_true: bool


class WordsStatisticUpdate(BaseModel):
    statistics: List[WordStatisticUpdate]

    def __iter__(self) -> Iterator[WordStatisticUpdate]:
        return iter(self.statistics)
