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

tasks = APIRouter()
db = TaskDB()


@tasks.get("/tasks")
def get_new_task() -> Word2Explanation:
    items = db.get_four_words()
    if items is None or len(items) != 4:
        raise HTTPException("Not enough items to fetch new task")
    right_answer_id = random.choice(range(len(items)))
    task_id = str(uuid.uuid4())
    db.save_task(
        task_id=task_id,
        word=items[right_answer_id].word,
        explanation=items[right_answer_id].word + "\n" + items[right_answer_id].explanation,
        right_answer=str(right_answer_id + 1),
    )
    return Word2Explanation(
        task_id=task_id,
        word1=items[0].word,
        word2=items[1].word,
        word3=items[2].word,
        word4=items[3].word,
        explanation=items[right_answer_id].explanation,
    )


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

