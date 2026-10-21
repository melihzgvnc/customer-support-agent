"""Model prompts"""

CLASSIFIER_PROMPT = """
Your task is to classify intent given a user query.

Here is the query:
<query>{query}</query>

Classify it into one of the topics: account, billing, data privacy, api usage, troubleshooting.

Provide confidence score between 1-10 for your prediction. 
"""

JEV_CLASSIFIER_INSTRUCTION = """Which department does this query belong to?"""

JEV_CLASSIFIER_CRITERIA = {
        "account": "Login/signup, account management issues",  
        "billing": "Payment, invoice or subscription issues", 
        "data privacy": "User data, data storage/deletion related queries", 
        "api usage": "API docs, technical related issues", 
        "troubleshooting": "Product bugs, system errors"
    }

RESPONDER_PROMPT = """
You are a helpful assistant.
Your task is to first decide if a query is answerable given some context 
and if so provide an answer. If not answerable, just leave it unanswered.
You also need to provide a confidence score between 1-10 along with the answer (0 if not answerable).

Here is the query and context:

<query>{query}</query>

<context>{retrieved_docs}</context>
"""