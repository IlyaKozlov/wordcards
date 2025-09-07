from fastapi import Query
from fastapi.routing import APIRouter

from generator.translator import Translator

translate_route = APIRouter()


@translate_route.get("")
def add_book(word: str = Query()) -> str:
    translation = Translator().translate(word)
    return translation

