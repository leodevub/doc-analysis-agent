import streamlit as st
import requests

API_URL = "https://docvyn-api2.onrender.com"

st.set_page_config(
    page_title="Docvyn",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #141414;
    }

    section[data-testid="stSidebar"] { display: none; }
    [data-testid="collapsedControl"] { display: none; }

    .login-container {
        max-width: 400px;
        margin: 4rem auto;
        padding: 2.5rem;
        background: #1c1c1c;
        border: 1px solid #2a2a2a;
        border-radius: 16px;
    }

    .brand {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -1px;
        text-align: center;
        margin-bottom: 0.25rem;
    }

    .brand span { color: #ef4444; }

    .tagline {
        font-size: 0.8rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 2rem;
    }

    .answer-box {
        background: #1c1c1c;
        border: 1px solid #2a2a2a;
        border-left: 3px solid #ef4444;
        border-radius: 0 12px 12px 0;
        padding: 1.5rem 2rem;
        margin-top: 1.5rem;
        line-height: 1.9;
        color: #d1d5db;
        font-size: 0.95rem;
    }

    .stTextInput>div>div>input {
        background: #222222 !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 8px !important;
        color: #f9fafb !important;
        padding: 0.75rem 1rem !important;
    }

    .stButton>button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        border: none !important;
        width: 100%;
    }

    label, p, .stMarkdown { color: #9ca3af !important; }
    h1, h2, h3 { color: #f9fafb !important; }

    .pill {
        display: inline-block;
        background: #1e1e1e;
        color: #ef4444;
        padding: 3px 12px;
        border-radius: 999px;
        font-size: 0.75rem;
    }

    .divider {
        border: none;
        border-top: 1px solid #2a2a2a;
        margin: 1.5rem 0;
    }

    footer { display: none; }
    </style>
""", unsafe_allow_html=True)

# LOGIN
if "token" not in st.session_state:
    st.markdown("""
        <div class='login-container'>
            <div class='brand'>Doc<span>vyn</span></div>
            <div class='tagline'>Intelligent Document Analysis Agent</div>
        </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="admin")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        submit = st.form_submit_button("Sign in →", type="primary", use_container_width=True)

        if submit:
            response = requests.post(f"{API_URL}/token", data={
                "username": username,
                "password": password
            })
            if response.status_code == 200:
                st.session_state.token = response.json()["access_token"]
                st.rerun()
            else:
                st.error("Invalid username or password")

# DASHBOARD
else:
    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("## Doc<span style='color:#ef4444'>vyn</span>", unsafe_allow_html=True)
    with col2:
        if st.button("Logout", use_container_width=True):
            del st.session_state.token
            st.rerun()

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    st.markdown("#### 📂 Document")
    file = st.file_uploader("Upload a CSV or PDF", type=["csv", "pdf"], label_visibility="collapsed")

    if file:
        with st.spinner("Indexing document..."):
            response = requests.post(
                f"{API_URL}/upload",
                files={"file": (file.name, file, file.type)},
                headers=headers
            )
        if response.status_code == 200:
            st.session_state.file_loaded = file.name
            st.success(f"✅ {file.name} indexed successfully!")
        else:
            st.warning("⚠️ File may already be indexed")

    if "file_loaded" in st.session_state:
        st.markdown(f'<span class="pill">📄 {st.session_state.file_loaded}</span>', unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    st.markdown("#### 💬 Your question")
    question = st.text_input("Question", placeholder="Ask in any language...", label_visibility="collapsed")

    if st.button("Analyze →", type="primary"):
        if question:
            with st.spinner("Analyzing document..."):
                response = requests.post(
                    f"{API_URL}/ask",
                    params={"question": question},
                    headers=headers
                )
            if response.status_code == 200:
                data = response.json()
                st.markdown(f"<div class='answer-box'>{data['answer']}</div>", unsafe_allow_html=True)
                st.caption(f"🌐 Language detected: `{data['language_detected']}`")
            else:
                st.error("Error processing question")
        else:
            st.warning("Please enter a question first")