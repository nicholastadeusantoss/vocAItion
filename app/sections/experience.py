import re
from app.utils.openai_client import call_openai
from app.utils.prompts import get_prompt

def parse_numbered_questions(text: str) -> list[str]:
    """
    Extrai perguntas numeradas de uma string (e.g. '1. Pergunta\n2. Pergunta...')
    """
    raw_questions = re.split(r'\n?\s*\d+[\.\)]\s*', text)
    return [q.strip() for q in raw_questions if q.strip()]

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

    experiences = []
    for line in response_text.split("\n"):
        line = line.strip()
        if line and (line[0].isdigit() and (line[1] == "." or line[2] == ".")):
            experience = line.split(".", 1)[1].strip()
            experiences.append(experience)
    return experiences
