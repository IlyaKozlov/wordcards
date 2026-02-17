from typing import Optional

import requests


class AudioDownloader:

    _base_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"

    def get_audio_url(self, word: str) -> Optional[str]:
        normalized = self._normalize_word(word)
        if normalized is None:
            return None
        url = self._base_url + normalized
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        transcription = None
        if isinstance(data, list) and len(data) > 0:
            for item in data:
                if "phonetic" in item:
                    transcription = item.get("phonetic")
                for phonetic in item.get("phonetics", []):
                    if phonetic.get("audio") is not None:
                        return phonetic.get("audio")
        return transcription

    @staticmethod
    def _normalize_word(word: str) -> Optional[str]:
        word = word.strip().lower()
        if len(word.split()) != 1 or len(word) == 0:
            return None
        return word
