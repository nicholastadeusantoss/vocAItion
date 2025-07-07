import PyPDF2
from typing import Union
from io import BytesIO

def load_resume_text(file: Union[BytesIO, str]) -> str:
    if isinstance(file, str):
        # Caminho local
        if file.endswith(".txt"):
            with open(file, "r", encoding="utf-8") as f:
                return f.read()
        elif file.endswith(".pdf"):
            with open(file, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                return "".join(page.extract_text() or "" for page in reader.pages).strip()
        else:
            raise ValueError("Formato de arquivo não suportado. Use .txt ou .pdf")

    elif isinstance(file, BytesIO):
        # Arquivo vindo do Streamlit
        reader = PyPDF2.PdfReader(file)
        return "".join(page.extract_text() or "" for page in reader.pages).strip()

    else:
        raise TypeError("Esperado caminho de arquivo ou BytesIO.")
