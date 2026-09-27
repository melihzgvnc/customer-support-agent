from sentence_transformers import CrossEncoder
from functools import lru_cache

@lru_cache(maxsize=1)
def get_reranker(model_path="BAAI/bge-reranker-v2-m3"):
    reranker = CrossEncoder(model_path)
    return reranker