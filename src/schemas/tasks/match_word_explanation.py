from pydantic import BaseModel


class MatchWordExplanation(BaseModel):
    task_id: str

    word1: str
    explanation1: str

    word2: str
    explanation2: str

    word3: str
    explanation3: str

    word4: str
    explanation4: str

    task_type: str = "MatchWordExplanation"
