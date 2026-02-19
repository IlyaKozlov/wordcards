import requests

from scripts.translate import response


def test_show_new_woed():
    params = {"uid": "test"}
    response = requests.get("http://localhost:2218/uncover/show_new_word", params= params)
    response.raise_for_status()
    data = response.json()

    assert "word" in data
    assert data["word"] in ["red","blue","green","gray"]
