from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.api.auth import verify_password, create_access_token, get_current_user, FAKE_USER
from app.tools.pdf_tool import read_pdf
from app.tools.csv_tool import read_csv
from app.rag.embedder import index_document, query_document
from app.agent.graph import build_graph
from loguru import logger
import shutil
import os

router = APIRouter()

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != FAKE_USER["username"]:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")
    if not verify_password(form_data.password, FAKE_USER["password"]):
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")
    token = create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/upload")
def upload_file(file: UploadFile = File(...), user: str = Depends(get_current_user)):
    logger.info(f"Upload recebido: {file.filename} por {user}")
    file_path = f"temp_{file.filename}"
    
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    if file.filename.endswith(".pdf"):
        content = read_pdf(file_path)
    elif file.filename.endswith(".csv"):
        content = read_csv(file_path)
    else:
        raise HTTPException(status_code=400, detail="Formato não suportado. Use PDF ou CSV.")
    
    index_document(file.filename, content)
    os.remove(file_path)
    
    return {"message": f"Arquivo {file.filename} indexado com sucesso!"}

@router.post("/ask")
def ask_question(question: str, user: str = Depends(get_current_user)):
    logger.info(f"Pergunta recebida de {user}: {question}")
    from langchain_groq import ChatGroq
    from dotenv import load_dotenv
    from langdetect import detect
    import os

    load_dotenv()
    context = query_document(question)

    language = detect(question)
    logger.info(f"Idioma detectado: {language}")

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY")
    )

    response = llm.invoke(
        f"""Responda a pergunta abaixo com base no documento fornecido.
Responda obrigatoriamente no idioma: {language}

Documento:
{context}

Pergunta: {question}"""
    )

    return {"answer": response.content, "language_detected": language}