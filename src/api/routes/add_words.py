import tempfile
from collections import Counter
from pathlib import Path

from fastapi import UploadFile, File
from fastapi.routing import APIRouter
from tqdm import tqdm

from db.word_db import WordDB
from dedoc_manager import DedocManager
from generator.page_to_normalized import PageToNormalized
from llm.llm_model import LLMModel

add_words = APIRouter()


@add_words.post("/add_book")
def add_book(file: UploadFile = File()) -> str:
    dm = DedocManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        file_path = tmpdir / file.filename
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        pages = dm.handle(file=file_path)

    normalizer = PageToNormalized(llm_model=LLMModel.from_env())
    all_words = Counter()
    for page in tqdm(pages):
        if not page:
            continue
        normalized_page = normalizer.normalize_page(page)
        for word in normalized_page.lower().split():
            all_words[word] += 1

    word_db = WordDB()
    word_db.update_existing_words(all_words)
    return f"Add {sum(all_words.values()):,d} ({len(all_words):,d} unique) words"
