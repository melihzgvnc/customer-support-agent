"""Classifier LLM for intent discovery"""

from langchain_openai import ChatOpenAI
from langchain_openrouter import ChatOpenRouter
from langchain_typesafe import TypeSafeClassifier
from support_agent.model.schemas import Intent
from dotenv import load_dotenv
from functools import lru_cache
import openai

@lru_cache(maxsize=1)
def get_classifier_model():
    load_dotenv()
    
    model = ChatOpenRouter(
        model="~deepseek/deepseek-flash-latest", 
        temperature=0, 
        max_tokens=1024, 
        max_retries=3
    )
    # model = ChatOpenAI(model="gpt-5-nano", temperature=0).with_retry(
    #     retry_if_exception_type=(openai.APITimeoutError, openai.APIConnectionError,
    #     openai.RateLimitError, openai.InternalServerError),
    #     stop_after_attempt=3
    # )

    return model.with_structured_output(Intent)

@lru_cache(maxsize=1)
def get_classifier_jev_model():
    load_dotenv()
    model = TypeSafeClassifier()

    return model