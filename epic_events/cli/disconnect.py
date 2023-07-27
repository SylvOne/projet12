import keyring


def logout():
    # Suppression du token du keyring
    keyring.delete_password("epicevents", "jwt_token")
    keyring.delete_password("epicevents", "user_id")
    print("You have been successfully logged out")
