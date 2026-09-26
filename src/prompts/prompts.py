"""Model prompts"""

CLASSIFIER_PROMPT = """
You are a helpful assistant. 
Your task is to classify intent given a user query.

Here is the query:
<query>{query}<query>

Classify it into one of the topics: billing, technical, account.

Provide confidence score between 1-10 for your prediction. 
"""
