from app.utils.openai_client import call_openai
from app.utils.prompts import get_prompt

def generate_experience_questions(description: str) -> str:
    prompt = get_prompt("experience_questions_prompt.txt").replace("{text}", description.strip())
    return call_openai(prompt)

def improve_experience_with_answers(description: str, answers: str) -> str:
    prompt = get_prompt("experience_improve_prompt.txt")
    prompt = prompt.replace("{original}", description.strip()).replace("{answers}", answers.strip())
    return call_openai(prompt)

def extract_experiences_with_ai(resume_text: str) -> list[str]:
    prompt_template = get_prompt("experience_extract_prompt.txt")
    prompt = prompt_template.replace("{text}", resume_text.strip())

    response_text = call_openai(prompt)

    # The response is expected to be a numbered list. We'll split and clean it.
    experiences = []
    for line in response_text.split("\n"):
        line = line.strip()
        if line and (line[0].isdigit() and (line[1] == "." or line[2] == ".")):
            # Remove the number at the beginning, e.g., "1. ..."
            experience = line.split(".", 1)[1].strip()
            experiences.append(experience)
    return experiences
