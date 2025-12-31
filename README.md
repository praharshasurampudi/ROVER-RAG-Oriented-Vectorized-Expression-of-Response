#ROVER
##RAG-Oriented-Vectorized-Expression-of-Response

A **production-grade Retrieval-Augmented Generation (RAG) backend** that ingests documents, performs **hybrid dense + BM25 retrieval**, and serves grounded answers via a **Flask API** with **structured logging** and **offline evaluation**.

---

## 🔹 Key Features

* 📄 **Document Ingestion** (PDF → text → chunks)
* 🔍 **Hybrid Retrieval**

  * Dense semantic search (ChromaDB + embeddings)
  * Sparse keyword search (BM25)
* 🤖 **Local LLM Inference**

  * Llama 3 via Ollama (no cloud dependency)
* 🌐 **Flask API**

  * Stateless `/query` endpoint
  * Request IDs & latency tracking
* 📊 **Structured JSON Logging**
* 🧪 **Offline Evaluation**

  * Fixed query set
  * Accuracy & latency metrics

---

## 🧠 System Architecture

```
                ┌──────────────┐
                │   PDF Files  │
                └──────┬───────┘
                       │
                ┌──────▼───────┐
                │ Ingestion    │
                │ (PDF Loader) │
                └──────┬───────┘
                       │
                ┌──────▼───────┐
                │ Chunking     │
                │ (Overlap)    │
                └──────┬───────┘
                       │
        ┌──────────────┴──────────────┐
        │                               │
┌───────▼────────┐          ┌──────────▼─────────┐
│ Dense Retrieval │          │ Sparse Retrieval   │
│ (ChromaDB +     │          │ (BM25)             │
│ Embeddings)     │          │                    │
└───────┬────────┘          └──────────┬─────────┘
        │                               │
        └──────────────┬──────────────┘
                       │
                ┌──────▼───────┐
                │ Hybrid        │
                │ Retriever     │
                └──────┬───────┘
                       │
                ┌──────▼───────┐
                │ Prompt +      │
                │ Context       │
                └──────┬───────┘
                       │
                ┌──────▼───────┐
                │ Llama 3       │
                │ (Ollama)      │
                └──────────────┘
```

---

## 📁 Project Structure

```
RAG/
│
├── backend/
│   ├── rag_engine.py          # Core RAG pipeline
│   │
│   ├── api/
│   │   ├── app.py             # Flask API
│   │   └── logger.py          # Structured JSON logging
│   │
│   ├── ingestion/             # PDF loading & chunking
│   ├── indexing/              # ChromaDB + BM25
│   ├── retrieval/             # Hybrid retriever
│   └── generation/            # Prompting + LLM
│
├── data/
│   ├── raw/                   # Input documents (PDFs)
│   └── processed/             # Vector store persistence
│
├── evaluation/
│   ├── eval_set.json          # Offline evaluation queries
│   └── evaluate.py            # Evaluation runner
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/praharshasurampudi/production-rag-text-knowledge-agent
cd RAG
```

---

## 🐍 Python Environment Setup

### macOS / Linux

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### Windows (PowerShell)

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
```

> ⚠️ If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---

### Install Dependencies (All OS)

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🤖 Ollama Setup (Local LLM)

### macOS

```bash
brew install ollama
```

### Windows

1. Download installer from:
   👉 [https://ollama.com/download](https://ollama.com/download)
2. Install and restart terminal

---

### Start Ollama Server

```bash
ollama serve
```

In a **new terminal**, pull the model:

```bash
ollama pull llama3
```

---

## 📄 Add Documents

Place PDFs inside:

```
data/raw/
```

Example:

```
data/raw/sample.pdf
```

---

## 🚀 Running the API

From the project root:

```bash
python -m backend.api.app
```

API runs at:

```
http://127.0.0.1:8000
```

---

### 🔗 Query Endpoint

**POST** `/query`

#### Example request

```bash
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is this document about?"}'
```

#### Example response

```json
{
  "request_id": "0935766c-f08b-480e-a756-9c2d8dbf1222",
  "answer": "This document is a resume for an AI Engineer...",
  "latency_seconds": 24.34
}
```

---

## 📊 Logging & Observability

* Logs are **JSON-formatted**
* Each request includes:

  * Request ID
  * Latency
  * Retrieval metadata
* Logs are emitted to **stdout** (Docker-friendly)

Example log:

```json
{
  "timestamp": "2025-12-29T08:41:22Z",
  "level": "INFO",
  "message": "request_completed request_id=0935766c latency_seconds=24.34 chunks=5",
  "logger": "rag-api"
}
```

---

## 🧪 Offline Evaluation

Run evaluation as a module:

```bash
python -m evaluation.evaluate
```

### Metrics Produced

* Accuracy (keyword-based grounding)
* Average latency
* Per-query diagnostics

Example output:

```
Accuracy: 1.00
Average Latency: 16.47s
```

This enables **regression testing** and retrieval quality monitoring over time.

---

## 🛠️ Design Decisions

* **Hybrid retrieval** improves grounding vs dense retrieval alone
* **Strict prompt grounding** minimizes hallucinations
* **Local LLM (Ollama)** ensures privacy and offline execution
* **Offline evaluation** avoids subjective LLM-as-judge scoring

---

## 📝 License © [Praharsha Surampudi](https://www.linkedin.com/in/praharsha-surampudi/)

---
