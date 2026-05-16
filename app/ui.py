import streamlit as st
import requests

API_URL = "http://api:8000"

st.set_page_config(page_title="Docvyn", page_icon="📄", layout="centered")
st.title("📄 Docvyn")
st.caption("Intelligent Document Analysis Agent")

# Login
if "token" not in st.session_state:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        response = requests.post(f"{API_URL}/token", data={
            "username": username,
            "password": password
        })
        if response.status_code == 200:
            st.session_state.token = response.json()["access_token"]
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")
else:
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    st.subheader("Upload do documento")
    file = st.file_uploader("Escolha um CSV ou PDF", type=["csv", "pdf"])
    
    if file:
        response = requests.post(
            f"{API_URL}/upload",
            files={"file": (file.name, file, file.type)},
            headers=headers
        )
        if response.status_code == 200:
            st.success(f"✅ {file.name} indexado com sucesso!")
        else:
            st.warning(f"⚠️ Arquivo enviado mas pode já estar indexado.")

    st.subheader("Faça sua pergunta")
    question = st.text_input("Digite sua pergunta em qualquer idioma")
    
    if st.button("Perguntar"):
        if question:
            with st.spinner("Analisando documento..."):
                response = requests.post(
                    f"{API_URL}/ask",
                    params={"question": question},
                    headers=headers
                )
            if response.status_code == 200:
                data = response.json()
                st.markdown("### Resposta")
                st.markdown(data["answer"])
                st.caption(f"Idioma detectado: {data['language_detected']}")
            else:
                st.error("Erro ao processar pergunta")
    
    if st.button("Logout"):
        del st.session_state.token
        st.rerun()