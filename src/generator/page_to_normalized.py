from llm.llm_model import LLMModel


class PageToNormalized:

    def __init__(self, llm_model: LLMModel) -> None:
        self.llm_model = llm_model

    def normalize_page(self, page: str) -> str:
        return self.llm_model.invoke(_template.format(text=page))


_template = """
You are an english native speaker.

Given the page of text lead every word to it's normal form, for example
are -> be, words -> word, did -> do etc. Skip all the punctuations, variables name, brackets and so on

Examples of normalized words
1. is -> be
2. running -> run
3. better -> good
4. children -> child
5. went -> go
6. eating -> eat
7. cars -> car
8. liked -> like
9. studying -> study
10. happier -> happy
11. knows -> know
12. talked -> talk
13. larger -> large
14. tried -> try
15. women -> woman

**Examples of "words" you need to drop:**

1. x_value -> drop, because it is a variable name
2. 2023 -> drop, it is a number
3. myVariable -> also drop


Answer with the normalized text only


Examples

Example1

**Original Text:**
The children are running in the park. They went to play with their
cars and liked the new swings. It is better to eat healthy food and
study regularly.

**Normalized Text:**
the child be run in the park they go to play with their car and like
the new swing it be good to eat healthy food and study regular

Example2
**Original Text:**
The algorithms are optimizing the x_value by calculating the iterations
needed. In 2023, the function generated data from various models.

**Normalized Text:**

the algorithm be optimize the by calculate the iteration need in
the the function generate data from various model


TEXT:

```
{text}
```
"""
