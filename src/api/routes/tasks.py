from pathlib import Path
from typing import Optional

from fastapi import Query, Body
from fastapi.routing import APIRouter
from starlette.responses import HTMLResponse

from db.task_db import TaskDB
from schemas.tasks.match_word2audio import MatchWordAudio
from schemas.tasks.match_word_explanation import MatchWordExplanation
from schemas.tasks.no_new_words import NoNewWords
from schemas.tasks.sentence_with_placeholder import SentenceWithPlaceholder
from schemas.tasks.word2explanation import Word2Explanation
from schemas.tasks.word_statistics_update import WordsStatisticUpdate
from generator.tasks.task_generator import TaskGenerator

tasks = APIRouter()


htmls_path = Path(__file__).parent.parent.parent / "static"


@tasks.get("/tasks")
def get_new_task(
    uid: str = Query(),
    task_type: Optional[str] = Query(default=None),
) -> Word2Explanation | SentenceWithPlaceholder | MatchWordExplanation | MatchWordAudio | NoNewWords:
    generator = TaskGenerator(uid)
    if task_type is not None and task_type.strip() == "":
        task_type = None
    return generator.new_task(task_type)


@tasks.post("/update_statistics")
def update_statistics(
        uid: str = Query(),
        statistics: WordsStatisticUpdate = Body(),
) -> str:
    db = TaskDB(uid)
    db.update_task_statistic(statistics)
    return "ok"


@tasks.get("")
def task(uid: str = Query(), ) -> HTMLResponse:
    with open(htmls_path / "task.html", "r", encoding="utf-8") as f:
        code = f.read()
    return HTMLResponse(code)


@tasks.get("/task_word2explanation")
def task_word2explanation(uid: str = Query(), ) -> HTMLResponse:
    with open(htmls_path / "task_word2explanation.html", "r", encoding="utf-8") as f:
        code = f.read()
    return HTMLResponse(code)


@tasks.get("/task_other")
def task_other(uid: str = Query(), ) -> HTMLResponse:
    with open(htmls_path / "task_typing.html", "r", encoding="utf-8") as f:
        code = f.read()
    return HTMLResponse(code)
