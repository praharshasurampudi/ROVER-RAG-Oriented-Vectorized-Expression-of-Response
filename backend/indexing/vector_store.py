from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def create_vector_store(chunks):
    """
    Create and persist a Chroma vector store.
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory="data/processed/chroma"
    )

    vectorstore.persist()
    return vectorstore
    

"""Each chunk → embedding vector

Stored locally in ChromaDB

Persistent across runs for efficiency"""