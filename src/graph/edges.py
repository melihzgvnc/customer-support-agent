"""Graph conditional edge definitions"""

from src.graph.states import SupportState
from typing import Literal

def route(state: SupportState) -> Literal["respond", "clarify", "escalate"]:
    answer = state["answer"]

    if not answer.is_answerable:
        return "escalate"
    elif answer.confidence < 7:
        return "clarify"
    else:
        return "respond"