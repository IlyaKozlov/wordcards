import logging
import os
from pathlib import Path
from typing import List

import requests

logger = logging.getLogger(__name__)


class DedocManager:

    max_size = 4096

    def handle(self, file: Path) -> List[str]:
        if file.name.lower().endswith(".txt"):
            return self._handle_txt_file(file)

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

    def _handle_txt_file(self, file: Path) -> List[str]:
        result = []

        batch = []
        batch_size = 0
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                if len(line) + batch_size > self.max_size:
                    result.append("".join(batch))
                    batch = []
                    batch_size = 0
                batch.append(line)
                batch_size += len(line)
        if len(batch) > 0:
            result.append("".join(batch))
        return result
