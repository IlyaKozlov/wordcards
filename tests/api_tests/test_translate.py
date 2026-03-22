import requests
import pytest
from utils_for_test import service_running


@pytest.mark.skipif(not service_running(), reason="service not running")
def test_translate() -> None:
    url = "http://localhost:2218/translate?uid=test"
    response = requests.get(url)
    assert response.status_code == 200


@pytest.mark.skipif(not service_running(), reason="service not running")
def test_translate_word() -> None:
    url = "http://localhost:2218/translate/translate"
    data = {"word": "friends"}
    response = requests.post(url, data=data, stream=True)
    assert response.status_code == 200
    count = 0
    for chunk in response.iter_content(chunk_size=1024):
        # Process each chunk (e.g., print it or save it)
        count += 1
    assert count > 0
