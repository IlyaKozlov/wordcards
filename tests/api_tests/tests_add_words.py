import requests
from tempfile import TemporaryDirectory
from pathlib import Path


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
