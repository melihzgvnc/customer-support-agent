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

- Docker & Docker Compose
- Environment variables configured in `.env`

### Quick Start

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f api

# Stop services
docker compose down
```

The API will be available at `http://localhost:9000`.

### Services

The application runs as a multi-container system:

- **API** (`api`) - FastAPI application on port 9000
- **ChromaDB** (`chromadb`) - Vector database on port 8000
- **Garage** (`garage`) - S3-compatible object storage on port 3900
- **PostgreSQL** (`db`) - Relational database for LangGraph checkpointing
- **Ingestion** (`ingest`) - One-off data ingestion job (profile: `ingest`)

### Configuration

Create a `.env` file and `secrets/` directory with required credentials:

```env
OPENAI_API_KEY=your_key
DB__POSTGRES_USER=postgres
DB__POSTGRES_DB=support_agent
# See compose.yaml for additional environment variables
```

Required secrets in `secrets/`:
- `llm__openai_api_key`
- `db__postgres_password`
- `db__s3_access_key_id`
- `db__s3_secret_access_key`
- Additional secrets listed in `compose.secrets.yaml`

## Usage

### API Endpoints

```bash
# Health check
curl http://localhost:9000/health

# Chat endpoint
curl -X POST http://localhost:9000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "How do I reset my password?"}]}'
```

### Ingesting New Data

```bash
# Run ingestion job
docker compose --profile ingest up ingest

# Or rebuild and run
docker compose build ingest
docker compose --profile ingest up ingest
```

Place knowledge base documents in `data/raw_data/` following the expected JSON schema.

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
- **FastAPI** - API framework
- **Docker Compose** - Container orchestration
- **ChromaDB** - Vector database
- **PostgreSQL** - Checkpointing & persistence
- **Garage** - S3-compatible object storage
- **Rank BM25** - Sparse retrieval
- **Sentence Transformers** - Embeddings
- **OpenAI** - Language models

## Project Structure

```
support-agent/
├── src/support_agent/
│   ├── api/            # FastAPI application
│   ├── graph/          # LangGraph workflow
│   ├── model/          # Model configurations
│   ├── prompts/        # Prompt templates
│   ├── services/       # Business logic
│   └── integrations/   # External services (Zendesk)
├── data/
│   ├── ingestion/      # Data pipeline scripts
│   ├── raw_data/       # Source documents
│   └── index/          # Search indexes (volumes)
├── secrets/            # Docker secrets
├── Dockerfile          # Multi-stage container build
├── compose.yaml        # Service orchestration
└── pyproject.toml      # Project config
```

## Development

### Local Development with Hot Reload

```bash
# Start services with watch mode
docker compose watch

# Changes to src/ trigger automatic restart
```

### Manual Python Setup (without Docker)

```bash
# Install UV
pip install uv

# Install dependencies
uv sync

# Run locally
uv run uvicorn support_agent.api.app:app --reload
```
