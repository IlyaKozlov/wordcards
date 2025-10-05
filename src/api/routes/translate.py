from fastapi import Form
from fastapi.routing import APIRouter

from generator.translator import Translator

translate_route = APIRouter()


@translate_route.post("/translate")
def translate(word: str = Form()) -> str:
    translation = Translator().translate(word)
    return translation

