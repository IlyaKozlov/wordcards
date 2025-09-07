from pydantic import BaseModel


class TaskAnswer(BaseModel):
    task_id: str
    right_answer: str
    explanation: str
    word: str
    timestamp: int
