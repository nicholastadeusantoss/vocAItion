from io import BytesIO
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.questions import generate_experience_questions
from app.services.improver import improve_experience_with_answers
from app.services.extractor import extract_experiences_with_ai
from app.utils.text import parse_numbered_questions
from app.utils.file_loader import load_resume_text


app = FastAPI(title="vocAItion API", version="1.0")


# CORS para permitir acesso do frontend local
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["http://localhost:5173"],  # porta padrão do Vite
    allow_methods=["*"],
    allow_headers=["*"],
)

class ExperienceInput(BaseModel):
    text: str

class ImproveInput(BaseModel):
    original: str
    answers: list[str]


@app.post("/questions")
def get_questions(data: ExperienceInput):
    try:
        raw_output = generate_experience_questions(data.text)
        questions = parse_numbered_questions(raw_output)
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/improve")
def improve_experience(data: ImproveInput):
    try:
        joined_answers = "\n".join(data.answers)
        improved = improve_experience_with_answers(data.original, joined_answers)
        return {"improved": improved}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = load_resume_text(BytesIO(content))

        # Aqui você pode salvar em cache, banco ou apenas retornar direto:
        return {"message": "Currículo processado com sucesso.", "text": text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract-experiences")
def extract_experiences(data: ExperienceInput):
    try:
        experiences = extract_experiences_with_ai(data.text)
        return {"experiences": experiences}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
