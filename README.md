# Support Agent

An intelligent support agent powered by LangGraph with hybrid retrieval-augmented generation (RAG).

## Overview

This project implements a multi-step support agent that classifies user queries, retrieves relevant documentation using hybrid search, and generates context-aware responses. The agent can handle queries, ask clarifying questions, or escalate to human support via **Zendesk** when needed.

## Architecture

### Graph Structure

The agent is built as a stateful graph with the following workflow:

1. **Intent Classification** - Classifies queries into topics (account, billing, data privacy, api usage, troubleshooting)
2. **Hybrid RAG Subgraph** - Retrieves relevant documents using:
   - Dense search (ChromaDB with vector embeddings)
   - Sparse search (BM25 keyword matching)
   - Reciprocal Rank Fusion (RRF) for result combination
   - Cross-encoder reranking for final selection
3. **Response Generation** - Generates answers based on retrieved context
4. **Routing** - Decides to respond, clarify, or escalate based on answer confidence

### Key Components

- **`src/graph/`** - LangGraph workflow definition
  - `builder.py` - Graph construction and compilation
  - `nodes.py` - Node implementations (classify, search, respond, clarify, escalate)
  - `edges.py` - Conditional routing logic
  - `states.py` - State schemas

- **`src/model/`** - Model configurations
  - `classifier.py` - Intent classification model
  - `reranker.py` - Cross-encoder reranking model
  - `responder.py` - Answer generation model
  - `schemas.py` - Pydantic output schemas

- **`src/index/`** - Search indexes
  - `dense/` - ChromaDB vector index
  - `sparse/` - BM25 tokenized corpus

- **`src/ingestion/`** - Data ingestion pipeline for building indexes

## Setup

### Prerequisites

- Python 3.11+
- UV package manager (recommended)

### Installation

```bash
# Install dependencies
uv sync

# Or with pip
pip install -e .
```

### Environment Variables

Create a `.env` file with:

```
OPENAI_API_KEY=your_api_key
```

## Usage

### Running the Agent

```python
from src.graph.builder import graph

result = graph.invoke({"messages": [{"role": "user", "content": "How do I reset my password?"}]})
print(result)
```

### Ingesting New Data

```bash
python -m src.ingestion.ingest
```

Place your knowledge base documents in `src/data/` with the format:

```json
[
  {
    "id": "unique-id",
    "text": "Document content...",
    "metadata": {"source": "faq", "category": "account"}
  }
]
```

## Features

- **Hybrid Search** - Combines semantic (dense) and keyword (sparse) retrieval
- **Reciprocal Rank Fusion** - Merges search results from multiple indices
- **Cross-Encoder Reranking** - Improves retrieval relevance
- **Intent Classification** - Routes queries to appropriate handlers
- **Graceful Escalation** - Falls back to human support when needed
- **Stateful Conversations** - Maintains context across interactions (via checkpointer)

## Tech Stack

- **LangGraph** - Workflow orchestration
- **LangChain** - LLM abstraction
- **ChromaDB** - Vector database
- **Rank BM25** - Sparse retrieval
- **Sentence Transformers** - Embeddings
- **OpenAI** - Language models

## Project Structure

```
support-agent/
├── src/
│   ├── graph/          # LangGraph workflow
│   ├── model/          # Model configurations
│   ├── prompts/        # Prompt templates
│   ├── index/          # Search indexes
│   ├── ingestion/      # Data pipeline
│   ├── integrations/   # External services (Zendesk)
│   └── data/           # Knowledge base
├── main.py             # Entry point
└── pyproject.toml      # Project config
```
