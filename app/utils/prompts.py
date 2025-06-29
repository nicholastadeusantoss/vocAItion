import os

PROMPTS_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts")

def get_prompt(prompt_filename: str) -> str:
    prompt_path = os.path.join(PROMPTS_PATH, prompt_filename)
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()
