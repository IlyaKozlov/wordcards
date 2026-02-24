import os.path
import tempfile
import zipfile

import requests


def test_backups() -> None:
    response = requests.get("http://localhost:2218/backups")
    response.raise_for_status()
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "fluffy.zip")
        with open(zip_path, "wb") as fluffy:
            fluffy.write(response.content)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.namelist()
