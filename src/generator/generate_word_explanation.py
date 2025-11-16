import json
from pathlib import Path
from typing import List

from llm.llm_model import LLMModel
from llm.llm_utils import get_code_blocs
from schemas.word_explanation import WordExplanation


class GenerateWordExplanation:

    def __init__(self):
        self.model = LLMModel.from_env()

    def generate_word_explanation(self, word: str) -> List[WordExplanation]:
        path = Path(__file__).parent / "prompt.txt"
        template = path.read_text()
        prompt = template.replace("WORD", word)
        result = self.model.invoke(prompt)
        blocks = get_code_blocs(result)
        block = blocks[0]
        raw_json = json.loads(block)
        result = []
        for d in raw_json:
            d["word"] = word
            result.append(WordExplanation.model_validate(d))
        return result
