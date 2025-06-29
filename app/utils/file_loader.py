import os
import PyPDF2

def load_resume_text(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo {file_path} não encontrado.")
    
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    
    elif file_path.endswith(".pdf"):
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text.strip()
    
    else:
        raise ValueError("Formato de arquivo não suportado. Use .txt ou .pdf")
