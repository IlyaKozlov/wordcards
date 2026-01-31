import requests


def test_translate():
    url = "http://localhost:2218/translate"
    response = requests.get(url)
    assert response.status_code == 200


def test_translate_word():
    url = "http://localhost:2218/translate/translate"
    data = {"word": "friends"}
    response = requests.post(url, data=data, stream=True)
    assert response.status_code == 200
    count = 0
    for chunk in response.iter_content(chunk_size=1024):
            # Process each chunk (e.g., print it or save it)
            count +=1
    assert count > 0