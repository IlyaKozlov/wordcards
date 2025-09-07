from logging import getLogger
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routes.add_words import add_words
from api.routes.translate import translate_route
from api.routes.uncover import uncover
from utils import setup_logging
from dotenv import load_dotenv

logger = getLogger(__name__)
load_dotenv(Path(__file__).parent.parent.parent / ".env")


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(uncover, prefix="/uncover")
app.include_router(add_words, prefix="/add_words")
app.include_router(translate_route, prefix="/translate")


@app.get("/")
def root():
    return "Hi"


# class Answer(BaseModel):
#     uuid: str
#     chosen: str
#
#
# @app.post("/answer")
# def check_answer(answer: Answer):
#     with TaskDatabase() as db:
#         true_answer = db.get_answer(answer.uuid)
#         if true_answer == answer.chosen:
#             logger.info(f"Answer {answer.chosen} {answer.uuid} is correct")
#             return True
#     logger.info(f"Answer {answer.chosen} {answer.uuid} is incorrect")
#     return False
#
#
# @app.get("/translate")
# def translate(word: str) -> str:
#
#     return Translator.translate(word)


if __name__ == "__main__":
    setup_logging()
    logger.info("Starting uvicorn")
    uvicorn.run(host="0.0.0.0", port=1155, app=app)
