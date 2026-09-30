"""Graph conditional edge definitions"""

from graph.states import SupportState
from typing import Literal

def route(state: SupportState) -> Literal["respond", "clarify", "escalate"]:
    answer = state["answer"]
    confidence = answer.confidence

    if not answer.is_answerable:
        return "escalate"
    elif answer.confidence < 7:
        return "clarify"
    else:
        return "respond"