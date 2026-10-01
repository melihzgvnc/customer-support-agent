"""Graph state definitions"""

from langgraph.graph import MessagesState
from typing import Literal, List, Dict. TypedDict
from chromadb.api.types import QueryResult
from model.schemas import Answer

class SupportState(MessagesState):
    query: str
    intent: str
    sentiment: str
    intent_confidence: int
    clarify_count: 0
    resolution: Literal["resolved", "pending", "escalated"]
    answer: Answer

class InternalSubgraphState(TypedDict):
    query: str
    dense_search_result: QueryResult
    sparse_search_result: List[str]
    fused_ranking: Dict
    retrieved_docs: List[str]
    answer : Answer

class OutputSubgraphState(TypedDict):
    query: str
    retrieved_docs: List[str]
    answer : Answer