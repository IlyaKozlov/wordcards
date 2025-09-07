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


if __name__ == '__main__':
    from dotenv import load_dotenv
    from tqdm import tqdm

    load_dotenv("/home/padre/rojects/learn/wordcards/.env")

    path = "/home/padre/rojects/learn/wordcards/db/existing_words.json"
    path_tmp = "/home/padre/rojects/learn/wordcards/db/existing_words.json.tmp"
    with open(path, "r") as f:
        existing_words = json.load(f)
    res = {}
    generator = GenerateWordExplanation()
    for word in tqdm(existing_words):
        explanation = generator.generate_word_explanation(word)
        for expl in explanation:
            if word not in res:
                res[word] = []
            res[word].append(expl.model_dump())
    with open(path_tmp, "w") as f:
        json.dump(obj=res, fp=f, indent=4, ensure_ascii=False)
