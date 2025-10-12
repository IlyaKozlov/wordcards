from typing import Optional

from pydantic import BaseModel

from schemas.words_statistic import WordsStatistic


class WordWithExplanation(BaseModel):
    word: str
    explanation: str
    words_statistics: Optional[WordsStatistic] = None
