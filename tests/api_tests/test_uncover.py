import requests

from utils_for_test import fill_db  # noqa


def test_unc_with_db(fill_db: None) -> None:
    params = {"uid": "test"}
    response = requests.get("http://localhost:2218/uncover", params=params)
    response.raise_for_status()


def test_unc_without_db() -> None:
    params = {"uid": "test"}
    response = requests.get("http://localhost:2218/uncover", params=params)
    response.raise_for_status()


def test_save_word() -> None:
    params = {"uid":"test"}
    data = {"word": "orange"}
    response = requests.post("http://localhost:2218/uncover/save_word", params = params, data = data)
    response.raise_for_status()
    assert response.json() == "Ok"


def test_save_word_ecs() -> None:
    url = "http://localhost:2218/uncover/save_word"
    params = {"uid": "test"}
    data = {"word": "red"}
    response = requests.post(url, data = data)
    assert response.status_code == 422
    response = requests.post(url, params = params)
    assert response.status_code == 422
    response = requests.post(url)
    assert response.status_code == 422


def test_show_new_words(fill_db):  # noqa
    params = {"uid": "test"}
    response = requests.get("http://localhost:2218/uncover/show_new_word", params= params)
    response.raise_for_status()
    assert response.status_code == 200
    result = response.json()

    assert "word" in result
    assert len(result["word"]) > 0


def test_mark_as_known() -> None:
    params = {"uid": "test"}
    data = {"word":"taste"}
    response = requests.post("http://localhost:2218/uncover/mark_as_known", params = params, data = data)
    response.raise_for_status()
    assert response.json() == "Ok"
