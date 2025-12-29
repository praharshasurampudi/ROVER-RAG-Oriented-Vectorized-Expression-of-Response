from rank_bm25 import BM25Okapi

def create_bm25_index(chunks):
    """
    Create a BM25 sparse index.
    """
    tokenized_chunks = [chunk.split() for chunk in chunks]
    return BM25Okapi(tokenized_chunks)

"""Keyword matching

Strong for exact terms, names, IDs

Complements embeddings"""