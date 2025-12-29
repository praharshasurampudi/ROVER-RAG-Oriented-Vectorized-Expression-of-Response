import json
import time
from backend.rag_engine import RAGEngine

PDF_PATH = "data/raw/sample.pdf"
EVAL_FILE = "evaluation/eval_set.json"


def load_eval_data(path: str):
    with open(path, "r") as f:
        return json.load(f)


def keyword_hit(answer: str, keywords: list[str]) -> bool:
    answer_lower = answer.lower()
    return any(keyword.lower() in answer_lower for keyword in keywords)


def run_evaluation():
    print("Initializing RAG engine...")
    engine = RAGEngine(pdf_path=PDF_PATH)

    eval_data = load_eval_data(EVAL_FILE)

    total = len(eval_data)
    hits = 0
    latencies = []

    print(f"Running evaluation on {total} queries...\n")

    for item in eval_data:
        query_id = item["id"]
        query = item["query"]
        expected_keywords = item["expected_keywords"]

        start = time.time()
        result = engine.query(query)
        latency = round(time.time() - start, 3)

        latencies.append(latency)

        answer = result["answer"]
        success = keyword_hit(answer, expected_keywords)

        if success:
            hits += 1

        print(f"[{query_id}] Query: {query}")
        print(f"Answer: {answer}")
        print(f"Latency: {latency}s")
        print(f"Match: {'PASS' if success else 'FAIL'}")
        print("-" * 60)

    accuracy = hits / total
    avg_latency = sum(latencies) / len(latencies)

    print("\n===== EVALUATION SUMMARY =====")
    print(f"Total Queries: {total}")
    print(f"Correct Answers: {hits}")
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Average Latency: {avg_latency:.2f}s")


if __name__ == "__main__":
    run_evaluation()
