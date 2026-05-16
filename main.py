from fastapi import FastAPI
from app.api.routes import router
from loguru import logger

app = FastAPI(
    title="Docvyn",
    description="Intelligent Document Analysis Agent",
    version="2.0.0"
)

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok", "version": "2.0.0"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Iniciando Docvyn API...")
    uvicorn.run(app, host="0.0.0.0", port=8000)