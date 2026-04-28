from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os

# ✅ Updated imports
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

vector_db = None

# 🔹 Upload PDF
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    global vector_db

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    docs = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vector_db = FAISS.from_documents(docs, embeddings)

    return {"message": "PDF processed successfully!"}


# 🔹 Ask question (NEW WAY — no RetrievalQA)
@app.post("/ask")
async def ask(data: dict):
    global vector_db

    if vector_db is None:
        return {"error": "Upload PDF first"}

    question = data.get("question")

    if not question:
        return {"error": "No question provided"}

    # Get relevant docs
    docs = vector_db.similarity_search(question, k=3)

    context = "\n".join([doc.page_content for doc in docs])

    # LLM
    llm = Ollama(model="llama3")

    prompt = f"""
    Answer the question based on the context below:

    Context:
    {context}

    Question:
    {question}
    """

    answer = llm.invoke(prompt)

    return {"answer": answer}


@app.get("/")
def home():
    return {"message": "RAG Chatbot running!"}