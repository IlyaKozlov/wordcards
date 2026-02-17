from pydantic import BaseModel


class MatchWordAudio(BaseModel):
    task_id: str

    word1: str
    audio1: str

    word2: str
    audio2: str

    word3: str
    audio3: str

    word4: str
    audio4: str

    task_type: str = "MatchWordAudio"
