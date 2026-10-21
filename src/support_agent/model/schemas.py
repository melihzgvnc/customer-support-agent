"""Output schemas for LLMs"""

from pydantic import BaseModel, Field
from typing import Literal

class Intent(BaseModel):
    topic: Literal["account", "billing", "data privacy", "api usage", "troubleshooting"] = Field(description="Topic that is to which the query is predicted to belong")
    confidence: float = Field(description="Confidence score of the prediction")

class Answer(BaseModel):
    is_answerable: bool = Field(description="Whether the query is answerable based on the context")
    answer: str = Field(default="", description="Answer to the given query")
    confidence: int = Field(description="How confident the answer is given the context")