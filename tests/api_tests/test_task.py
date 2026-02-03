import requests
import pytest
from pathlib import Path
from shutil import rmtree

base_url = "http://localhost:2218"
@pytest.fixture
def fill_db():

    for word in ["one", "two", "three", "four", "five"]:
        data = {"word":word}
        params = {"uid": "test_user"}
        url = f"{base_url}/uncover/save_word"
        response = requests.post(url, params = params, data = data)
        response.raise_for_status()
    yield
    rmtree(Path(__file__).parent.parent.parent / "db" / "test_user")

def test_filldb(fill_db):
    pass
