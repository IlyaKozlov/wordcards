from pathlib import Path
from typing import Optional

from fastapi import Query
from fastapi.routing import APIRouter
from starlette.responses import HTMLResponse

from db.task_db import TaskDB
from schemas.tasks.match_word_explanation import MatchWordExplanation
from schemas.tasks.sentence_with_placeholder import SentenceWithPlaceholder
from schemas.tasks.word2explanation import Word2Explanation
from schemas.tasks.word_statistics_update import WordsStatisticUpdate
from generator.tasks.task_generator import TaskGenerator

tasks = APIRouter()
db = TaskDB()
generator = TaskGenerator()

htmls_path = Path(__file__).parent.parent.parent / "static"


@tasks.get("/tasks")
def get_new_task(
    task_type: Optional[str] = Query(default=None),
) -> Word2Explanation | SentenceWithPlaceholder | MatchWordExplanation:
    if task_type is not None and task_type.strip() == "":
        task_type = None
    return generator.new_task(task_type)


@tasks.post("/update_statistics")
def update_statistics(statistics: WordsStatisticUpdate) -> str:
    for word in statistics:
        db.update_task_statistic(
            word=word.word,
            is_correct=word.is_true,
        )

    return "ok"


@tasks.get("")
def task() -> HTMLResponse:
    with open(htmls_path / "task.html", "r") as f:
        code = f.read()
    return HTMLResponse(code)


@tasks.get("/task_word2explanation")
def task() -> HTMLResponse:
    with open(htmls_path / "task_word2explanation.html", "r") as f:
        code = f.read()
    return HTMLResponse(code)


@tasks.get("/task_other")
def task_other() -> HTMLResponse:
    with open(htmls_path / "task_typing.html", "r") as f:
        code = f.read()
    return HTMLResponse(code)
