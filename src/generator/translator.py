import json
import logging
import shutil
from pathlib import Path

from generator.generate_word_explanation import GenerateWordExplanation
from paths import dictionary_path, path_new

logger = logging.getLogger(__name__)


class Translator:

    def __init__(self):
        self.cache_miss_cnt = 0
        self.call_cnt = 0

    def translate(self, word: str, update_cnt: bool = True) -> str:
        self.call_cnt += 1
        with open(dictionary_path) as f:
            d = json.load(f)
        normalized = word.strip().lower()
        if normalized not in d:
            self.cache_miss_cnt += 1
            explanations = GenerateWordExplanation().generate_word_explanation(word)
            res = ""
            for explanation in explanations:
                res += f"{explanation.explanation}\n"
                res += f"{explanation.translation}\n"
            d[normalized] = res
            dictionary_path_tmp = Path(str(dictionary_path) + ".tmp")
            with open(dictionary_path_tmp, "w") as out:
                json.dump(fp=out, obj=d, ensure_ascii=False, indent=4)
            shutil.move(dictionary_path_tmp, dictionary_path)
        else:
            logger.info(f"Cache miss from dictionary ({word})")
            res = d[word]
        if update_cnt:
            with open(path_new) as inp:
                new_words = json.load(inp)
            new_words[normalized] = new_words.get(normalized, 0) + 1
            with open(path_new, "w") as out:
                json.dump(obj=new_words, fp=out, indent=4)
        return res
