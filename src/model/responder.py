from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from functools import lru_cache
from model.schemas import Answer
from prompts.prompts import RESPONDER_PROMPT

@lru_cache(maxsize=1)
def get_responder_model():
    load_dotenv()
    model = ChatOpenAI(
        model="gpt-5-nano",
        temperature=0,
    )
    return model.with_structured_output(Answer).with_retry(
        retry_if_exception_type=[
            openai.APITimeoutError, openai.APIConnectionError,
            openai.RateLimitError, openai.InternalServerError
            ],
        stop_after_attempt=3
        )
