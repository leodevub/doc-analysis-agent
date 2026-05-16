# Docvyn — Intelligent Document Analysis Agent

AI-powered agent that analyzes CSV and PDF files and answers questions in any language.

## Features

- Upload CSV or PDF files via UI or API
- Ask questions in any language — responds in the same language
- RAG (Retrieval-Augmented Generation) for accurate PDF analysis
- JWT authentication
- Clean and modern Streamlit interface
- Fully containerized with Docker

## Tech Stack

| Layer | Technology |
|---|---|
| Agent | LangGraph + LangChain |
| LLM | Groq (llama-3.1-8b-instant) |
| Vector DB | ChromaDB |
| API | FastAPI |
| Auth | JWT (python-jose) |
| UI | Streamlit |
| PDF Reader | PyMuPDF |
| Logging | Loguru |
| Tests | Pytest |
| Container | Docker + Docker Compose |

## How to Run

### Requirements
- Docker
- Groq API Key (free at https://console.groq.com)

### Setup

1. Clone the repository
\```bash
git clone https://github.com/leodevub/doc-analysis-agent.git
cd doc-analysis-agent
\```

2. Create the `.env` file
\```bash
GROQ_API_KEY=your_key_here
\```

3. Run with Docker
\```bash
docker compose up --build
\```

4. Access
- **UI:** http://localhost:8501
- **API Docs:** http://localhost:8000/docs

### Default credentials
- Username: `admin`
- Password: `admin123`

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | /token | ❌ | Get JWT token |
| POST | /upload | ✅ | Upload CSV or PDF |
| POST | /ask | ✅ | Ask a question |
| GET | /health | ❌ | Health check |

## Running Tests

\```bash
python -m pytest tests/ -v
\```

## Architecture

\```
User → Streamlit UI → FastAPI → LangGraph Agent
                                      ↓
                              detect file type
                                      ↓
                    CSV → pandas    PDF → PyMuPDF → ChromaDB (RAG)
                                      ↓
                                  Groq LLM
                                      ↓
                               Response in user's language
\```