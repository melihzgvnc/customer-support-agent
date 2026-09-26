"""Graph node definitions"""

from langchain.messages import HumanMessage
from graph.states import SupportState
from prompts import prompts
from model.classifier import get_classifier_model

def classify_intent(state: SupportState):
    """Classify user intent"""
    
    query = state["messages"][-1]

    prompt = prompts.CLASSIFIER_PROMPT.format(query=query)
    input_msg = HumanMessage(content=prompt)

    classifier = get_classifier_model()
    result = classifier.invoke([input_msg])
    
        

def retrieve_and_answer(state):
    pass

def respond(state):
    pass

def clarify(state):
    pass

def escalate(state):
    pass

