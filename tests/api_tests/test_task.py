import time

import pytest
import requests
from pygments.lexer import words

from schemas.tasks.match_word_explanation import MatchWordExplanation


@pytest.fixture
def fill_db():
    params = {"uid": "test"}
    for word in ("one", "two", "tree", "for", "five"):
        data = {"word": word}
        response = requests.post(
            "http://localhost:2218/uncover/save_word", params=params, data=data
        )
        response.raise_for_status()
    time.sleep(1)
    yield


def test_smoke(fill_db: None) -> None:
    pass


def test_tasks(fill_db: None) -> None:
    params = {"uid": "test"}
    response = requests.get("http://localhost:2218/tasks/tasks", params=params)
    response.raise_for_status()


def test_task_type(fill_db: None) -> None:
    params = {"uid": "test", "task_type": "MatchWordExplanation"}
    response = requests.get("http://localhost:2218/tasks/tasks", params=params)
    response.raise_for_status()
    raw_answer = response.json()
    MatchWordExplanation.model_validate(raw_answer)
