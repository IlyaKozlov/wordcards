import json
import logging
import random
import sys
from pathlib import Path


import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from logging import getLogger

from db_module import TaskDatabase


logger = getLogger(__name__)


def setup_logging():
    handler = logging.StreamHandler(sys.stderr)
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


app = FastAPI()


@app.get("/")
def root():
    path = Path(__file__).parent.parent / "db" / "words.json"
    with open(path) as f:
        words = json.load(f)
    words = random.sample(words, 4)
    right_answer_id = random.choice(list(range(len(words))))
    right_answer = words[right_answer_id]

    with TaskDatabase() as db:
        uid = db.add_answer(f"word{right_answer_id}")

    task = {
          "uid": str(uid),
          "translation": right_answer["translation"],
          "word1": words[0]["word"],
          "word2": words[1]["word"],
          "word3": words[2]["word"],
          "word4": words[3]["word"]
        }

    with open(Path(__file__).parent / "htmls" / "some_html.html") as file:
        content = file.read().replace(
            "JSON_TASK", json.dumps(task, indent=4)
        )
        return HTMLResponse(content=content, status_code=200)


class Answer(BaseModel):
    uuid: str
    chosen: str


@app.post("/answer")
def check_answer(answer: Answer):
    with TaskDatabase() as db:
        true_answer = db.get_answer(answer.uuid)
        if true_answer == answer.chosen:
            logger.info(f"Answer {answer.chosen} {answer.uuid} is correct")
            return True
    logger.info(f"Answer {answer.chosen} {answer.uuid} is incorrect")
    return False


if __name__ == "__main__":
    setup_logging()
    uvicorn.run(host="0.0.0.0", port=1155, app=app)
