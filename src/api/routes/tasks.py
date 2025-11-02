import random
import uuid
from http.client import HTTPException
from pathlib import Path

from fastapi import Form
from fastapi.routing import APIRouter
from starlette.responses import HTMLResponse

from db.task_db import TaskDB
from schemas.tasks.match_word_explanation import MatchWordExplanation
from schemas.tasks.sentence_with_placeholder import SentenceWithPlaceholder
from schemas.tasks.task_status import TaskStatus
from schemas.tasks.word2explanation import Word2Explanation
from task_generator import TaskGenerator

tasks = APIRouter()
db = TaskDB()
generator = TaskGenerator()

htmls_path = Path(__file__).parent.parent / "static"


@tasks.get("/tasks")
def get_new_task() -> Word2Explanation | SentenceWithPlaceholder | MatchWordExplanation:
    return generator.new_task()


@tasks.post("/check")
def check_answer(answer: str = Form(), task_id: str = Form(...)) -> TaskStatus:
    status = db.get_task(task_id=task_id)
    if status.right_answer == answer:
        db.update_task_statistic(word=status.word, is_correct=True)
        return TaskStatus(is_true=True, explanation="")
    else:
        db.update_task_statistic(word=status.word, is_correct=False)
        return TaskStatus(is_true=False,
                          explanation=status.explanation)


@tasks.get("")
def task() -> HTMLResponse:
    with open(htmls_path / "task_experimental.html", "r") as f:
        code = f.read()
    return HTMLResponse(code)


@tasks.get("/task_experimental_word2explanation")
def task_experimental() -> HTMLResponse:
    with open(htmls_path / "task_experimental_word2explanation.html", "r") as f:
        code = f.read()
    return HTMLResponse(code)


@tasks.get("/task_experimental_other")
def task_experimental_other() -> HTMLResponse:
    with open(htmls_path / "task_experimental_other.html", "r") as f:
        code = f.read()
    return HTMLResponse(code)

