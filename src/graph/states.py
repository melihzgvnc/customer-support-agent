"""Graph state definitions"""

from dataclasses import dataclass, field
from langgraph.graph import MessagesState
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing import Literal, List, Dict, TypedDict, Annotated
from chromadb.api.types import QueryResult
from model.schemas import Answer

@dataclass
class SupportState:
    messages: Annotated[List[AnyMessage], add_messages] = field(default_factory=List)
    query: str
    intent: str
    sentiment: str
    intent_confidence: int
    clarify_count: int = 0
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