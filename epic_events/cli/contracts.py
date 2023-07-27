import sys
import requests
import json

BASE_URL = 'http://localhost:8000/api/'

def create_contract(client_email, total_amount, amount_due, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    client_id = get_client_id(client_email, token)
    commercial_contact_id = get_commercial_contact_id(client_id, token)

    contract_data = {
        'client': client_id,
        'commercial_contact': commercial_contact_id,
        'total_amount': total_amount,
        'amount_due': amount_due
    }

    response = requests.post(BASE_URL + 'contracts/', data=json.dumps(contract_data), headers=headers)
    if response.status_code == 201:
        print('Contract created successfully.')
    else:
        sys.exit('Failed to create contract. ' + response.text)


def update_contract(contract_id, client_email, total_amount, amount_due, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    client_id = get_client_id(client_email, token)
    commercial_contact_id = get_commercial_contact_id(client_id, token)

    contract_data = {
        'client': client_id,
        'commercial_contact': commercial_contact_id,
        'total_amount': total_amount,
        'amount_due': amount_due
    }

    response = requests.put(BASE_URL + f'contracts/{contract_id}/', data=json.dumps(contract_data), headers=headers)
    if response.status_code == 200:
        print('Contract updated successfully.')
    else:
        sys.exit('Failed to update contract. ' + response.text)



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


def get_filtered_contracts(token, filters=None):

    if filters is None:
        filters = {}

    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(BASE_URL + 'contracts/', params=filters, headers=headers)
    if response.status_code != 200:
        sys.exit('Failed to get contracts. ' + response.text)
    contracts = response.json()
    for contract in contracts:
        print(contract)
