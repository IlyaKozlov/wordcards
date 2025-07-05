import os
from typing import List

from openai import OpenAI
from pydantic import SecretStr


class LLMModel:

    def __init__(self, key: SecretStr):
        self.key = key
        base_url = "https://api.deepseek.com"
        self._model = OpenAI(api_key=key.get_secret_value(), base_url=base_url)

    def invoke(self, prompt: str) -> str:
        response = self._model.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a native english speaker"},
                {"role": "user", "content": prompt},
            ],
            stream=False
        )

        return response.choices[0].message.content

    @staticmethod
    def from_env() -> "LLMModel":
        key = SecretStr(os.getenv("LLM_API_KEY_DS"))
        return LLMModel(key)

    @staticmethod
    def get_code_blocs(text: str) -> List[str]:
        started = False
        result = []
        block = []
        for line in text.split("\n"):
            if line.startswith("```"):
                if started:
                    result.append("\n".join(block))
                started = not started
            elif started:
                block.append(line)
        return result

