import logging
import tempfile
from collections import Counter
from pathlib import Path

from fastapi import UploadFile, File, Query
from fastapi.routing import APIRouter
from tqdm import tqdm

from api.routes.uncover import database
from db.word_db import WordDB
from dedoc_manager import DedocManager
from generator.generate_word_explanation import GenerateWordExplanation
from generator.page_to_normalized import PageToNormalized
from generator.translator import Translator
from llm.llm_model import LLMModel

add_words = APIRouter()
logger = logging.getLogger(__name__)


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


@add_words.get("/translate_all")
def translate_in_advance(min_cnt: str = Query(default="10")) -> str:
    words = database.get_new_words(min_cnt=int(min_cnt))
    translator = Translator()
    for w in tqdm(words):
        logger.info(f"translate word in advance '{w}'")
        translator.translate(w, update_cnt=False)
        logger.info(f"translate word in advance done '{w}'")
        logger.info(
            f"cache miss rate:"
            f" {translator.cache_miss_cnt / translator.call_cnt:0.2f} "
            f"({translator.cache_miss_cnt} of {translator.call_cnt})"
        )
    return f"translated {len(words)} words"


@add_words.get("/fix_learning_words")
def translate_in_advance() -> str:
    words = database.get_learning_words()
    broken = [k for k, v in words.items() if len(v) == 0]
    generator = GenerateWordExplanation()
    for w in tqdm(broken, desc="Fix word explanation"):
        explanation = generator.generate_word_explanation(w)
        database.save_word_explanation(w, explanation)
    return f"fix {len(broken)} words"
