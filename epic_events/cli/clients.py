import argparse
from epic_events.models import Client, User
import sys
import keyring
import getpass
import requests
import json


BASE_URL = 'http://localhost:8000/api/'

# def get_user_id(username, token):
#     headers = {
#         'Authorization': f'Bearer {token}',
#     }
#     response = requests.get(BASE_URL + 'users/', params={'username': username}, headers=headers)
#     if response.status_code != 200:
#         sys.exit('Failed to get user ID. ' + response.text)
#     return response.json()[0]['id']

def get_filtered_clients(token, filters=None):
    if filters is None:
        filters = {}

    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(BASE_URL + 'clients/', params=filters, headers=headers)
    if response.status_code != 200:
        sys.exit('Failed to get clients. ' + response.text)
    
    clients_info = response.json()

    for client in clients_info:
        print(f"Client: {client['full_name']}, Email: {client['email']}, Phone: {client['phone']}, Company: {client['company_name']}, Contact: {client['contact']}")


def get_client_id(email, token):
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(BASE_URL + 'clients/', params={'email': email}, headers=headers)
    if response.status_code != 200:
        sys.exit('Failed to get client ID. ' + response.text)
    return response.json()[0]['id']


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

    response = requests.post(BASE_URL + 'clients/', data=json.dumps(client_data), headers=headers)
    if response.status_code == 201:
        print('Client created successfully.')
    else:
        sys.exit('Failed to create client. ' + response.text)


def update_client(full_name, email, phone, company_name, client_email, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Récupérer l'ID du client à partir de l'email
    client_id = get_client_id(client_email, token)

    # Récupérer les informations du client
    response = requests.get(BASE_URL + f'clients/{client_id}/', headers=headers)
    if response.status_code != 200:
        sys.exit('Failed to get client information. ' + response.text)
    
    client_info = response.json()

    client_data = {
        'full_name': full_name,
        'email': email,
        'phone': phone,
        'company_name': company_name,
        'contact': client_info['contact']
    }

    # Mettre à jour le client
    response = requests.put(BASE_URL + f'clients/{client_id}/', data=json.dumps(client_data), headers=headers)
    if response.status_code == 200:
        print('Client updated successfully.')
    else:
        sys.exit('Failed to update client. ' + response.text)
