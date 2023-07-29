import argparse
from epic_events.models import Client, User
import sys
import keyring
import getpass
import requests
import json
from epic_events.cli.controllers import constants, utils
import sentry_sdk
from rich.console import Console


console = Console()
BASE_URL = constants.BASE_URL


def get_filtered_clients(token, filters=None):
    if filters is None:
        filters = {}

    headers = {
        'Authorization': f'Bearer {token}',
    }
    try:
        response = requests.get(BASE_URL + 'clients/', params=filters, headers=headers)
        response.raise_for_status()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        sys.exit('Failed to get clients. ' + response.text)
    
    clients_info = response.json()

    for client in clients_info:
        console.print(f"Client: {client['full_name']}, Email: {client['email']}, Phone: {client['phone']}, Company: {client['company_name']}, Contact: {client['contact']}", style="bold blue")



def create_client(full_name, email, phone, company_name, commercial_id, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    

    client_data = {
        'full_name': full_name,
        'email': email,
        'phone': phone,
        'company_name': company_name,
        'contact': int(commercial_id)
    }

    try:
        response = requests.post(BASE_URL + 'clients/', data=json.dumps(client_data), headers=headers)
        response.raise_for_status()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        sys.exit('Failed to create client. ' + response.text)

    console.print('Client créé avec succès.', style="bold green")


def update_client(full_name, email, phone, company_name, client_email, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Récupérer l'ID du client à partir de l'email
    client_id = utils.get_client_id(client_email, token)

    try:
        # Récupérer les informations du client
        response = requests.get(BASE_URL + f'clients/{client_id}/', headers=headers)
        response.raise_for_status()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        sys.exit('Echec pour obtenir les informations du client. ' + response.text)

    
    client_info = response.json()

    client_data = {
        'full_name': full_name,
        'email': email,
        'phone': phone,
        'company_name': company_name,
        'contact': client_info['contact']
    }

    try:
        # Mettre à jour le client
        response = requests.put(BASE_URL + f'clients/{client_id}/', data=json.dumps(client_data), headers=headers)
        response.raise_for_status()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        sys.exit('Echec pour mettre à jour le client. ' + response.text)

    console.print('Client mis à jour avec succès.', style="bold green")
