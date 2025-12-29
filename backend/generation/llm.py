from langchain_community.llms import Ollama
from .prompts import SYSTEM_PROMPT

llm = Ollama(model="llama3")

def generate_answer(query, context):
    prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Question:
{query}
"""
    response = llm.invoke(prompt)
    return response


"""Generates answers using Llama3 via Ollama, Local LLM, no API keys, fully offline capability"""