import requests
import keyring
import sys
import json
from . import constants
from rich.console import Console



console = Console()
BASE_URL = constants.BASE_URL

def authenticate(username, password):
    response = requests.post(BASE_URL + 'token/', data={'username': username, 'password': password})
    if response.status_code != 200:
        sys.exit('Mot de passe ou username invalide.')
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

    console.print("Merci pour votre connexion", style="bold green")

    return token