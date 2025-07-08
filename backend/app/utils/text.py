import re
from app.utils.openai_client import call_openai
from app.utils.prompts import get_prompt

def parse_numbered_questions(text: str) -> list[str]:
    """
    Extrai perguntas numeradas de uma string (e.g. '1. Pergunta\n2. Pergunta...')
    """
    raw_questions = re.split(r'\n?\s*\d+[\.\)]\s*', text)
    return [q.strip() for q in raw_questions if q.strip()]