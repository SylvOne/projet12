import getpass
from django.contrib.auth import authenticate
import sys
from epic_events.models import Event, Contract, User
from datetime import datetime
import requests
import json
from datetime import datetime



BASE_URL = 'http://localhost:8000/api/'

def create_event(event_name, contract_id, event_date_start, event_date_end, location, attendees, notes, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    # Conversion des dates du format 'dd-mm-yyyy' au format 'yyyy-mm-ddT00:00:00Z'
    event_date_start_iso = convert_date_to_iso(event_date_start)
    event_date_end_iso = convert_date_to_iso(event_date_end)

    event_data = {
        'event_name': event_name,
        'contract': contract_id,
        'event_date_start': event_date_start_iso,
        'event_date_end': event_date_end_iso,
        'location': location,
        'attendees': attendees,
        'notes': notes
    }

    response = requests.post(BASE_URL + 'events/', data=json.dumps(event_data), headers=headers)
    if response.status_code == 201:
        print('Event created successfully.')
    else:
        sys.exit('Failed to create event. ' + response.text)


def get_filtered_events(token, filters=None):
    
    if filters is None:
        filters = {}

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Conversion des dates du format 'dd-mm-yyyy' au format 'yyyy-mm-dd'
    if 'event_date_start' in filters:
        filters['event_date_start'] = convert_date_to_iso(filters['event_date_start'])
    if 'event_date_end' in filters:
        filters['event_date_end'] = convert_date_to_iso(filters['event_date_end'])
    
    response = requests.get(BASE_URL + 'events/', params=filters, headers=headers)

    if response.status_code == 200:
        events = response.json()
        for event in events:
            print(event)
    else:
        sys.exit('Failed to get events. ' + response.text)


def get_events_no_support_contact(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(BASE_URL + 'events/no_support_contact/', headers=headers)
    if response.status_code == 200:
        events = response.json()
        for event in events:
            print(event)
    else:
        sys.exit('Failed to get events. ' + response.text)


def convert_date_to_iso(date_str):
    """Convert a date from the format 'dd-mm-yyyy' to 'yyyy-mm-dd'"""
    dt = datetime.strptime(date_str, "%d-%m-%Y")
    return dt.strftime("%Y-%m-%d")


def assign_support_contact_to_event(event_id, support_contact_username, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Get the support contact's ID
    response = requests.get(BASE_URL + 'users/', params={'username': support_contact_username}, headers=headers)
    if response.status_code != 200:
        sys.exit('Failed to get user. ' + response.text)

    users = response.json()
    if not users:
        sys.exit(f"No user with username: {support_contact_username} exists.")
    
    support_contact_id = users[0]['id']

    update_data = {
        'support_contact': support_contact_id
    }

    response = requests.patch(BASE_URL + f'events/{event_id}/', data=json.dumps(update_data), headers=headers)
    if response.status_code == 200:
        print('Event updated successfully. Support contact assigned.')
    else:
        sys.exit('Failed to update event. ' + response.text)
