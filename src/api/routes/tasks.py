import random
import uuid
from http.client import HTTPException
from pathlib import Path

from fastapi import Form
from fastapi.routing import APIRouter
from starlette.responses import HTMLResponse

from db.task_db import TaskDB
from schemas.tasks.task_status import TaskStatus
from schemas.tasks.word2explanation import Word2Explanation
from task_generator import TaskGenerator

tasks = APIRouter()
db = TaskDB()
generator = TaskGenerator()


@tasks.get("/tasks")
def get_new_task() -> Word2Explanation:
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
    with open(Path(__file__).parent / "task.html", "r") as f:
        code = f.read()
    return HTMLResponse(code)

