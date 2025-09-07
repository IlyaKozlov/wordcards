from openai import BaseModel


class TaskStatus(BaseModel):
    is_true: bool
    explanation: str
