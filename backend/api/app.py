from flask import Flask, request, jsonify
from backend.rag_engine import RAGEngine
from backend.api.logger import get_logger
import uuid
import time
import logging  # ✅ FIX 1: import logging

app = Flask(__name__)

# ----------------------
# Structured logging
# ----------------------
logger = get_logger("rag-api")

# ----------------------
# Load RAG engine ONCE
# ----------------------
engine = RAGEngine(pdf_path="data/raw/sample.pdf")

@app.route("/query", methods=["POST"])
def query_rag():
    request_id = str(uuid.uuid4())
    start_time = time.time()

    data = request.get_json()
    user_query = data.get("query") if data else None

    if not user_query:
        logger.warning(
            f"request_invalid request_id={request_id} reason=empty_query"
        )
        return jsonify({"error": "Query is required"}), 400

    logger.info(f"request_received request_id={request_id}")

    # ---- Run RAG ----
    result = engine.query(user_query)

    latency = round(time.time() - start_time, 3)

    logger.info(
        f"request_completed request_id={request_id} "
        f"latency_seconds={latency} chunks={result['num_chunks']}"
    )

    return jsonify({
        "request_id": request_id,
        "answer": result["answer"],
        "latency_seconds": latency
    })

if __name__ == "__main__":
    app.run(port=8000, debug=False)
