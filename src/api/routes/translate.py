from pathlib import Path
from typing import Optional

from fastapi import Form, Query
from fastapi.routing import APIRouter
from fastapi.responses import StreamingResponse, HTMLResponse

from generator.translator_stream import TranslatorStream

translate_route = APIRouter()


@translate_route.get("/")
def html_form(
    uid: str = Query(),
) -> HTMLResponse:
    path = Path(__file__).parent / "translate_form.html"
    assert path.is_file()
    with open(path) as file:
        html = file.read()
    return HTMLResponse(content=html)


@translate_route.post("/translate")
def translate(word: str = Form(), uid: Optional[str] = Query(None)) -> StreamingResponse:
    translator = TranslatorStream.from_env(uid)
    translation = translator.handle(word)
    return StreamingResponse(content=(_.model_dump_json() + "\n" for _ in translation))
