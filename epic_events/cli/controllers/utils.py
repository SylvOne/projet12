import requests
import sys
from . import constants
from datetime import datetime


BASE_URL = constants.BASE_URL


def get_client_id(email, token):
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(BASE_URL + 'clients/', params={'email': email}, headers=headers)
    if response.status_code != 200:
        sys.exit('Failed to get client ID. ' + response.text)
    return response.json()[0]['id']


def get_commercial_contact_id(client_id, token):
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(BASE_URL + 'clients/' + str(client_id) + '/', headers=headers)
    if response.status_code != 200:
        sys.exit('Failed to get commercial contact ID. ' + response.text)
    return response.json()['contact']


def get_user_id(username, token):
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(BASE_URL + 'users/', params={'username': username}, headers=headers)
    if response.status_code != 200:
        sys.exit('Failed to get user ID. ' + response.text)
    return response.json()[0]['id']


def convert_date_to_iso(date_str):
    try:
        # Essayez d'abord d'analyser la date au format ISO
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        # Si cela échoue, essayez de l'analyser au format 'dd-mm-yyyy'
        dt = datetime.strptime(date_str, "%d-%m-%Y")
    # Convertir en format ISO
    return dt.strftime("%Y-%m-%d")
