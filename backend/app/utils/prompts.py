import os

def get_prompt(filename: str) -> str:
    base_dir = os.path.dirname(__file__)
    prompts_dir = os.path.abspath(os.path.join(base_dir, "..", "prompts"))
    file_path = os.path.join(prompts_dir, filename)

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
