# app/upload_resume.py
import streamlit as st
import os
from pathlib import Path

def save_file(uploaded_file):
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    file_path = data_dir / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def main():
    st.title("Upload Your Resume")
    st.write("Please upload your resume in PDF or DOCX format to get started.")

    uploaded_file = st.file_uploader("Drag and drop your PDF or DOCX here", type=["pdf", "docx"])

    if uploaded_file:
        saved_path = save_file(uploaded_file)
        st.success(f"📄 Currículo carregado: {saved_path}")
        st.session_state["resume_path"] = str(saved_path)  # salva caminho para tela seguinte

if __name__ == "__main__":
    main()
