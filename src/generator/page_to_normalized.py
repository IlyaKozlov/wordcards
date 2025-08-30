from llm.llm_model import LLMModel


class PageToNormalized:

    def __init__(self, llm_model: LLMModel) -> None:
        self.llm_model = llm_model

    def normalize_page(self, page: str) -> str:
        return self.llm_model.invoke(_template.format(text=page))


_template = """
You are an english native speaker.

Given the page of text lead every word to it's normal form, for example
are -> be, words -> word, did -> do etc. Skip all the punctuations. 

Answer with the normalized text only

TEXT: 

```
{text}
``` 
"""