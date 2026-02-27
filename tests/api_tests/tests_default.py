import requests


def test_root() -> None:
    response = requests.get("http://localhost:2218/")
    response.raise_for_status()


def test_favicon_ico() -> None:
    response = requests.get("http://localhost:2218/favicon.ico")
    response.raise_for_status()
