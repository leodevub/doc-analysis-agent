from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", " "]
)

# Armazena chunks em memória
document_store = []

def index_document(doc_id: str, text: str):
    global document_store
    logger.info(f"Indexando documento: {doc_id}")
    chunks = splitter.split_text(text)
    document_store = [{"id": f"{doc_id}_chunk_{i}", "text": chunk} for i, chunk in enumerate(chunks)]
    logger.success(f"{len(chunks)} chunks indexados")

def query_document(question: str, n_results: int = 5) -> str:
    logger.info(f"Buscando chunks relevantes para: {question}")
    keywords = question.lower().split()
    
    scored = []
    for chunk in document_store:
        score = sum(chunk["text"].lower().count(kw) for kw in keywords)
        scored.append((score, chunk["text"]))
    
    scored.sort(reverse=True)
    top_chunks = [text for _, text in scored[:n_results] if _ > 0]
    
    if not top_chunks:
        top_chunks = [chunk["text"] for chunk in document_store[:n_results]]
    
    logger.debug(f"{len(top_chunks)} chunks encontrados")
    return "\n\n".join(top_chunks)