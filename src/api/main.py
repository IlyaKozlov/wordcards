import logging
import sys
from logging import getLogger

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from api.routes.uncover import uncover

logger = getLogger(__name__)


def setup_logging():
    handler = logging.StreamHandler(sys.stderr)
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(uncover, prefix="/uncover")


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
    uvicorn.run(host="0.0.0.0", port=1155, app=app)
