from typing import Optional, List

from pydantic import BaseModel


class MatchWordExplanation(BaseModel):
    task_id: str

    word1: str
    audio1: Optional[str]
    explanation1: str
    explanation_placeholder1: Optional[List[str]]

    word2: str
    audio2: Optional[str]
    explanation2: str
    explanation_placeholder2: Optional[List[str]]

    word3: str
    audio3: Optional[str]
    explanation3: str
    explanation_placeholder3: Optional[List[str]]

    word4: str
    audio4: Optional[str]
    explanation4: str
    explanation_placeholder4: Optional[List[str]]

    task_type: str = "MatchWordExplanation"
