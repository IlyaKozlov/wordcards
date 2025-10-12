from pydantic import BaseModel


class WordsStatistic(BaseModel):
    n_words: int
    n_uncovered_words: int
