import pandas as pd
from loguru import logger

def read_csv(file_path: str) -> str:
    logger.info(f"Lendo CSV: {file_path}")
    try:
        df = pd.read_csv(file_path)
        logger.success(f"CSV carregado com sucesso — {len(df)} linhas, {len(df.columns)} colunas")
        return df.to_string()
    except Exception as e:
        logger.error(f"Erro ao ler CSV: {e}")
        return f"Erro ao ler CSV: {e}"