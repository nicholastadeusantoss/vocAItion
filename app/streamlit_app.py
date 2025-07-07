import streamlit as st
import os
from app.utils.file_loader import load_resume_text
from app.sections.experience import (
    extract_experiences_with_ai,
    generate_experience_questions,
    improve_experience_with_answers,
    parse_numbered_questions
)

st.set_page_config(page_title="vocAItion - Resume AI", layout="wide")

st.markdown(
    """
    <style>
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #f9fafb;
            color: #000;
        }
    </style>
    """,
    unsafe_allow_html=True
)

if "step" not in st.session_state:
    st.session_state.step = "upload"
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "experiences" not in st.session_state:
    st.session_state.experiences = []
if "selected_experience" not in st.session_state:
    st.session_state.selected_experience = ""

st.title("📄 vocAItion — Resume Enhancement Assistant")

st.markdown("""
    <style>
        .centered {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            min-height: 0vh;
            padding-top: 50px;
            text-align: center;
        }
        [data-testid="stFileUploader"] > div:first-child {
            border: 2px dashed #ccc;
            border-radius: 10px;
            padding: 40px;
            background-color: #fff;
            max-width: 600px;
            margin: 30px auto;
            text-align: center;
        }
        .upload-box:hover {
            border-color: #999;
        }
        .upload-button button {
            background-color: #e0e0e0;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 600;
            margin-top: 10px;
        }
        .stException {
            max-height: 400px;
            overflow-y: auto;
        }
        button[kind="secondary"] {
            background-color: #f1f1f1 !important;
            color: #000000 !important;
            border: 1px solid #ccc !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease-in-out;
        }
        button[kind="secondary"]:hover {
            background-color: #e0e0e0 !important;
            color: #000000 !important;
            border-color: #888 !important;
        }
        label[for^="q_"] {
            font-weight: 600;
            font-size: 1rem;
            color: #111827;
            margin-bottom: 0.5rem;
            display: block;
        }
        textarea {
            background-color: #ffffff !important;
            color: #000 !important;
            border: 1px solid #ccc !important;
            border-radius: 8px !important;
            padding: 12px !important;
            font-size: 1rem !important;
            width: 100% !important;
            max-width: 800px;
            min-height: 100px;
            resize: vertical;
            margin-bottom: 20px;
        }
        footer {
            font-size: 0.8rem;
            margin-top: 40px;
            color: gray;
        }
        
    </style>
""", unsafe_allow_html=True)

# === Etapa 1: Upload ===
if st.session_state.step == "upload":
    st.markdown('<div class="centered">', unsafe_allow_html=True)
    st.image("https://img.icons8.com/ios-filled/50/resume.png", width=50)
    st.markdown("## Upload Your Resume")
    st.markdown("Please upload your resume in PDF format. Our system will analyze your resume and provide personalized feedback to help you improve it.")

    with st.container():
        st.markdown("#### Drag and drop your PDF here", unsafe_allow_html=True)

        st.markdown('<div style="width:100%; max-width:500px;">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            label=" ", 
            type=["pdf"], 
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)   

        st.markdown('</div>', unsafe_allow_html=True)


        st.markdown("""<footer> By uploading your resume, you agree to our <a href="#">terms of service</a> and <a href="#">privacy policy</a>.
            </footer>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Processa o arquivo ao subir
        if uploaded_file:
            with st.spinner("Reading resume and extracting experiences..."):
                resume_text = load_resume_text(uploaded_file)
                experiences = extract_experiences_with_ai(resume_text)

                st.session_state.resume_text = resume_text
                st.session_state.experiences = experiences
                st.session_state.step = "select_experience"
                st.rerun()

# === Etapa 2: Selecionar experiência ===
elif st.session_state.step == "select_experience":
    st.header("2. Select an Experience to Improve")

    if not st.session_state.experiences:
        st.warning("No experiences found. Please upload a valid resume.")
        st.session_state.step = "upload"
        st.rerun()

    for i, exp in enumerate(st.session_state.experiences):
        st.markdown(f"**{exp}**")
        if st.button(f"✏️ Edit Experience {i+1}", key=f"edit_{i}"):
            st.session_state.selected_experience = exp
            st.session_state.questions = []  # limpa perguntas antigas
            st.session_state.step = "interview"
            st.rerun()

# === Etapa 3: Entrevista (perguntas sobre a experiência) ===
elif st.session_state.step == "interview":
    st.header("3. Help Us Improve This Experience")

    if "questions" not in st.session_state or not st.session_state.questions:
        with st.spinner("Generating questions..."):
            raw_output = generate_experience_questions(
                st.session_state.selected_experience
            )
            questions = parse_numbered_questions(raw_output)

            if not questions:
                st.error("❌ Failed to generate questions. Please try a different experience.")
                st.stop()

            st.session_state.questions = questions

    with st.form("experience_questions_form"):
        responses = []
        for i, q in enumerate(st.session_state.questions):
            st.markdown(f"""
                <div style="margin-top:20px; margin-bottom:5px; font-weight:bold;">
                    {i+1}. {q}
                </div>
            """, unsafe_allow_html=True)
            response = st.text_area(label="", key=f"q{i}", height=100)
            responses.append(response)

        submitted = st.form_submit_button("Generate Improved Experience")
    if submitted:
        st.session_state.responses = responses
        try:
            with st.spinner("Improving your experience text..."):
                answers_text = "\n\n".join(responses)
                improved = improve_experience_with_answers(
                    st.session_state.selected_experience, answers_text
                )
                st.session_state.improved_experience = improved
                st.session_state.step = "preview"
                st.rerun()
        except Exception as e:
            st.error(f"❌ Erro ao melhorar a experiência: {str(e)}")

# === Etapa 4: Prévia e confirmação ===
elif st.session_state.step == "preview":
    st.header("4. Preview the Improved Experience")

    st.markdown("### ✨ Improved Experience:")
    st.markdown(f"""<div style="border:1px solid #ccc; padding:15px; border-radius:8px; background:#fff;">
    {st.session_state.improved_experience}
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("✅ Accept and Continue"):
            # Aqui você pode salvar em algum storage, banco ou apenas manter na session
            st.success("Experience saved successfully!")
            st.session_state.step = "select_experience"
            st.rerun()
    with col2:
        if st.button("🔁 Refine Again"):
            st.session_state.step = "interview"
            st.rerun()

