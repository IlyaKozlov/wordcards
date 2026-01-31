import logging
from fastapi import Query
from pathlib import Path

from fastapi import Form, BackgroundTasks
from fastapi.routing import APIRouter
from starlette.responses import HTMLResponse

from db.word_db import WordDB
from generator.generate_word_explanation import GenerateWordExplanation
from generator.translator import Translator
from schemas.word_with_explanation import WordWithExplanation
from schemas.words_statistic import WordsStatistic

uncover = APIRouter()
logger = logging.getLogger(__name__)


@uncover.get("")
def html_form(uid: str = Query(default=None)) -> HTMLResponse:
    path = Path(__file__).parent / "form.html"
    with open(path) as file:
        code = file.read()
    return HTMLResponse(content=code)


@uncover.post("/save_word")
def save_word(
    uid: str = Query(default=None),
    word: str = Form(),
    *,
    background_tasks: BackgroundTasks,
) -> str:
    database = WordDB(uid)

    def save() -> None:
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
    uid: str = Query(default=None),
    word: str = Form(...),
) -> str:
    database = WordDB(uid)
    database.save_know_word(word)
    return "Ok"


@uncover.get("/show_new_word")
def show_new_word(uid: str = Query(default=None)) -> WordWithExplanation:
    database = WordDB(uid)
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
    explanation = Translator(uid).translate(word, update_cnt=False)
    return WordWithExplanation(
        word=word,
        explanation=explanation,
        words_statistics=statistics,
    )
