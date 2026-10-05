"""Classifier LLM for intent discovery"""

from langchain_openai import ChatOpenAI
from langchain_typesafe import TypeSafeClassifier
from src.model.schemas import Intent
from dotenv import load_dotenv
from functools import lru_cache
import openai

@lru_cache(maxsize=1)
def get_classifier_model():
    load_dotenv()
    model = ChatOpenAI(model="gpt-5-nano", temperature=0)
    return model.with_structured_output(Intent).with_retry(
        retry_if_exception_type=(openai.APITimeoutError, openai.APIConnectionError,
        openai.RateLimitError, openai.InternalServerError),
        stop_after_attempt=3
    )

@lru_cache(maxsize=1)
def get_classifier_jev_model():
    load_dotenv()
    model = TypeSafeClassifier()

    return model