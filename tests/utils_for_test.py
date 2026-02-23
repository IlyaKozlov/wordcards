import os
import shutil
from pathlib import Path
import pytest
import zipfile


@pytest.fixture
def fill_db():
    db_path = Path(__file__).parent.parent / "db"
    db_path_uid = db_path / "test"
    if db_path_uid.exists():
        shutil.rmtree(db_path_uid)
    os.makedirs(db_path, exist_ok=True)
    archive_path = Path(__file__).parent / "test.zip"

    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        zip_ref.extractall(db_path)
    yield
    if db_path_uid.exists():
        shutil.rmtree(db_path_uid)


if __name__ == '__main__':
    fill_db()
