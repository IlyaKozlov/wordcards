from pathlib import Path

from fastapi import Form
from fastapi.routing import APIRouter
from fastapi.responses import StreamingResponse, HTMLResponse

from generator.translator_stream import TranslatorStream

translate_route = APIRouter()


@translate_route.get("/")
def html_form() -> HTMLResponse:
    path = Path(__file__).parent / "translate_form.html"
    assert path.is_file()
    with open(path) as file:
        html = file.read()
    return HTMLResponse(content=html)


@translate_route.post("/translate")
def translate(word: str = Form()) -> StreamingResponse:
    translator = TranslatorStream.from_env()
    translation = translator.handle(word)
    return StreamingResponse(content=(_.model_dump_json() + "\n" for _ in translation))

