import logging
import os
from typing import List

from openai import OpenAI
from pydantic import SecretStr

logger = logging.getLogger(__name__)


class LLMModel:

    _token_in_cache_price = 0.07 / 1e6
    _token_in_cache_miss_price = 0.27 / 1e6
    _token_out_price = 1.1 / 1e6

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
        token_in_cache = response.usage.prompt_cache_hit_tokens
        token_in_cache_miss = response.usage.prompt_cache_miss_tokens
        token_out = response.usage.completion_tokens
        price = (
                token_in_cache * self._token_in_cache_price +
                token_in_cache_miss * self._token_in_cache_miss_price +
                token_out * self._token_out_price
                 )
        logger.info(price)
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

