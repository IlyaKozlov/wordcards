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
