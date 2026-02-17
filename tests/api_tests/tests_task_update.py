import requests

from schemas.tasks.word_statistics_update import (
    WordsStatisticUpdate,
    WordStatisticUpdate,
)


def test_task_update():
    for is_true in [True, False]:
        statistics = [WordStatisticUpdate(word="mouse", is_true=is_true)]
        data = WordsStatisticUpdate(statistics=statistics)
        params = {"uid": "test"}
        response = requests.post(
        "http://0.0.0.0:2218/tasks/update_statistics",
        params=params,
        json=data.model_dump(),
        )
        response.raise_for_status()
        assert response.json() == "ok"
