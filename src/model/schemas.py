"""Output schemas for LLMs"""

from pydantic import BaseModel, Field

class Intent(BaseModel):
    topic: Literal["billing", "technical", "account"] = Field(description="Topic that is to which the query is predicted to belong")
    confidence: float = Field(description="Confidence score of the prediction")


class Answer(BaseModel):
    is_answerable: bool = Field(description="Whether a query is answerable based on context")
    answer: str = Field(default="", description="Answer to a given query")
    confidence: int = Field(description="How confident the answer is given context")