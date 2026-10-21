from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from langgraph.checkpoint.memory import InMemorySaver

from support_agent.api.routers import chat
from support_agent.graph.builder import build_graph

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.graph = build_graph(checkpointer=InMemorySaver())
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(chat.router, tags=["chat"])

