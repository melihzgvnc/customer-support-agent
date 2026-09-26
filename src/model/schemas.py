"""Output schemas for LLMs"""

from pydantic import BaseModel, Field

class Intent(BaseModel):
    topic: Literal["billing", "technical", "account"] = Field(description="Topic that is to which the query is predicted to belong")
    confidence: float = Field(description="Confidence score of the prediction")
    