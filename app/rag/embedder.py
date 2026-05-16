import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger

client = chromadb.PersistentClient(path="./chroma_db")
embedding_fn = embedding_functions.DefaultEmbeddingFunction()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", " "]
)

def index_document(doc_id: str, text: str):
    logger.info(f"Indexando documento: {doc_id}")
    collection = client.get_or_create_collection(
        name="documents",
        embedding_function=embedding_fn
    )

    chunks = splitter.split_text(text)
    ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]

    collection.add(documents=chunks, ids=ids)
    logger.success(f"{len(chunks)} chunks indexados")

def query_document(question: str, n_results: int = 3) -> str:
    logger.info(f"Buscando chunks relevantes para: {question}")
    collection = client.get_or_create_collection(
        name="documents",
        embedding_function=embedding_fn
    )

    results = collection.query(query_texts=[question], n_results=n_results)
    chunks = results["documents"][0]
    logger.debug(f"Chunks encontrados: {chunks}")
    return "\n\n".join(chunks)