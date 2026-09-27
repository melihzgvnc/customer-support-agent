"""Graph node definitions"""

import chromadb
from rank_bm25 import BM25Okapi
from langchain.messages import HumanMessage
from graph.states import SupportState, InternalSubgraphState
from prompts import prompts
from model.classifier import get_classifier_model

def classify_intent(state: SupportState):
    """Classify user intent"""
    
    query = state["messages"][-1]

    prompt = prompts.CLASSIFIER_PROMPT.format(query=query)
    input_msg = HumanMessage(content=prompt)

    response = get_classifier_model().invoke([input_msg])

    return {"query": query ,"intent": response.topic}    

def retrieve_and_answer(state):
    pass

def respond(state):
    pass

def clarify(state):
    pass

def escalate(state):
    pass


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

def fuse():
    pass

def rerank():
    pass

def generate_answer():
    pass