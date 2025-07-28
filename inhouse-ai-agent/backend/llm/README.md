### `/backend/llm`

LLM operations and RAG pipeline.

* `model.py`: Load TinyLlama locally
* `embeddings.py`: Embed text for vector DB
* `retriever.py`: Search vector DB (Chroma)
* `rag_pipeline.py`: Combine retriever + model for QA
