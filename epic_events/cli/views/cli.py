import os
import sys
# Chemin absolu vers le dossier du projet
dossier_projet = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
# Ajout du dossier du projet au chemin Python
sys.path.append(dossier_projet)
# Définition du module de configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet12.settings')
import django  # noqa: E402
django.setup()
import keyring  # noqa: E402
import getpass  # noqa: E402
import argparse  # noqa: E402
from epic_events.cli.controllers import login, disconnect  # noqa: E402
from epic_events.cli.models import gestion, clients, contracts, events  # noqa: E402


# Création du parser de niveau supérieur
parser = argparse.ArgumentParser(prog='PROG')
subparsers = parser.add_subparsers(help='sub-command help')


# Création du parser pour la commande "create_user"
parser_create_user = subparsers.add_parser('create_user', help='Create a new user')
parser_create_user.add_argument('--username', required=True, help='Username for the new user')
parser_create_user.add_argument('--email', required=True, help='Email for the new user')
parser_create_user.add_argument('--first_name', required=True, help='First name for the new user')
parser_create_user.add_argument('--last_name', required=True, help='Last name for the new user')
parser_create_user.add_argument('--group', required=True, help='Group for the new user')

# Création du parser pour la commande "update_user"
parser_update_user = subparsers.add_parser('update_user', help='Update a user')
parser_update_user.add_argument('--username', required=True, help='Username of the user to update')
parser_update_user.add_argument('--new_username', help='New username for the user')
parser_update_user.add_argument('--password', help='New password for the user')
parser_update_user.add_argument('--email', help='New email for the user')
parser_update_user.add_argument('--first_name', help='New first name for the user')
parser_update_user.add_argument('--last_name', help='New last name for the user')
parser_update_user.add_argument('--group', help='New group for the user')

# Création du parser pour la commande "delete_user"
parser_delete_user = subparsers.add_parser('delete_user', help='Delete a user')
parser_delete_user.add_argument('--username', required=True, help='Username of the user to delete')


# Création du parser pour la commande "clients"
parser_clients = subparsers.add_parser('clients', help='clients command help')
parser_clients.add_argument('action', choices=['create', 'update', 'delete', 'list'])
parser_clients.add_argument('--full_name', required='create' in sys.argv or 'update' in sys.argv)
parser_clients.add_argument('--email', required='create' in sys.argv or 'update' in sys.argv)
parser_clients.add_argument('--phone', required='create' in sys.argv or 'update' in sys.argv)
parser_clients.add_argument('--company_name', required='create' in sys.argv or 'update' in sys.argv)
parser_clients.add_argument('--client_email', required='update' in sys.argv)
parser_clients.add_argument('--filters', nargs='+', action='append')


# Création du parser pour la commande "contracts"
parser_contracts = subparsers.add_parser('contracts', help='contracts command help')
parser_contracts.add_argument('action', choices=['create', 'update', 'delete', 'list', 'update_status'])
parser_contracts.add_argument('--contract_id', type=int)
parser_contracts.add_argument('--client_email')
parser_contracts.add_argument('--total_amount', type=float)
parser_contracts.add_argument('--amount_due', type=float)
parser_contracts.add_argument('--filters', nargs='+', action='append')
parser_contracts.add_argument('--status', required='update_status' in sys.argv)


# Création du parser pour la commande "events"
parser_events = subparsers.add_parser('events', help='events command help')
parser_events.add_argument('action', choices=['create', 'assign_support', 'list', 'update', 'no_support_contact'])
parser_events.add_argument('--event_name', required='create' in sys.argv)
parser_events.add_argument('--contract_id', required='create' in sys.argv, type=int)
parser_events.add_argument('--event_date_start', required='create' in sys.argv)
parser_events.add_argument('--event_date_end', required='create' in sys.argv)
parser_events.add_argument('--location', required='create' in sys.argv)
parser_events.add_argument('--attendees', required='create' in sys.argv, type=int)
parser_events.add_argument('--notes', required='create' in sys.argv)
# arguments pour la liste d'événements
parser_events.add_argument('--filters', nargs='+', action='append')

# arguments spécifiques à la commande 'assign_support' pour le parser 'events'
parser_events.add_argument('--event_id', required='assign_support' in sys.argv, type=int)
parser_events.add_argument('--support_contact_username', required='assign_support' in sys.argv)

# arguments spécifiques à la commande 'update' pour le parser 'events'
parser_events.add_argument('--event_id_update', required='update' in sys.argv, type=int)
parser_events.add_argument('--new_event_name', required='update' in sys.argv)
parser_events.add_argument('--new_contract_id', required='update' in sys.argv, type=int)
parser_events.add_argument('--new_event_date_start', required='update' in sys.argv)
parser_events.add_argument('--new_event_date_end', required='update' in sys.argv)
parser_events.add_argument('--new_location', required='update' in sys.argv)
parser_events.add_argument('--new_attendees', required='update' in sys.argv, type=int)
parser_events.add_argument('--new_notes', required='update' in sys.argv)


