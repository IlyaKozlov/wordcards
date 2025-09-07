from pydantic import BaseModel


class Word2Explanation(BaseModel):
    task_id: str
    explanation: str
    word1: str
    word2: str
    word3: str
    word4: str
