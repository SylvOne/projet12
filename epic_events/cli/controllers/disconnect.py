import keyring
from rich.console import Console


console = Console()


def logout():
    # Suppression du token du keyring
    keyring.delete_password("epicevents", "jwt_token")
    keyring.delete_password("epicevents", "user_id")
    console.print("Vous avez été déconnecté avec succès", style="bold green")
