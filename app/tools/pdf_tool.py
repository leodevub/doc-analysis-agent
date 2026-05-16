import fitz
from loguru import logger
import re

def read_pdf(file_path: str, max_chars: int = None) -> str:
    logger.info(f"Lendo PDF: {file_path}")
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text().encode("utf-8", "ignore").decode("utf-8")
        if max_chars:
            text = text[:max_chars]
        logger.success(f"PDF carregado com sucesso — {len(doc)} páginas (truncado em {max_chars} chars)")
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', ' ', text)
        return text
    except Exception as e:
        logger.error(f"Erro ao ler PDF: {e}")
        return f"Erro ao ler PDF: {e}"