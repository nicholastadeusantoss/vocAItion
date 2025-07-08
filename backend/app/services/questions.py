import re
from app.utils.openai_client import call_openai
from app.utils.prompts import get_prompt


def generate_experience_questions(description: str) -> str:
    prompt = get_prompt("experience_questions_prompt.txt").replace("{text}", description.strip())
    return call_openai(prompt)


