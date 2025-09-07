from pydantic import BaseModel


class Sentence2Word(BaseModel):
    sentence_with_space: str
    word_with_space: str
