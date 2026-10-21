"""Endpoint definitions for graph streaming"""

from fastapi import APIRouter, Depends
from typing import Annotated, Callable
from uuid import uuid4

from support_agent.api.dependencies import get_graph
from support_agent.services.agent_service import aget_response
from support_agent.api.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", tags=["chat"])
async def send_query(req: ChatRequest, graph: Annotated[Callable, Depends(get_graph)]) -> ChatResponse:
    thread_id = req.thread_id or uuid4()
    config = {"configurable": {"thread_id": str(thread_id)}}
    response =  await aget_response(req.query, config, graph)
    return ChatResponse(thread_id=thread_id, answer=response)