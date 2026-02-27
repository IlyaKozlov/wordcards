import requests
from tempfile import TemporaryDirectory
from pathlib import Path
from utils_for_test import fill_db  # noqa


def test_add_word() -> None:
    params = {"uid": "test"}
    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        path = tmpdir / "book.txt"
        with open(path, "w", encoding="utf-8") as file:
            file.write("open this book and then read its all")
        with open(path, "rb") as file:
            response = requests.post(
                "http://localhost:2218/add_words/add_book",
                files={"file": (path.name, file)},
                params=params,
            )

    response.raise_for_status()
    assert response.json() == "Add 8 (8 unique) words"


def test_translate_all(fill_db: None) -> None:
    for params in [{"uid":"test"},{"uid":"test", "min_cnt":"10"}]:
        response = requests.get("http://localhost:2218/add_words/translate_all",params = params)
        response.raise_for_status()
    params = {"min_cnt":"10"}
    response = requests.get("http://localhost:2218/add_words/translate_all", params=params)
    assert response.status_code >= 400
