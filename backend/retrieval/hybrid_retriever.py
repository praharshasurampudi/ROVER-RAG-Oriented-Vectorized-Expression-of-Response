def hybrid_search(query, vectorstore, bm25, chunks, k=5):
    """
    Combine dense (Chroma) and sparse (BM25) retrieval.
    """
    dense_results = vectorstore.similarity_search(query, k=k)
    bm25_scores = bm25.get_scores(query.split())

    combined_scores = {}

    # Add BM25 scores
    for idx, chunk in enumerate(chunks):
        combined_scores[chunk] = bm25_scores[idx]

    # Boost scores for dense matches
    for doc in dense_results:
        combined_scores[doc.page_content] += 1.0

    # Return top-k chunks
    ranked_chunks = sorted(
        combined_scores,
        key=combined_scores.get,
        reverse=True
    )

    return ranked_chunks[:k]
    
"""Combines dense and sparse retrieval for robust results"""