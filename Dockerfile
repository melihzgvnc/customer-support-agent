# ----STAGE: Base Build & Package Installation----
FROM dhi.io/python:3.12-debian13-dev AS base
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system compiler/linker tools required for compiling Rust extensions
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv


# ----STAGE: API Dependencies----
FROM base AS api-deps

# Copy lock files and install dependencies *without* the local project
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

# Download the heavy ML model
ENV HF_HOME=/hf
RUN /app/.venv/bin/python3 -c "\
from sentence_transformers import CrossEncoder, SentenceTransformer; \
CrossEncoder('BAAI/bge-reranker-v2-m3'); \
SentenceTransformer('BAAI/bge-small-en-v1.5')"

# Copy the source code and finalize the project installation
COPY src/ ./src/
RUN uv sync --frozen --no-dev


# ----STAGE: Ingestion----
FROM api-deps AS ingest

COPY ./data/ingestion /app/ingestion

CMD ["uv", "run", "--no-sync", "/app/ingestion/ingest.py"]


# ----STAGE: API Runtime----
FROM api-deps AS api

# Set correct runtime environment variables & fixed virtualenv path
ENV PATH="/app/.venv/bin:$PATH" HF_HOME=/hf HF_HUB_OFFLINE=1

USER nobody
# CMD ["fastapi", "run", "./src/support_agent/api/app.py"]
CMD ["uvicorn", "support_agent.api.app:app", "--host", "0.0.0.0", "--port", "9000"]