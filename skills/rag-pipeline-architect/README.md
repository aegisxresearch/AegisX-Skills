# RAG Pipeline Architect

> 🎯 **Kategori:** Machine Learning / AI | **Level:** Advanced

## Deskripsi
Panduan membangun Retrieval-Augmented Generation (RAG) system yang production-ready.

## Yang Dipelajari
- RAG architecture overview
- Chunking strategies (fixed-size, recursive, semantic)
- Embedding models comparison
- Vector database selection (Pinecone, Qdrant, Chroma)
- Hybrid search (vector + BM25)
- Reranking & query optimization
- Evaluation metrics (faithfulness, relevance)

## File
📄 [`rag-pipeline-architect.md`](./rag-pipeline-architect.md) — Isi skill lengkap

## Architecture
```
User Query → Query Processing → Vector Search → Reranking → LLM Generation → Response
```

## References
- https://docs.smith.langchain.com/evaluation
- https://docs.pinecone.io/guides/get-started/quick-tour
