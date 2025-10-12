import json
import logging
from pathlib import Path

from fastapi import Form, BackgroundTasks
from fastapi.routing import APIRouter
from starlette.responses import HTMLResponse
from tqdm import tqdm

from db.word_db import WordDB
from generator.generate_word_explanation import GenerateWordExplanation
from generator.translator import Translator
from paths import path_existing, path_known
from schemas.word_with_explanation import WordWithExplanation
from schemas.words_statistic import WordsStatistic

uncover = APIRouter()
logger = logging.getLogger(__name__)

database = WordDB()


@uncover.get("")
def html_form() -> HTMLResponse:
    path = Path(__file__).parent / "form.html"
    with open(path) as file:
        code = file.read()
    return HTMLResponse(content=code)


@uncover.get("/translate_all")
def translate_in_advance() -> str:
    words = database.get_new_words()
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


@uncover.post("/save_word")
def save_word(word: str = Form(), *, background_tasks: BackgroundTasks) -> str:
    def save():
        logger.info(f"Start saving word {word}")
        database.save_word_explanation(word, [])
        generator = GenerateWordExplanation()
        explanations = generator.generate_word_explanation(word)
        database.save_word_explanation(word, explanations)
        logger.info(f"Saved word {word}")

    background_tasks.add_task(save)
    return "Ok"


@uncover.post("/mark_as_known")
def mark_as_known(
    word: str = Form(...),
) -> str:
    database.save_know_word(word)
    return "Ok"


@uncover.get("/show_new_word")
def show_new_word() -> WordWithExplanation:
    words = database.get_new_words(min_cnt=1)
    n_known_words = database.get_n_know_word()
    statistics = WordsStatistic(n_words=len(words), n_uncovered_words=n_known_words)
    if len(words) == 0:
        return WordWithExplanation(
            word="No new words",
            explanation="",
            words_statistics=statistics,
        )
    else:
        word = words[0]
    explanation = Translator().translate(word, update_cnt=False)
    return WordWithExplanation(
        word=word,
        explanation=explanation,
        words_statistics=statistics,
    )
