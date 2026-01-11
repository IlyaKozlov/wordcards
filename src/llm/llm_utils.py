import hashlib
from typing import List
from uuid import UUID


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


def get_hash(text: str) -> UUID:
    calculator = hashlib.md5()
    calculator.update(text.encode("utf-8"))
    return UUID(calculator.hexdigest())

def fix_json(text: str, model: "LLMModel", error: Exception) -> str:
    prompt = f"""
    I've tried to read a json (see below) but got an error, please try to fix it 
    
    Exception:
    ```
    {error}
    ```
    
    Json:
    ```
    {text}
    ```    
    """
    answer = model.invoke(prompt)
    return answer
