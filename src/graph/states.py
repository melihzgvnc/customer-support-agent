"""Graph state definitions"""

from dataclasses import dataclass, field
from langgraph.graph import MessagesState
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing import Literal, TypedDict, Annotated
from chromadb.api.types import QueryResult
from src.model.schemas import Answer

@dataclass
class SupportState:
    query: str
    intent: str
    sentiment: str
    intent_confidence: int
    resolution: Literal["resolved", "pending", "escalated"]
    answer: Answer
    clarify_count: int = 0
    messages: Annotated[list[AnyMessage], add_messages] = field(default_factory=list)

class InternalSubgraphState(TypedDict):
    query: str
    dense_search_result: QueryResult
    sparse_search_result: list[str]
    fused_ranking: dict
    retrieved_docs: list[str]
    answer : Answer

class OutputSubgraphState(TypedDict):
    query: str
    retrieved_docs: list[str]
    answer : Answer