import requests
import os
import json
from graph.states import SupportState
# Load OAuth access token and configuration from environment variables (ensure these are set)
ZENDESK_SUBDOMAIN = os.getenv('ZENDESK_SUBDOMAIN')
ZENDESK_ACCESS_TOKEN = os.getenv('ZENDESK_ACCESS_TOKEN')

if not ZENDESK_ACCESS_TOKEN or not ZENDESK_SUBDOMAIN:
    print('Error: Missing required environment variables.')
    exit(1)

def build_zendesk_payload(state: SupportState):
    """Package the data in a dictionary matching the expected Zendesk JSON Format"""

    subject = f"Bot Escalation - {state['intent'].upper()}"
    transcript = "\n".join([f"{msg['role']}: {msg['content']}" for msg in state["messages"]])
    summary = (
        f"Escalated by bot\n"
        f"Intent: {state['intent']} | Confidence: {state['confidence']:.2f}\n\n"
        f"{transcript}"
    )

    return {
        'ticket': {
            'subject': subject,
            'comment': {
                'body': summary
            },
            'prioriy': 'urgent',
            'tags': ['escalation', f"{state['intent']}"],
            'metadata': {
                'custom': state
            }
        }
    }


def create_ticket(payload):
    """Send POST request to create a new ticket"""
    
    data = payload
    url = f'https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2/tickets.json'

    HEADERS = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ZENDESK_ACCESS_TOKEN}'
    }

    # Serialize the data dictionary to a JSON string
    payload = json.dumps(data)

    try:
        # Do the HTTP post request with serialized JSON payload and headers
        response = requests.post(url, data=payload, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
        exit(1)

    # Report success
    print('Successfully created the ticket.')
    print(response.json())
