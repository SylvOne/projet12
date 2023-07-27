import requests
import json
import sys


BASE_URL = 'http://localhost:8000/api/'

def create_user(username, password, email,first_name, last_name, group, token):
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

    response = requests.post(BASE_URL + 'users/', data=json.dumps(user_data), headers=headers)
    if response.status_code == 201:
        print('User created successfully.')
    else:
        sys.exit('Failed to create user. ' + response.text)


def update_user(username, token, new_username=None, new_password=None, new_email=None, new_first_name=None, new_last_name=None, new_group=None):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    user_id = get_user_id(username, token)
    if user_id is None:
        print(f"No user found with username {username}.")
        return

    # Get current user data
    response = requests.get(BASE_URL + 'users/' + str(user_id) + '/', headers=headers)
    if response.status_code != 200:
        print('Failed to get user data.')
        return
    user_data = response.json()

    # Update user data
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

    # Update user on the server
    response = requests.patch(BASE_URL + 'users/' + str(user_id) + '/', data=json.dumps(user_data), headers=headers)
    if response.status_code == 200:
        print('User updated successfully.')
    else:
        print('Failed to update user. ' + response.text)




def delete_user(username, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(BASE_URL + f'users/?username={username}', headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        if user_data:
            user_id = user_data[0]['id']
            response = requests.delete(BASE_URL + f'users/{user_id}/', headers=headers)
            if response.status_code == 204:
                print('User deleted successfully.')
            else:
                print('Failed to delete user. ' + response.text)
        else:
            print(f"No user found with username {username}")
    else:
        print('Failed to retrieve user. ' + response.text)

def get_user_id(username, token):
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(BASE_URL + 'users/', params={'username': username}, headers=headers)
    if response.status_code != 200:
        sys.exit('Failed to get user ID. ' + response.text)
    return response.json()[0]['id']