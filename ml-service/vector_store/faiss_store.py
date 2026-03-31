from langchain_community.vectorstores import FAISS

def create_vector_store(docs, embedding_model):
    return FAISS.from_documents(docs, embedding_model)

def load_vector_store(path, embedding_model):
    return FAISS.load_local(path, embedding_model, allow_dangerous_deserialization=True)

def save_vector_store(store, path):
    store.save_local(path)