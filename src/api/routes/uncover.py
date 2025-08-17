import json
import random
from pathlib import Path

from fastapi import Form
from fastapi.routing import APIRouter
from starlette.responses import HTMLResponse

from generator.translator import Translator
from paths import path_existing, path_new, path_known
from schemas.word_with_explanation import WordWithExplanation

uncover = APIRouter()


@uncover.get("")
def html_form() -> HTMLResponse:
    path = Path(__file__).parent / "form.html"
    with open(path) as file:
        code = file.read()
    return HTMLResponse(content=code)


@uncover.post("/uncover_word")
def uncover_word(word: str = Form()) -> str:
    with open(path_existing) as file:
        ls = json.load(file)
    if word not in ls:
        ls.append(word)
    with open(path_existing, "w") as out:
        json.dump(obj=ls, fp=out, indent=4)
    return "Ok"


@uncover.post("/mark_as_known")
def mark_as_known(word: str = Form(...)) -> str:
    with open(path_known) as file:
        ls = json.load(file)
    if word not in ls:
        ls.append(word)
    with open(path_known, "w") as out:
        json.dump(obj=ls, fp=out, indent=4)
    return "Ok"


@uncover.get("/show_new_word")
def show_new_word() -> WordWithExplanation:
    with open(path_existing) as f:
        existing_words = set(json.load(f))
    with open(path_new) as f:
        words = [w for w, cnt in json.load(f).items() if w not in existing_words]
    if len(words) == 0:
        return WordWithExplanation(word="No new words", explanation="")
    else:
        word = random.choice(words)
    explanation = Translator.translate(word, update_dict=False)
    return WordWithExplanation(word=word, explanation=explanation)

