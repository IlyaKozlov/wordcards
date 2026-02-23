import requests
from utils_for_test import fill_db



def test_show_new_words(fill_db):
    params = {"uid": "test"}
    response = requests.get("http://localhost:2218/uncover/show_new_word", params= params)
    response.raise_for_status()
    assert  response.status_code == 200
    result = response.json()


    assert "word" in result
    assert len(result["word"])>0
