import re
from app.utils.openai_client import call_openai
from app.utils.prompts import get_prompt


def improve_experience_with_answers(description: str, answers: str) -> str:
    prompt = get_prompt("experience_improve_prompt.txt")
    prompt = prompt.replace("{original}", description.strip()).replace("{answers}", answers.strip())
    return call_openai(prompt)