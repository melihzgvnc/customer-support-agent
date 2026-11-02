"""Graph builder"""
import os
from support_agent.config import get_settings
from typing import Literal

from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.checkpoint.memory import InMemorySaver
from support_agent.graph.states import InputState, SupportState, InternalSubgraphState, OutputSubgraphState
from support_agent.graph.edges import route
from support_agent.graph.nodes import (
    classify_intent, respond, clarify, escalate,
    dense_search, sparse_search, fuse, rerank, generate_answer
)

settings = get_settings()

# Sub-Graph Constructuion
sub_builder = StateGraph(
    state_schema=InternalSubgraphState, 
    output_schema=OutputSubgraphState
)

sub_builder.add_node(dense_search)
sub_builder.add_node(sparse_search)
sub_builder.add_node(fuse)
sub_builder.add_node(rerank)
sub_builder.add_node(generate_answer)

sub_builder.add_edge(START, 'dense_search')
sub_builder.add_edge(START, 'sparse_search')
sub_builder.add_edge('dense_search', 'fuse')
sub_builder.add_edge('sparse_search', 'fuse')
sub_builder.add_edge('fuse', 'rerank')
sub_builder.add_edge('rerank', 'generate_answer')
sub_builder.add_edge('generate_answer', END)

subgraph = sub_builder.compile()

# Main Graph Constructuion
builder = StateGraph(SupportState, input_schema=InputState)

builder.add_node(classify_intent)
builder.add_node('subgraph', subgraph)
builder.add_node(respond)
builder.add_node(clarify)
builder.add_node(escalate)

builder.add_edge(START, 'classify_intent')
builder.add_edge('classify_intent', 'subgraph')
builder.add_conditional_edges('subgraph', route)
builder.add_edge('respond', END)
builder.add_edge('clarify', END)
builder.add_edge('escalate', END)
