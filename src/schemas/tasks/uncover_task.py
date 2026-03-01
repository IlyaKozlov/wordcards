from typing import Optional

from openai import BaseModel


class UncoverTask(BaseModel):
    word: str
    explanation: str
    translation: Optional[str] = None
    task_type: str = "UncoverTask"
