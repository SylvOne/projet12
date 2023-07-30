import sys
import requests
import json
from epic_events.cli.controllers import constants, utils
import sentry_sdk
from rich.console import Console


console = Console()
BASE_URL = constants.BASE_URL


def create_contract(client_email, total_amount, amount_due, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    client_id = utils.get_client_id(client_email, token)
    commercial_contact_id = utils.get_commercial_contact_id(client_id, token)

    contract_data = {
        'client': client_id,
        'commercial_contact': commercial_contact_id,
        'total_amount': total_amount,
        'amount_due': amount_due
    }

    try:
        response = requests.post(BASE_URL + 'contracts/', data=json.dumps(contract_data), headers=headers)
        response.raise_for_status()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        sys.exit('Failed to create contract. ' + response.text)
    console.print('Contract créé avec succès.', style="bold green")


def update_contract(contract_id, client_email, total_amount, amount_due, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    client_id = utils.get_client_id(client_email, token)
    commercial_contact_id = utils.get_commercial_contact_id(client_id, token)

    contract_data = {
        'client': client_id,
        'commercial_contact': commercial_contact_id,
        'total_amount': total_amount,
        'amount_due': amount_due
    }

    try:
        response = requests.put(
            BASE_URL + f'contracts/{contract_id}/', data=json.dumps(contract_data), headers=headers
        )
        response.raise_for_status()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        sys.exit('Failed to update contract. ' + response.text)
    console.print('Contrat mis à jour avec succès.', style="bold green")


def update_contract_status(contract_id, status, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    contract_data = {
        'status': status,
    }

    try:
        response = requests.patch(
            BASE_URL + f'contracts/{contract_id}/', data=json.dumps(contract_data), headers=headers
        )
        response.raise_for_status()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        sys.exit('Failed to update contract status. ' + response.text)
    console.print('Statut du contrat mis à jour avec succès.', style="bold green")


def get_filtered_contracts(token, filters=None):
    if filters is None:
        filters = {}

    headers = {
        'Authorization': f'Bearer {token}',
    }
    try:
        response = requests.get(BASE_URL + 'contracts/', params=filters, headers=headers)
        response.raise_for_status()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        sys.exit('Echec pour obtenir les contrats. ' + response.text)
    contracts = response.json()
    for contract in contracts:
        console.print(contract)
