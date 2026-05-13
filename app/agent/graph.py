from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from loguru import logger
from typing import TypedDict
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

class AgentState(TypedDict):
    question: str
    file_path: str
    file_type: str
    answer: str

def detect_file_type(state: AgentState) -> AgentState:
    path = state["file_path"].strip().lower()
    logger.debug(f"Caminho recebido: '{path}'")
    if path.endswith(".csv"):
        state["file_type"] = "csv"
        logger.info("Arquivo detectado: CSV")
    elif path.endswith(".pdf"):
        state["file_type"] = "pdf"
        logger.info("Arquivo detectado: PDF")
    else:
        state["file_type"] = "unknown"
        logger.warning("Tipo de arquivo desconhecido")
    return state

def process_document(state: AgentState) -> AgentState:
    from app.tools.csv_tool import read_csv
    from app.tools.pdf_tool import read_pdf

    if state["file_type"] == "csv":
        content = read_csv(state["file_path"])
    elif state["file_type"] == "pdf":
        content = read_pdf(state["file_path"])
    else:
        state["answer"] = "Formato de arquivo não suportado."
        return state

    logger.info("Enviando documento para o LLM...")
    response = llm.invoke(
        f"Com base no documento abaixo, responda: {state['question']}\n\n{content}"
    )
    state["answer"] = response.content
    return state

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("detect", detect_file_type)
    graph.add_node("process", process_document)
    graph.set_entry_point("detect")
    graph.add_edge("detect", "process")
    graph.add_edge("process", END)
    return graph.compile()