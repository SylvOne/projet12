import requests
import keyring
import sys
import json


BASE_URL = 'http://localhost:8000/api/'

def authenticate(username, password):
    response = requests.post(BASE_URL + 'token/', data={'username': username, 'password': password})
    if response.status_code != 200:
        sys.exit('Invalid username or password.')
    token = response.json()['access']

    # Stockage du token dans le keyring
    keyring.set_password("epicevents", "jwt_token", token)

    # Obtention et stockage de l'ID de l'utilisateur
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(BASE_URL + 'me/', headers=headers)
    if response.status_code != 200:
        sys.exit('Failed to get current user ID. ' + response.text)
    user_id = str(response.json()['id'])

    # Stockage de l'ID de l'utilisateur dans le keyring
    keyring.set_password("epicevents", "user_id", user_id)

    print("Thanks for your connection")

    return token