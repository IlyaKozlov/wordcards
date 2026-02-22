from typing import Optional, List

from pydantic import BaseModel


class Word2Explanation(BaseModel):
    task_id: str
    explanation: str
    explanation_placeholder: Optional[List[str]]
    word1: str
    word2: str
    word3: str
    word4: str
    target_word: str
    target_word_placeholder: Optional[List[str]]
    audio_url: Optional[str] = None
    right_answer_id: int
    task_type: str = "Word2Explanation"
