from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

from services.embedding import get_embedding_model
from services.retrieval import retrieve_docs
from services.rag_pipeline import generate_answer
from services.ingestion import load_and_chunk_pdf
from vector_store.faiss_store import create_vector_store, load_vector_store, save_vector_store

app = FastAPI()

embedding_model = get_embedding_model()

VECTOR_PATH = "vector_store/index"

# Try loading existing store
try:
    vector_store = load_vector_store(VECTOR_PATH, embedding_model)
except:
    vector_store = None


class QueryRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "RAG API is running"}

@app.post("/query")
def query(req: QueryRequest):
    global vector_store

    if vector_store is None:
        return {"answer": "No documents uploaded yet."}

    docs = retrieve_docs(vector_store, req.question)
    answer = generate_answer(req.question, docs)

    return {
        "answer": answer,
        "sources": [doc.page_content[:200] for doc in docs]
    }


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    global vector_store

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    docs = load_and_chunk_pdf(file_path)

    vector_store = create_vector_store(docs, embedding_model)
    save_vector_store(vector_store, VECTOR_PATH)

    os.remove(file_path)

    return {"message": "Document processed successfully"}