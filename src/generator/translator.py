import json
import logging

from generator.generate_word_explanation import GenerateWordExplanation
from paths import dictionary_path, path_new

logger = logging.getLogger(__name__)


class Translator:

    @staticmethod
    def translate(word: str, update_dict: bool = True) -> str:
        with open(dictionary_path) as f:
            d = json.load(f)
        normalized = word.strip().lower()
        if normalized not in d:
            explanations = GenerateWordExplanation().generate_word_explanation(word)
            res = ""
            for explanation in explanations:
                res += f"{explanation.explanation}\n"
                res += f"{explanation.translation}\n"
            d[normalized] = res
            with open(dictionary_path, "w") as out:
                json.dump(fp=out, obj=d, ensure_ascii=False, indent=4)
        else:
            logger.info("Cache miss from dictionary")
            res = d[word]
        if update_dict:
            with open(path_new) as inp:
                new_words = json.load(inp)
            new_words[normalized] = new_words.get(normalized, 0) + 1
            with open(path_new, "w") as out:
                json.dump(obj=new_words, fp=out, indent=4)
        return res
