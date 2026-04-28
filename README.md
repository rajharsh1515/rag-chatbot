# AI PDF Chatbot (RAG-based)

## Tech Stack
- FastAPI
- LangChain
- FAISS
- Ollama (Local LLM)

## Features
- Upload PDF
- Ask questions
- Context-aware answers

## How to Run
1. Install dependencies
2. Run:
   python -m uvicorn main:app --reload
3. Start Ollama:
   ollama run llama3
4. Open frontend

## Note
This project uses Ollama (local LLM), so it runs locally.
