import sys
import requests
import json
from epic_events.cli.controllers import constants, utils
import sentry_sdk
from rich.console import Console


console = Console()
BASE_URL = constants.BASE_URL


def create_event(event_name, contract_id, event_date_start, event_date_end, location, attendees, notes, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    # Conversion des dates du format 'dd-mm-yyyy' au format 'yyyy-mm-ddT00:00:00Z'
    event_date_start_iso = utils.convert_date_to_iso(event_date_start)
    event_date_end_iso = utils.convert_date_to_iso(event_date_end)

    event_data = {
        'event_name': event_name,
        'contract': contract_id,
        'event_date_start': event_date_start_iso,
        'event_date_end': event_date_end_iso,
        'location': location,
        'attendees': attendees,
        'notes': notes
    }
    try:
        response = requests.post(BASE_URL + 'events/', data=json.dumps(event_data), headers=headers)
        response.raise_for_status()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        sys.exit('Failed to create event. ' + str(e))
    console.print('Event créé avec succès.', style="bold green")


def get_filtered_events(token, filters=None):
    if filters is None:
        filters = {}

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # Conversion des dates du format 'dd-mm-yyyy' au format 'yyyy-mm-ddT00:00:00Z'
    if 'event_date_start' in filters:
        filters['event_date_start'] = utils.convert_date_to_iso(filters['event_date_start'])
    if 'event_date_end' in filters:
        filters['event_date_end'] = utils.convert_date_to_iso(filters['event_date_end'])
    try:
        response = requests.get(BASE_URL + 'events/', params=filters, headers=headers)
        response.raise_for_status()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        sys.exit('Echec pour obtenir les evenements. ' + str(e))
    events = response.json()
    for event in events:
        console.print(event)


def get_events_no_support_contact(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(BASE_URL + 'events/no_support_contact/', headers=headers)
        response.raise_for_status()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        sys.exit('Echec pour obtenir l evenement. ' + str(e))
    events = response.json()
    for event in events:
        console.print(event)


def assign_support_contact_to_event(event_id, support_contact_username, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(BASE_URL + 'users/', params={'username': support_contact_username}, headers=headers)
        response.raise_for_status()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        sys.exit('Echec pour obtenir l utilisateur. ' + str(e))
    users = response.json()
    if not users:
        sys.exit(f"Aucun utilisateur avec le username: {support_contact_username} exists.")
    support_contact_id = users[0]['id']

    update_data = {
        'support_contact': support_contact_id
    }

    try:
        response = requests.patch(BASE_URL + f'events/{event_id}/', data=json.dumps(update_data), headers=headers)
        response.raise_for_status()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        sys.exit('Failed to update event. ' + str(e))
    console.print('Evenement mis à jour. Support contact assigné.', style="bold green")


def update_event(
    event_id,
    event_name=None,
    contract_id=None,
    event_date_start=None,
    event_date_end=None,
    location=None,
    attendees=None,
    notes=None,
    token=None
):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    # Conversion des dates du format 'dd-mm-yyyy' au format 'yyyy-mm-ddT00:00:00Z'
    event_date_start_iso = utils.convert_date_to_iso(event_date_start) if event_date_start else None
    event_date_end_iso = utils.convert_date_to_iso(event_date_end) if event_date_end else None

    update_data = {
        'event_name': event_name,
        'contract': contract_id,
        'event_date_start': event_date_start_iso,
        'event_date_end': event_date_end_iso,
        'location': location,
        'attendees': attendees,
        'notes': notes
    }

    # Suppression des clés avec des valeurs None
    update_data = {k: v for k, v in update_data.items() if v is not None}

    try:
        response = requests.patch(BASE_URL + f'events/{event_id}/', data=json.dumps(update_data), headers=headers)
        response.raise_for_status()
    except Exception as e:
        # Enregistrement de l'exception dans Sentry
        sentry_sdk.capture_exception(e)
        sys.exit('Echec pour mettre à jour l evenement. ' + str(e))

    console.print('Evenement mis à jour avec succès.', style="bold green")
