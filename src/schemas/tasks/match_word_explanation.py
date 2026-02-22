from typing import Optional

from pydantic import BaseModel


class MatchWordExplanation(BaseModel):
    task_id: str

    word1: str
    audio1: Optional[str]
    explanation1: str

    word2: str
    audio2: Optional[str]
    explanation2: str

    word3: str
    audio3: Optional[str]
    explanation3: str

    word4: str
    audio4: Optional[str]
    explanation4: str

    task_type: str = "MatchWordExplanation"
