"""Graph state definitions"""

from langgraph.graph import MessagesState
from typing import Literal

class SupportState(MessagesState):
    intent: str
    sentiment: str
    confidence: float
    clarify_count: int
    resolution: Literal["resolved", "pending", "escalated"]
