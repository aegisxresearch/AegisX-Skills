# RAG Pipeline Architect

## Overview
Panduan membangun Retrieval-Augmented Generation (RAG) system yang siap diuji di lingkungan staging: dari chunking, embedding, vector DB, sampai retrieval.

---

## ️ RAG Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     USER QUERY                          │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              1. QUERY PROCESSING                        │
│  • Query rewriting                                     │
│  • Intent classification                               │
│  • Query expansion                                     │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              2. RETRIEVAL                               │
│  • Vector search (semantic)                             │
│  • Keyword search (BM25)                                │
│  • Hybrid search (combined)                             │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              3. RERANKING                               │
│  • Cross-encoder reranker                               │
│  • MMR (diversity)                                      │
│  • Score threshold filtering                            │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              4. GENERATION                              │
│  • Context assembly                                     │
│  • LLM inference                                        │
│  • Citation extraction                                  │
└─────────────────────────────────────────────────────────┘
```python

---

## Chunking Strategies

### 1. Fixed-Size Chunking
```python
def fixed_size_chunk(text, chunk_size=512, overlap=50):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks
```python

### 2. Recursive Character Splitting
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""]
)
chunks = splitter.split_documents(documents)
```

### 3. Semantic Chunking (Best Quality)
```python
# Split based on embedding similarity
# When semantic similarity drops, create new chunk
```python

### Chunk Size Guidelines
| Content Type | Recommended Size | Overlap |
|-------------|------------------|---------|
| Technical docs | 512-1024 tokens | 10-20% |
| Code | 256-512 tokens | 50-100 lines |
| FAQ | 200-400 tokens | 0 |
| Legal docs | 1024-2048 tokens | 10% |

---

## Embedding Models

### Model Selection
| Model | Dimensions | Speed | Quality | Cost |
|-------|-----------|-------|---------|------|
| text-embedding-3-small | 1536 | ⚡ Fast | ⭐⭐⭐ | $ |
| text-embedding-3-large | 3072 | ⚡ Fast | ⭐⭐⭐⭐ | $$ |
| bge-large-en-v1.5 | 1024 | 🐢 Slow | ⭐⭐⭐⭐ | Free |
| nomic-embed-text | 768 | ⚡ Fast | ⭐⭐⭐ | Free |

### Embedding Code
```python
from openai import OpenAI
client = OpenAI()

def get_embedding(text, model="text-embedding-3-small"):
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding
```

---

## ️ Vector Database Selection

| DB | Use Case | Hosting |
|----|----------|---------|
| **Pinecone** | Production, managed | Cloud |
| **Qdrant** | Self-hosted, feature-rich | Self/Cloud |
| **Weaviate** | GraphQL API, hybrid search | Self/Cloud |
| **Chroma** | Development, simple | Local |
| **pgvector** | `PostgreSQL` ecosystem | Self/Cloud |

---

## Search Strategies

### Vector Search (Semantic)
```python
results = vector_db.search(
    query_embedding=query_emb,
    top_k=10,
    filter={"category": "technical"}
)
```

### Hybrid Search (Vector + BM25)
```python
# Combine semantic + keyword search
vector_results = vector_db.search(query_emb, top_k=20)
bm25_results = bm25_index.search(query_text, top_k=20)

# Reciprocal Rank Fusion
final_results = rrf_merge(vector_results, bm25_results, k=60)
```

---

## Optimization Tips

### Query Processing
```python
# 1. Query Rewriting
rewritten_query = llm(f"Rewrite this query: {query}")

# 2. Query Expansion (HyDE)
hyde_response = llm(f"Write a hypothetical answer: {query}")
results = search(hyde_response)
```python

### Context Window Management
```python
# Keep context under token limit
MAX_CONTEXT_TOKENS = 4000

def assemble_context(retrieved_chunks, max_tokens):
    context = []
    current_tokens = 0
    for chunk in retrieved_chunks:
        chunk_tokens = count_tokens(chunk)
        if current_tokens + chunk_tokens > max_tokens:
            break
        context.append(chunk)
        current_tokens += chunk_tokens
    return context
```

---

## RAG Pipeline Checklist

- [ ] Chunking strategy chosen (recursive recommended)
- [ ] Chunk size tested (512-1024 tokens)
- [ ] Overlap configured (10-20%)
- [ ] Embedding model selected
- [ ] Vector DB provisioned and indexed
- [ ] Hybrid search implemented
- [ ] Reranker added for quality
- [ ] Metadata filtering supported
- [ ] Query rewriting implemented
- [ ] Citation tracking enabled
- [ ] Evaluation metrics defined (faithfulness, relevance)

---

## Evaluation Metrics

| Metric | What it Measures |
|--------|------------------|
| **Faithfulness** | Is answer grounded in context? |
| **Answer Relevancy** | Does answer address the query? |
| **Context Precision** | Are retrieved chunks relevant? |
| **Context Recall** | Did we retrieve all necessary info? |

---

## References
- https://docs.smith.langchain.com/evaluation
- https://docs.pinecone.io/guides/get-started/quick-tour
- https://python.langchain.com/docs/modules/data_connection/retrievers/

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
