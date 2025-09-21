from pydantic import BaseModel


class SentenceWithPlaceholder(BaseModel):
    task_id: str
    sentence: str
    word: str
    task_type: str = "SentenceWithPlaceholder"
