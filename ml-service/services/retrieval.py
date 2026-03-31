def retrieve_docs(vector_store, query, k=3):
    return vector_store.similarity_search(query, k=k)