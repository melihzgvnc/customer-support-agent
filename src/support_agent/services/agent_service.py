"""Thin wrapper over the graph"""
from langchain_core.messages import HumanMessage
import asyncio

async def aget_response(query, config, graph):
    input_message = {"messages": [HumanMessage(content=query)]}
    response = await graph.ainvoke(input=input_message, config=config)
    last_message = response["messages"][-1]
    return last_message.content

