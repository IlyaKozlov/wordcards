import json
import logging
from pathlib import Path

from fastapi import Form, BackgroundTasks
from fastapi.routing import APIRouter
from starlette.responses import HTMLResponse
from tqdm import tqdm

from generator.translator import Translator
from paths import path_existing, path_new, path_known
from schemas.word_with_explanation import WordWithExplanation

uncover = APIRouter()
logger = logging.getLogger(__name__)


@uncover.get("")
def html_form() -> HTMLResponse:
    path = Path(__file__).parent / "form.html"
    with open(path) as file:
        code = file.read()
    return HTMLResponse(content=code)


@uncover.get("/translate_all")
def translate_in_advance() -> str:
    with open(path_existing) as f1, open(path_known) as f2:
        existing_words = set(json.load(f1)) | set(json.load(f2))
    with open(path_new) as f:
        words_cnt = [
            (w, cnt)
            for w, cnt in json.load(f).items()
            if w not in existing_words
            if len(w) > 0
            if any(_.isalpha() for _ in w)
            if cnt > 2
        ]
        words_cnt.sort(key=lambda x: x[1], reverse=True)
        words = [w for w, _ in words_cnt]

        translator = Translator()
        for w in tqdm(words):
            logger.info(f"translate word in advance '{w}'")
            translator.translate(w, update_cnt=False)
            logger.info(f"translate word in advance done '{w}'")
            logger.info(
                f"cache miss rate:"
                f" {translator.cache_miss_cnt / translator.call_cnt:0.2f} "
                f"({translator.cache_miss_cnt} of {translator.call_cnt})"
            )
        return f"translated {len(words)} words"


@uncover.post("/uncover_word")
def uncover_word(word: str = Form(), *, background_tasks: BackgroundTasks) -> str:
    def save():
        logger.info(f"Start saving word {word}")
        with open(path_existing) as file:
            ls = json.load(file)
        if word not in ls:
            ls.append(word)
        with open(path_existing, "w") as out:
            json.dump(obj=ls, fp=out, indent=4)
        logger.info(f"Saved word {word}")

    background_tasks.add_task(save)
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
def show_new_word(background_tasks: BackgroundTasks) -> WordWithExplanation:
    with open(path_existing) as f1, open(path_known) as f2:
        existing_words = set(json.load(f1)) | set(json.load(f2))
    with open(path_new) as f:
        words_cnt = [
            (w, cnt)
            for w, cnt in json.load(f).items()
            if w not in existing_words
            if len(w) > 0
            if any(_.isalpha() for _ in w)
        ]
        words_cnt.sort(key=lambda x: x[1], reverse=True)
        words = [w for w, _ in words_cnt]

    if len(words) == 0:
        return WordWithExplanation(word="No new words", explanation="")
    else:
        word = words[0]
    explanation = Translator().translate(word, update_cnt=False)
    return WordWithExplanation(word=word, explanation=explanation)
