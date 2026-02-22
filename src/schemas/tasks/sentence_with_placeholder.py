from typing import Optional

from pydantic import BaseModel


class SentenceWithPlaceholder(BaseModel):
    task_id: str
    sentence: str
    explanation: str
    word: str
    audio_url: Optional[str]
    word_part: str
    task_type: str = "SentenceWithPlaceholder"
