from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from support_agent.api.routers import chat
from support_agent.graph.builder import builder
from support_agent.config import get_settings

settings = get_settings()

username = settings.db.postgres_user
password = settings.db.postgres_password.get_secret_value()
db_name = settings.db.postgres_db
DB_URI=f"postgresql://{username}:{password}@db:5432/{db_name}?sslmode=disable"

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncPostgresSaver.from_conn_string(DB_URI) as checkpointer:
        await checkpointer.setup()
        app.state.graph = builder.compile(checkpointer=checkpointer)
        yield

app = FastAPI(lifespan=lifespan)

app.include_router(chat.router, tags=["chat"])

