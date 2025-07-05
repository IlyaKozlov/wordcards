from pydantic import BaseModel


class Explanation2Word(BaseModel):
    word: str
    explanation1: str
    explanation2: str
    explanation3: str
    explanation4: str
