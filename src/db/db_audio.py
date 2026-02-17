import json
import logging
from typing import Dict, Optional

from db.db_abc import Database
from generator.audio_downloader import AudioDownloader


class AudioDB(Database):

    _downloader = AudioDownloader()
    _logger = logging.getLogger(__name__)

    def get_audio_url(self, word: str) -> Optional[str]:
        word2audio = self._word2audio()
        if word not in word2audio:
            try:
                url = self._downloader.get_audio_url(word)
            except Exception as e:
                self._logger.warning(f"Error while downloading audio for word '{word}': {e}")
                url = None
            if url is not None:
                word2audio[word] = url
            self.save_audio(word, url)
        return word2audio.get(word)

    def save_audio(self, word: str, url: str) -> None:
        word2audio = self._word2audio()
        word2audio[word] = url
        self.save_object(word2audio, self._path_audio)

    def _word2audio(self) -> Dict[str, str]:
        if not self._path_audio.is_file():
            with open(self._path_audio, "w") as file:
                json.dump({}, file)
            return {}
        with open(self._path_audio) as file:
            return json.load(file)
