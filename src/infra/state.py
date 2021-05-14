from data.owners import Owner
from services.db_services import find_account_by_email

active_account: Owner = None


def reload_account():
    global active_account
    if not active_account:
        return

    active_account = find_account_by_email(active_account.email)
