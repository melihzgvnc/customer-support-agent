from langchain_openai import ChatOpenAI
from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
from functools import lru_cache
from support_agent.model.schemas import Answer
from support_agent.prompts.prompts import RESPONDER_PROMPT
import openai

@lru_cache(maxsize=1)
def get_responder_model():
    load_dotenv()
    
    model = ChatOpenRouter(
        model="~deepseek/deepseek-flash-latest", 
        temperature=0, 
        max_tokens=1024, 
        max_retries=3,
        streaming=True
    )

    fallback_model_1 = ChatOpenRouter(
        model="~deepseek/deepseek-flash-latest",
        temperature=0,
        max_tokens=1024,
        max_retries=3,
        streaming=True
    ).with_structured_output(Answer)

    fallback_model_2 = ChatOpenAI(
        model="gpt-5-nano",
        temperature=0,
        streaming=True
    ).with_structured_output(Answer).with_retry(
        retry_if_exception_type=[
            openai.APITimeoutError, openai.APIConnectionError,
            openai.RateLimitError, openai.InternalServerError
            ],
        stop_after_attempt=3
        )

    return model.with_structured_output(Answer).with_fallbacks([fallback_model_1, fallback_model_2])