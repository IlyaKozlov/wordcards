import json
import tempfile
from collections import Counter
from pathlib import Path

from fastapi import Query
from fastapi.responses import StreamingResponse
from fastapi.routing import APIRouter
from tqdm import tqdm

from dedoc_manager import DedocManager
from llm.llm_model import LLMModel
from generator.page_to_normalized import PageToNormalized
from paths import path_new

translate_route = APIRouter()


@translate_route.get("/word")
def add_book(word: str = Query()) -> StreamingResponse:
    dm = DedocManager()
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        file_path = tmpdir / file.filename
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        pages = dm.handle(file=file_path)

    normalizer = PageToNormalized(llm_model=LLMModel.from_env())
    with open(path_new, "r") as file:
        all_words = json.load(file)
    for page in tqdm(pages):
        if not page:
            continue
        normalized_page = normalizer.normalize_page(page)
        for word in normalized_page.lower().split():
            all_words[word] = 1 + all_words.get(word, 0)
    with open(path_new, "w") as file:
        json.dump(obj=Counter(all_words), fp=file, indent=4)
    return "Ok"
