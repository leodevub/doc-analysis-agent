import fitz
from loguru import logger

def read_pdf(file_path: str, max_chars: int = 3000) -> str:
    logger.info(f"Lendo PDF: {file_path}")
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        text = text[:max_chars]
        logger.success(f"PDF carregado com sucesso — {len(doc)} páginas (truncado em {max_chars} chars)")
        return text
    except Exception as e:
        logger.error(f"Erro ao ler PDF: {e}")
        return f"Erro ao ler PDF: {e}"