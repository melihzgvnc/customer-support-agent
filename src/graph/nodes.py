"""Graph node definitions"""

import chromadb
from rank_bm25 import BM25Okapi
import numpy as np
from langchain.messages import HumanMessage, AIMessage

from graph.states import SupportState, InternalSubgraphState, OutputSubgraphState
from prompts import prompts
from model.classifier import get_classifier_model
from model.reranker import get_reranker_model
from model.responder import get_responder_model
from integrations.zendesk import build_zendesk_payload, create_ticket

def classify_intent(state: SupportState):
    """Classify user intent"""
    
    query = state["messages"][-1]

    prompt = prompts.CLASSIFIER_PROMPT.format(query=query)
    input_msg = HumanMessage(content=prompt)

    response = get_classifier_model().invoke([input_msg])

    return {"query": query ,"intent": response.topic}    

def respond(state: SupportState):
    """Return the answer to the user"""
    
    answer = AIMessage(content=state["answer"])

    return {"messages": [answer], "resolution": "resolved"}

def clarify(state: SupportState):
    """Request more detail from the user"""

    clarify_count = state["clarify_count"]
    clarify_count += 1
    message = """I couldn't find relevant info regarding your question.
    Please provide more details on your issue."""
    message = AIMessage(content=message)

    return {"messages": [message], "clarify_count": clarify_count, "resolution": "pending"}

def escalate(state: SupportState):
    """Escalate the query to human"""
    
    message = """A human will be with you shortly. Please wait.."""
    message = AIMessage(content=message)

    payload = build_zendesk_payload(state)
    create_ticket(payload)

    return {"messages": [message], "resolution": "escalated"}


# ------ SUB-GRAPH (RAG) -------

def dense_search(state: InternalSubgraphState):
    """Vector/Embedding search (dense index) with ChromaDB"""
    
    client = chromadb.PersistentClient(path="path/to/data")
    collection = client.get_collection(name="collection_name")

    query = state["query"]
    query_result = collection.query(query_texts=query)
    
    return {"dense_search_result": query_result}

def sparse_search(state: InternalSubgraphState):
    """Keyword search (sparse index) with BM25"""

    query = state["query"]
    tokenized_query = query

    bm25 = BM25Okapi(tokenized_corpus)
    query_result = bm25.get_top_n(tokenized_query, corpus, n=10)

    return {"sparse_search_result": query_result}

def fuse(state: InternalSubgraphState):
    """Apply Reciprocal Rank Fusion (RRF) over dense and sparse scores"""
    
    dense_search_result = state["dense_search_result"]["documents"][0]
    sparse_search_result = state["sparse_search_result"]

    k = 60 # smoothing_constant
    dense_rank = lambda x: 1 / (k + (dense_search_result.index(x) if x in dense_search_result else 0) + 1)
    sparse_rank = lambda x: 1 / (k + (sparse_search_result.index(x) if x in sparse_search_result else 0) + 1)

    n = 10 # size of each search result
    documents_w_scores = {}
    for i in range(n):
        dense_doc = dense_search_result["documents"][0][i]
        sparse_doc = sparse_search_result[i]

        dense_rrf = dense_rank(dense_doc) + sparse_rank(dense_doc)
        sparse_rrf = dense_rank(sparse_doc) + sparse_rank(sparse_doc)

        documents_w_scores[dense_doc] = dense_rrf
        documents_w_scores[sparse_doc] = sparse_rrf

    documents_w_scores = dict(sorted(documents_w_scores.items(), reverse=True, key=lambda item: item[1]))
    
    result = {}
    for k, v in documents_w_scores.items():
        result[k] = v
        if len(result) == 10:
            break

    return {"fused_ranking": result}

def rerank(state: InternalSubgraphState):
    """Rerank documents with a cross-encoder"""

    query = state["query"]
    docs = state["fused_ranking"]
    
    top_k = 5
    scores = np.array(get_reranker_model().predict([(query, doc) for doc in list(docs.key())]))
    
    indices_of_max_values = np.argpartition(scores, -top_k)[-top_k:]
    result = [list(docs.keys())[i] for i in indices_of_max_values]
    
    return {"retrieved_docs": result}

def generate_answer(state: InternalSubgraphState) -> OutputSubgraphState:
    """Answer to the query based on the retrieved docs"""

    query = state["query"]
    retrieved_docs = state["retrieved_docs"]

    prompt = prompts.RESPONDER_PROMPT.format(query=query, retrieved_docs=retrieved_docs)
    input_msg = HumanMessage(content=prompt)

    response = get_responder_model.invoke([input_msg])
    
    return {"answer": response}