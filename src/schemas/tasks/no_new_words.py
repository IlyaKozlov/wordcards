from pydantic import BaseModel


class NoNewWords(BaseModel):
    task_type: str = "NoNewWords"
