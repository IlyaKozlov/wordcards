from pydantic import BaseModel


class WordWithExplanation(BaseModel):
    word: str
    explanation: str
