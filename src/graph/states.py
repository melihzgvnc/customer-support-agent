"""Graph state definitions"""

from langgraph.graph import MessagesState
from typing import Literal, List, Dict
from chromadb.api.types import QueryResult

class SupportState(MessagesState):
    query: str
    intent: str
    sentiment: str
    confidence: float
    clarify_count: int
    resolution: Literal["resolved", "pending", "escalated"]
    answer: str

class InternalSubgraphState(MessagesState):
    query: str
    dense_search_result: QueryResult
    sparse_search_result: List[str]
    fused_ranking: Dict
    retrieved_docs: List[str]
    answer : str