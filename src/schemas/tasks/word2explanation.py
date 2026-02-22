from typing import Optional

from pydantic import BaseModel


class Word2Explanation(BaseModel):
    task_id: str
    explanation: str
    word1: str
    word2: str
    word3: str
    word4: str
    target_word: str
    audio_url: Optional[str] = None
    right_answer_id: int
    task_type: str = "Word2Explanation"
