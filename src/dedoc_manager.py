import json
import logging
import os
from pathlib import Path
from typing import List

import requests

from llm.llm_model import LLMModel

logger = logging.getLogger(__name__)


class DedocManager:

    max_size = 16000

    def handle(self, file: Path) -> List[str]:
        url = os.path.join(os.getenv("DEDOC_URL", "http://localhost:1231"), "upload")
        with open(file, "rb") as f:
            response = requests.post(
                url,
                files={'file': (file.name, f)}, data={"structure_type": "linear"}
            )
        document = response.json()
        structure = document["content"]["structure"]
        stack = [structure]
        result = []
        batch = []
        while stack:
            item = stack.pop()
            batch.append(item["text"])
            stack += reversed(item["subparagraphs"])
            if sum(map(len, batch)) >= self.max_size:
                result.append("".join(batch))
                batch = []
        if batch:
            result.append("".join(batch))
        return result


if __name__ == '__main__':
    items = (DedocManager().handle(
        Path("/media/padre/0123-4567/yandex/ooks/history/shortestHistory/shortestHistoryUniverse.pdf")
    ))
    model = LLMModel.from_env()
    for item in items:
        prefix = "Convert each word to the normal form, for example did -> do, cats -> cat, men -> man\n"
        prefix += "Drop all punctuations and numbers"
        prompt = prefix + item
        answer = model.invoke(prompt)
        path = "/home/padre/rojects/learn/wordcards/db/dictionary.json"
        with open(path) as f:
            d = json.load(f)
        k = 0
        n = 0
        words = sorted(set(answer.split()))
        for word in words:
            k += word.lower() in d
            n += 1
        logger.info(k, n, k / n)
        pass
