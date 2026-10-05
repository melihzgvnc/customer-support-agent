import requests
import os
import json
import sys
from pydantic_core import to_jsonable_python
from src.graph.states import SupportState
# Load OAuth access token and configuration from environment variables (ensure these are set)


ZENDESK_SUBDOMAIN = os.getenv('ZENDESK_SUBDOMAIN')
ZENDESK_CLIENT_ID = os.getenv('ZENDESK_CLIENT_ID')
ZENDESK_CLIENT_SECRET = os.getenv('ZENDESK_CLIENT_SECRET')

URL = f"https://{os.environ['ZENDESK_SUBDOMAIN']}.zendesk.com/oauth/tokens"

payload = {
  "grant_type": "client_credentials",
  "client_id": os.environ['ZENDESK_CLIENT_ID'],
  "client_secret": os.environ['ZENDESK_CLIENT_SECRET'],
  "scope": "read write"
}

response = requests.post(url=URL, json=payload)
ZENDESK_ACCESS_TOKEN = json.loads(response.content)['access_token']


if not ZENDESK_ACCESS_TOKEN or not ZENDESK_SUBDOMAIN:
    print('Error: Missing required Zendesk environment variables.')
    exit(1)

def build_zendesk_payload(state: SupportState):
    """Package the data in a dictionary matching the expected Zendesk JSON Format"""

    subject = f"Bot Escalation - {state['intent'].upper()}"
    transcript = "\n".join([f"{msg.type}: {msg.content}" for msg in state["messages"]])
    summary = (
        f"Escalated by bot\n"
        f"Intent: {state['intent']} | Confidence: {state['intent_confidence']}\n\n"
        f"{transcript}"
    )

    return {
        'ticket': {
            'subject': subject,
            'comment': {
                'body': summary
            },
            'priority': 'urgent',
            'tags': ['escalation', f"{state['intent']}"],
            # 'metadata': {
            #     'custom': to_jsonable_python(state)
            # }
        }
    }


def create_ticket(payload):
    """Send POST request to create a new ticket"""
    
    url = f'https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2/tickets'

    HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ZENDESK_ACCESS_TOKEN}'
    }

    # Serialize the data dictionary to a JSON string

    try:
        # Do the HTTP post request with serialized JSON payload and headers
        print(payload)
        response = requests.post(url, json=payload, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f'Request failed: {e}') from e
        print(response.json())
        

    # Report success
    print('Successfully created the ticket.')
    print(response.json())
