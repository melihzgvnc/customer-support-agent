# ----STAGE: Base Build & Package Installation----
FROM dhi.io/python:3.12-debian13-dev AS base
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

WORKDIR app/

# Install system compiler/linker tools required for compiling Rust extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv


# ----STAGE: API Dependencies----
FROM base AS api-deps

# Copy lock files and install dependencies *without* the local project
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

# Download the heavy ML model
ENV HF_HOME=/hf
RUN /app/.venv/bin/python3 -c "from sentence_transformers import CrossEncoder; CrossEncoder('BAAI/bge-reranker-v2-m3')"

# Copy the source code and finalize the project installation
COPY src/ ./src/
RUN uv sync --frozen --no-dev


# ----STAGE: Ingestion----
FROM base AS ingest

RUN pip install --no-cache-dir chromadb

COPY ./data/ingestion /app/ingestion

CMD ["uv", "run", "/app/ingestion/ingest.py"]


# ----STAGE: API Runtime----
FROM api-deps AS api

# Copy the pre-built virtual environment and model cache from base
COPY --from=api-deps /app/.venv/ /app/.venv/
COPY --from=api-deps /hf /hf

# Set correct runtime environment variables & fixed virtualenv path
ENV PATH="/app/.venv/bin:$PATH" HF_HOME=/hf HF_HUB_OFFLINE=1
ENV PATH="/root/.local/bin:$PATH"
ENV HF_HOME=/hf

COPY src/ ./src/

USER nobody
CMD ["fastapi", "run", "./src/support_agent/api/app.py"]
