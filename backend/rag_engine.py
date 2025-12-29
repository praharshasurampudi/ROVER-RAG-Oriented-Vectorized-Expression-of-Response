from backend.ingestion.pdf_loader import load_pdf
from backend.ingestion.chunker import chunk_text
from backend.indexing.vector_store import create_vector_store
from backend.indexing.bm25_store import create_bm25_index
from backend.retrieval.hybrid_retriever import hybrid_search
from backend.generation.llm import generate_answer


class RAGEngine:
    def __init__(self, pdf_path: str):
        text = load_pdf(pdf_path)
        self.chunks = chunk_text(text)
        self.vectorstore = create_vector_store(self.chunks)
        self.bm25 = create_bm25_index(self.chunks)

    def query(self, user_query: str) -> dict:
        retrieved_chunks = hybrid_search(
            query=user_query,
            vectorstore=self.vectorstore,
            bm25=self.bm25,
            chunks=self.chunks
        )

        context = "\n".join(retrieved_chunks)
        answer = generate_answer(user_query, context)

        return {
            "query": user_query,
            "answer": answer,
            "num_chunks": len(retrieved_chunks)
        }
