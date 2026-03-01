from db.task_db import TaskDB
from schemas.tasks.word_statistics_update import (
    WordsStatisticUpdate,
    WordStatisticUpdate,
)
from utils_for_test import fill_db  # noqa


def test_get_four_words(fill_db: None) -> None:
    task_db = TaskDB(user_id="test")
    words = task_db.get_four_words()
    assert len(words) == 4


def test_update_task_statistic(fill_db: None) -> None:
    task_db = TaskDB(user_id="test")
    for is_true in (True, False):
        task_db.update_task_statistic(
            WordsStatisticUpdate(
                statistics=[
                    WordStatisticUpdate(
                        word="one",
                        is_true=is_true,
                    )
                ],
            )
        )
