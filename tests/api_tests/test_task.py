import requests

from schemas.tasks.uncover_task import UncoverTask
from utils_for_test import fill_db  # noqa

from schemas.tasks.match_word_explanation import MatchWordExplanation
from schemas.tasks.sentence_with_placeholder import SentenceWithPlaceholder
from schemas.tasks.word2explanation import Word2Explanation

base_url = "http://localhost:2218"


def test_filldb() -> None:
    for word in ["one", "two", "three", "four", "five"]:
        data = {"word": word}
        params = {"uid": "test_user"}
        url = f"{base_url}/uncover/save_word"
        response = requests.post(url, params=params, data=data)
        response.raise_for_status()


def test_tasks(fill_db: None) -> None:
    params = {"uid": "test"}
    _get_tasks(params)


def test_task_type(fill_db: None) -> None:
    params = {"uid": "test", "task_type": "MatchWordExplanation"}
    raw_answer = _get_tasks(params)
    MatchWordExplanation.model_validate(raw_answer)


def test_uncover_task(fill_db: None) -> None:
    params = {"uid": "test", "task_type": "UncoverTask"}
    raw_answer = _get_tasks(params)
    UncoverTask.model_validate(raw_answer)


def test_task_type1(fill_db: None) -> None:
    params = {"uid": "test", "task_type": "SentenceWithPlaceholder"}
    raw_answer = _get_tasks(params)
    SentenceWithPlaceholder.model_validate(raw_answer)


def test_task_type2(fill_db: None) -> None:
    params = {"uid": "test", "task_type": "Word2Explanation"}
    raw_answer = _get_tasks(params)
    Word2Explanation.model_validate(raw_answer)


def _get_tasks(params: dict) -> dict:
    response = requests.get("http://localhost:2218/tasks/tasks", params=params)
    response.raise_for_status()
    raw_answer = response.json()
    return raw_answer
