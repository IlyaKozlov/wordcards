from pydantic import BaseModel


class Word2Explanation(BaseModel):
    explanation: str
    word1: str
    word2: str
    word3: str
    word4: str
