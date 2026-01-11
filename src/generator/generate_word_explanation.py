import json
import logging
from json import JSONDecodeError
from pathlib import Path
from typing import List

from pydantic.v1 import JsonError

from llm.llm_model import LLMModel
from llm.llm_utils import get_code_blocs, fix_json
from schemas.word_explanation import WordExplanation


class GenerateWordExplanation:

    def __init__(self):
        self.model = LLMModel.from_env()
        self.logger = logging.getLogger(__name__)

    def generate_word_explanation(self, word: str) -> List[WordExplanation]:
        path = Path(__file__).parent / "prompt.txt"
        template = path.read_text()
        prompt = template.replace("WORD", word)
        result = self.model.invoke(prompt)

        blocks = get_code_blocs(result)
        if len(blocks) > 0:
            block = blocks[0]
        else:
            block = result
        try:
            raw_json = json.loads(block)
        except JSONDecodeError as err:
            self.logger.error(f"Error while parsing json: '{err}', try to fix")
            text_fixe = fix_json(
                text=block,
                model=self.model,
                error=err,
            )
            blocks = get_code_blocs(text_fixe)
            if len(blocks) > 0:
                block = blocks[0]
            else:
                block = text_fixe
            raw_json = json.loads(block)
        result = []
        for d in raw_json:
            d["word"] = word
            result.append(WordExplanation.model_validate(d))
        return result
