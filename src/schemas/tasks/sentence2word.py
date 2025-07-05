from pydantic import BaseModel


class Word2Explanation(BaseModel):
    sentence_with_space: str
    word_with_space: str
