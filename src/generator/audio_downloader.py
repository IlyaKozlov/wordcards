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
                    if phonetic.get("audio"):
                        return phonetic.get("audio")
        wiktionary_url = self._get_audio_url_wiktionary(normalized)
        if wiktionary_url:
            return wiktionary_url
        return transcription

    @staticmethod
    def _normalize_word(word: str) -> Optional[str]:
        word = word.strip().lower()
        if len(word.split()) != 1 or len(word) == 0:
            return None
        return word

    # Returns Optional[str] (None if no audio found)
    # Uses the Wiktionary MediaWiki API (no HTML parsing).

    from typing import Optional
    import requests

    API_URL = "https://en.wiktionary.org/w/api.php"
    USER_AGENT = "word-audio-fetcher/1.0 (https://example.com)"

    def _get_audio_url_wiktionary(self, word: str) -> Optional[str]:
        """
        Query the Wiktionary API for files used on the page for `word`,
        prefer audio file extensions and return the direct upload.wikimedia.org URL
        for the first matching audio file found. Returns None if no audio is found.
        """
        session = requests.Session()
        session.headers.update({"User-Agent": self.USER_AGENT})

        # 1) Ask the parse endpoint for the list of files/images used on the page
        try:
            resp = session.get(
                self.API_URL,
                params={"action": "parse", "page": word, "prop": "images", "format": "json"},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException:
            return None

        # If page doesn't exist or parse failed
        images = data.get("parse", {}).get("images", [])
        if not images:
            return None

        # Audio file extensions to consider (common ones on Wiktionary)
        audio_exts = (".ogg", ".oga", ".mp3", ".wav", ".flac", ".m4a")

        # Heuristic scoring to prefer likely pronunciation audio files
        def score_name(name: str) -> int:
            n = name.lower()
            score = 0
            if any(n.endswith(ext) for ext in audio_exts):
                score += 100
            if "pron" in n or "audio" in n or "pronunciation" in n:
                score += 10
            if "-en" in n or "_en" in n or n.startswith("en-") or "us" in n or "uk" in n:
                score += 5
            return score

        # Sort images by descending score so we try most likely ones first
        images_sorted = sorted(images, key=score_name, reverse=True)

        # 2) For each candidate file, request imageinfo to get the direct URL
        for img_name in images_sorted:
            # skip non-audio if low confidence
            if not any(img_name.lower().endswith(ext) for ext in audio_exts):
                # still allow if name contains 'pron' or 'audio' but no known ext (rare)
                if not any(k in img_name.lower() for k in ("pron", "audio")):
                    continue

            file_title = f"File:{img_name}"
            try:
                resp2 = session.get(
                    self.API_URL,
                    params={
                        "action": "query",
                        "titles": file_title,
                        "prop": "imageinfo",
                        "iiprop": "url",
                        "format": "json",
                    },
                    timeout=10,
                )
                resp2.raise_for_status()
                data2 = resp2.json()
            except requests.RequestException:
                continue

            pages = data2.get("query", {}).get("pages", {})
            for page in pages.values():
                imageinfo = page.get("imageinfo")
                if imageinfo and isinstance(imageinfo, list) and imageinfo:
                    url = imageinfo[0].get("url")
                    if url and "upload.wikimedia.org" in url:
                        return url

        # Nothing found
        return None
