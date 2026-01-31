import logging
import os
from typing import Iterator

from openai import OpenAI
from pydantic import SecretStr

from llm.llm_model_cache import LLMCache
from llm.llm_utils import get_hash

logger = logging.getLogger(__name__)


class LLMModel:

    _token_in_cache_price = 0.07 / 1e6
    _token_in_cache_miss_price = 0.27 / 1e6
    _token_out_price = 1.1 / 1e6

    def __init__(self, key: SecretStr) -> None:
        self.key = key
        base_url = "https://api.deepseek.com"
        self._model = OpenAI(api_key=key.get_secret_value(), base_url=base_url)
        self.cache = LLMCache()

    def invoke(self, prompt: str) -> str:
        key = get_hash(prompt)
        cached_value = self.cache.get(key)
        if cached_value is None:
            value = self._call(prompt)
            self.cache.put(key, value)
            return value
        return cached_value

    def invoke_stream(self, prompt: str) -> Iterator[str]:
        key = get_hash(prompt)
        cached_value = self.cache.get(key)
        if cached_value is None:
            stream = self._call_stream(prompt)
            value = ""
            for item in stream:
                value += item
                yield item
            self.cache.put(key, value)
        else:
            yield from cached_value

    def _call(self, prompt: str) -> str:
        response = self._model.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a native english speaker"},
                {"role": "user", "content": prompt},
            ],
            stream=False,
        )
        token_in_cache = response.usage.prompt_cache_hit_tokens
        token_in_cache_miss = response.usage.prompt_cache_miss_tokens
        token_out = response.usage.completion_tokens
        price = (
            token_in_cache * self._token_in_cache_price
            + token_in_cache_miss * self._token_in_cache_miss_price
            + token_out * self._token_out_price
        )
        logger.info(price)
        return response.choices[0].message.content

    def _call_stream(self, prompt: str) -> Iterator[str]:
        response = self._model.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a native english speaker"},
                {"role": "user", "content": prompt},
            ],
            stream=True,
        )
        for item in response:
            yield "".join(_.delta.content for _ in item.choices)

    @staticmethod
    def from_env() -> "LLMModel":
        key = SecretStr(os.getenv("LLM_API_KEY_DS"))
        return LLMModel(key)
