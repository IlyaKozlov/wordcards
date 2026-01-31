from logging import getLogger
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.routes.add_words import add_words
from api.routes.database_route import db_route
from api.routes.tasks import tasks
from api.routes.translate import translate_route
from api.routes.uncover import uncover
from utils import setup_logging

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

static_path = Path(__file__).parent.parent / "static"
app.mount("/static", StaticFiles(directory=static_path), name="static")

app.include_router(uncover, prefix="/uncover", tags=["uncover"])
app.include_router(add_words, prefix="/add_words", tags=["add_words"])
app.include_router(translate_route, prefix="/translate", tags=["translate"])
app.include_router(tasks, prefix="/tasks", tags=["tasks"])
app.include_router(db_route, prefix="/backups", tags=["backups"])


@app.get("/")
def root() -> HTMLResponse:
    with open(static_path / "main.html") as out:
        code = out.read()
    return HTMLResponse(code)


@app.get("/favicon.ico")
def icon() -> FileResponse:
    path: Path = Path(__file__).parent / "icon.ico"
    return FileResponse(path, media_type="image/x-icon")


if __name__ == "__main__":
    setup_logging()
    logger.info("Starting uvicorn")
    uvicorn.run(host="0.0.0.0", port=2218, app=app)
