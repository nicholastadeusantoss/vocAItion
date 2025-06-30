import streamlit as st
import os
from app.utils.file_loader import load_resume_text
from app.sections.experience import (
    extract_experiences_with_ai,
    generate_experience_questions,
    improve_experience_with_answers
)

st.set_page_config(page_title="vocAItion - Resume AI", layout="wide")

if "step" not in st.session_state:
    st.session_state.step = "upload"
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "experiences" not in st.session_state:
    st.session_state.experiences = []
if "selected_experience" not in st.session_state:
    st.session_state.selected_experience = ""

st.title("📄 vocAItion — Resume Enhancement Assistant")

# Step 1: Upload
if st.session_state.step == "upload":
    st.header("1. Upload your resume")
    uploaded_file = st.file_uploader("Choose a .txt or .pdf file", type=["pdf", "txt"])

    if uploaded_file:
        file_path = os.path.join("data", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("File uploaded successfully!")

        resume_text = load_resume_text(file_path)
        st.session_state.resume_text = resume_text
        st.session_state.step = "select"

        st.rerun()

# Step 2: Select experience
elif st.session_state.step == "select":
    st.header("2. Select experience to improve")

    if not st.session_state.experiences:
        with st.spinner("Extracting experiences from resume..."):
            experiences = extract_experiences_with_ai(st.session_state.resume_text)
            st.session_state.experiences = experiences

    if not st.session_state.experiences:
        st.error("No experiences found.")
        st.stop()

    selected = st.radio("Choose one experience to improve:", st.session_state.experiences)

    if st.button("Continue"):
        st.session_state.selected_experience = selected
        st.session_state.step = "qa"
        st.rerun()

# Step 3: QA + Improvement
elif st.session_state.step == "qa":
    st.header("3. Answer questions to improve your experience")

    st.subheader("Selected experience")
    st.code(st.session_state.selected_experience)

    with st.spinner("Generating questions..."):
        questions = generate_experience_questions(st.session_state.selected_experience)

    st.write("Please answer the questions below:")
    st.text_area("Questions", questions, height=150, disabled=True)

    answers = st.text_area("Your answers")

    if st.button("Generate improved description"):
        with st.spinner("Improving experience..."):
            improved = improve_experience_with_answers(st.session_state.selected_experience, answers)
        st.subheader("✅ Improved experience")
        st.success(improved)

        if st.button("🔁 Start over"):
            for key in ["step", "resume_text", "experiences", "selected_experience"]:
                st.session_state.pop(key, None)
            st.rerun()
