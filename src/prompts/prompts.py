"""Model prompts"""

CLASSIFIER_PROMPT = """
Your task is to classify intent given a user query.

Here is the query:
<query>{query}</query>

Classify it into one of the topics: billing, technical, account.

Provide confidence score between 1-10 for your prediction. 
"""

RESPONDER_PROMPT = """
You are a helpful assistant.
Your task is to first decide if a query is answerable given some context 
and if so provide an answer. If not answerable, just leave it unanswered.
You also need to provide a confidence score between 1-10 along with the answer (0 if not answerable).

Here is the query and context:

<query>{query}</query>

<context>{retrieved_docs}</context>
"""