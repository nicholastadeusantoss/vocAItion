import re
from app.utils.openai_client import call_openai
from app.utils.prompts import get_prompt


def extract_experiences_with_ai(resume_text: str) -> list[str]:
    prompt_template = get_prompt("experience_extract_prompt.txt")
    prompt = prompt_template.replace("{text}", resume_text.strip())

    response_text = call_openai(prompt)

    experiences = []
    for line in response_text.split("\n"):
        line = line.strip()
        if line and (line[0].isdigit() and (line[1] == "." or line[2] == ".")):
            experience = line.split(".", 1)[1].strip()
            experiences.append(experience)
    return experiences
