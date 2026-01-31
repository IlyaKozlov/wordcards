from pydantic import BaseModel


class WordStatistic(BaseModel):
    word: str
    hits: int
    misses: int
    correct: int
