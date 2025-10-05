from schemas.message_type import MessageType
from pydantic import BaseModel


class Chunk(BaseModel):
    text: str
    message_type: MessageType

    def __init__(self, message: str):
        assert len(message) > 0
        text = message.strip()
        if text.startswith("**"):
            message_type = MessageType.BOLD
        elif text.startswith("Synonyms"):
            message_type = MessageType.ITALIC
        elif text.startswith("<RUS>"):
            text = message.replace("<RUS>", "")
            message_type = MessageType.SPOILER
        else:
            message_type = MessageType.NORMAL
        super().__init__(text=text, message_type=message_type)
