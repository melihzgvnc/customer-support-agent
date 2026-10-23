"""Classifier LLM for intent discovery"""

from langchain_openai import ChatOpenAI
from langchain_openrouter import ChatOpenRouter
from langchain_typesafe import TypeSafeClassifier
from support_agent.model.schemas import Intent
from support_agent.config import get_settings
import os
from functools import lru_cache
import openai

settings = get_settings()

@lru_cache(maxsize=1)
def get_classifier_model():

    model = ChatOpenRouter(
        model="~deepseek/deepseek-flash-latest",
        api_key=settings.llm.openrouter_api_key, 
        temperature=0, 
        max_tokens=1024, 
        max_retries=3
    )
    return model.with_structured_output(Intent)

@lru_cache(maxsize=1)
def get_classifier_jev_model():
    model = TypeSafeClassifier(
        api_key = settings.llm.openrouter_api_key,
        base_url = settings.llm.openrouter_base_url
    )
    return model