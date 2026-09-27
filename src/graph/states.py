"""Graph state definitions"""

from langgraph.graph import MessagesState
from typing import Literal, List
from chromadb.api.types import QueryResult

class SupportState(MessagesState):
    query: str
    intent: str
    sentiment: str
    confidence: float
    clarify_count: int
    resolution: Literal["resolved", "pending", "escalated"]

class InternalSubgraphState(MessagesState):
    query: str
    dense_search_results: QueryResult
    sparse_search_results: List[List[str]]
