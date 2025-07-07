# app/chat_resume.py
import streamlit as st
from app.utils import file_loader, openai_client, prompts

def main():
    st.title("💬 Conversa com seu Currículo")

    resume_path = st.session_state.get("resume_path")
    if not resume_path:
        st.warning("Por favor, envie um currículo primeiro na aba de upload.")
        return

    st.markdown(f"📄 **Currículo carregado:** `{resume_path}`")

    # 1. Extrai conteúdo do currículo
    content = file_loader.load_file(resume_path)

    # 2. Extrai experiência com prompt
    extract_prompt = prompts.load_prompt("experience_extract_prompt.txt")
    extracted_exp = openai_client.ask_llm(extract_prompt.format(content=content))

    st.markdown("📌 **Experiência detectada:**")
    st.markdown(extracted_exp)

    # 3. Perguntas personalizadas
    question_prompt = prompts.load_prompt("experience_questions_prompt.txt")
    questions = openai_client.ask_llm(question_prompt.format(content=extracted_exp))
    st.markdown("❓ **Por favor, responda às perguntas abaixo para melhorar sua descrição:**")
    st.text_area("Digite suas respostas (em texto corrido):", key="user_answers")

    if st.button("Gerar versão otimizada"):
        improve_prompt = prompts.load_prompt("experience_improve_prompt.txt")
        improved = openai_client.ask_llm(improve_prompt.format(content=extracted_exp, answers=st.session_state["user_answers"]))
        st.success("✅ **Descrição otimizada:**")
        st.markdown(improved)

if __name__ == "__main__":
    main()
