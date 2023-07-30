import requests
import json
import sys
from epic_events.cli.controllers import constants, utils
import sentry_sdk
from rich.console import Console


console = Console()
BASE_URL = constants.BASE_URL


def create_user(username, password, email, first_name, last_name, group, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    user_data = {
        'username': username,
        'password': password,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'group': group
    }

    try:
        response = requests.post(BASE_URL + 'users/', data=json.dumps(user_data), headers=headers)
        response.raise_for_status()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        sys.exit('Echec pour créer l utilisateur. ' + str(e))
    console.print('User créé avec succès.', style="bold green")


def update_user(
    username,
    token,
    new_username=None,
    new_password=None,
    new_email=None,
    new_first_name=None,
    new_last_name=None,
    new_group=None
):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    user_id = utils.get_user_id(username, token)
    if user_id is None:
        console.print(f"Aucun utilisateur trouvé avec le username {username}.", style="bold red")
        return

    try:
        # On récupère l'utilisateur
        response = requests.get(BASE_URL + 'users/' + str(user_id) + '/', headers=headers)
        response.raise_for_status()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print('Echec pour obtenir les données utilisateur.')
        return
    user_data = response.json()

    # On met à jour l'utilisateur
    if new_username is not None:
        user_data['username'] = new_username
    if new_password is not None:
        user_data['password'] = new_password
    if new_email is not None:
        user_data['email'] = new_email
    if new_first_name is not None:
        user_data['first_name'] = new_first_name
    if new_last_name is not None:
        user_data['last_name'] = new_last_name
    if new_group is not None:
        user_data['group'] = new_group

    # On met à jour l'utilisteur sur le serveur
    try:
        response = requests.patch(
            BASE_URL + 'users/' + str(user_id) + '/', data=json.dumps(user_data), headers=headers
        )
        response.raise_for_status()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print('Echec pour mettre à jour l utilisateur. ' + str(e))
        return
    console.print('Utilisateur mis à jour avec succès.', style="bold green")


def delete_user(username, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(BASE_URL + f'users/?username={username}', headers=headers)
        response.raise_for_status()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print("Échec de la récupération de l'utilisateur. " + str(e))
        return

    user_data = response.json()
    if user_data:
        user_id = user_data[0]['id']

        try:
            response = requests.delete(BASE_URL + f'users/{user_id}/', headers=headers)
            response.raise_for_status()
        except Exception as e:
            sentry_sdk.capture_exception(e)
            print("Echec pour effacer l'utilisateur. " + str(e))
            return
        console.print('Utilisateur effacé avec succès', style="bold green")
    else:
        console.print(f"Aucun utilisateur trouvé avec le username {username}", style="bold red")
