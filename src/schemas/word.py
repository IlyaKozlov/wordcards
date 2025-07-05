from pydantic import BaseModel


class Word(BaseModel):
    word: str
    n_occurrences: int
    last_touch: float
    in_rotation: bool = False
