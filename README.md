# semantic-search-offline-minilm-faiss
Offline semantic search using FAISS and Sentence Transformers (all-MiniLM-L6-v2) for accurate, private, and efficient similarity search on small datasets—no external APIs or servers required.

## Required Software

- **Python**: 3.13.3 or higher

### Required Packages

- **sentence-transformers** (>=2.2.2): Hugging Face library for generating high-quality sentence embeddings using pre-trained transformer models. Used to convert text documents into vector representations for semantic similarity search.

- **faiss-cpu** (>=1.7.4): Facebook AI Similarity Search library for efficient similarity search and clustering of dense vectors. Provides fast indexing and retrieval capabilities for large-scale vector databases without requiring GPU acceleration.