# Création du parser pour la commande "login"
parser_login = subparsers.add_parser('login', help='login command help')
parser_login.add_argument('--username', required=True)


# Création du parser pour la commande "logout"
parser_logout = subparsers.add_parser('logout', help='logout command help')


args = parser.parse_args()

if 'login' in sys.argv:
    password = getpass.getpass("Enter your password :")
    login.authenticate(args.username, password)
elif 'logout' in sys.argv:
    disconnect.logout()
elif 'create_user' in sys.argv:
    # Pour récupérer le token
    token = keyring.get_password("epicevents", "jwt_token")
    if not token:
        sys.exit("Please login first.")
    # Pour récupérer le mot de passe de manière sécurisée
    password = getpass.getpass("Enter the new user's password:")
    # Appel de la fonction pour créer un nouvel utilisateur
    gestion.create_user(args.username, password, args.email, args.first_name, args.last_name, args.group, token)
elif 'update_user' in sys.argv:
    # Pour récupérer le token
    token = keyring.get_password("epicevents", "jwt_token")
    if not token:
        sys.exit("Please login first.")
    # Pour récupérer le mot de passe de manière sécurisée
    new_password = getpass.getpass("Enter the new password for the user:") if args.password else None
    # Appel de la fonction pour mettre à jour un utilisateur
    gestion.update_user(
        args.username,
        token, args.new_username,
        new_password,
        args.email,
        args.first_name,
        args.last_name,
        args.group
    )
elif 'delete_user' in sys.argv:
    # Pour récupérer le token
    token = keyring.get_password("epicevents", "jwt_token")
    if not token:
        sys.exit("Please login first.")
    # Appel de la fonction pour supprimer un utilisateur
    gestion.delete_user(args.username, token)
elif 'clients' in sys.argv:
    # Pour récupérer le token
    token = keyring.get_password("epicevents", "jwt_token")
    commercial_id = keyring.get_password("epicevents", "user_id")
    if not token or not commercial_id:
        sys.exit("Please login first.")
    if args.action == 'create':
        clients.create_client(args.full_name, args.email, args.phone, args.company_name, commercial_id, token)
    elif args.action == 'update':
        clients.update_client(args.full_name, args.email, args.phone, args.company_name, args.client_email, token)
    elif args.action == 'list':
        if args.filters is not None:
            filters = dict(filter.split('=') for filter in args.filters[0])
            clients.get_filtered_clients(token, filters)
        else:
            clients.get_filtered_clients(token)
elif 'contracts' in sys.argv:
    # Pour récupérer le token
    token = keyring.get_password("epicevents", "jwt_token")
    if not token:
        sys.exit("Please login first.")
    if args.action == 'create':
        if not all([args.client_email, args.total_amount, args.amount_due]):
            sys.exit("Please provide client email, total amount, and amount due for creating a contract.")
        contracts.create_contract(args.client_email, args.total_amount, args.amount_due, token)
    elif args.action == 'update':
        if not all([args.contract_id, args.client_email, args.total_amount, args.amount_due]):
            sys.exit("Please provide contract ID, client email, total amount, and amount due for updating a contract.")
        contracts.update_contract(args.contract_id, args.client_email, args.total_amount, args.amount_due, token)
    elif args.action == 'update_status':
        contracts.update_contract_status(args.contract_id, args.status, token)
    elif args.action == 'list':
        if args.filters is not None:
            filters = dict(filter.split('=') for filter in args.filters[0])
            contracts.get_filtered_contracts(token, filters)
        else:
            contracts.get_filtered_contracts(token)
elif 'events' in sys.argv:
    # Pour récupérer le token
    token = keyring.get_password("epicevents", "jwt_token")
    if not token:
        sys.exit("Please login first.")
    if args.action == 'create':
        events.create_event(
            args.event_name,
            args.contract_id,
            args.event_date_start,
            args.event_date_end,
            args.location,
            args.attendees,
            args.notes,
            token
        )
    elif args.action == 'update':
        events.update_event(args.event_id_update, args.new_event_name, args.new_contract_id, args.new_event_date_start,
                            args.new_event_date_end, args.new_location, args.new_attendees, args.new_notes, token)
    elif args.action == 'list':
        if args.filters is not None:
            filters = dict(filter.split('=') for filter in args.filters[0])
            events.get_filtered_events(token, filters)
        else:
            events.get_filtered_events(token)
    elif args.action == 'assign_support':
        events.assign_support_contact_to_event(args.event_id, args.support_contact_username, token)
    elif args.action == 'no_support_contact':
        events.get_events_no_support_contact(token)
