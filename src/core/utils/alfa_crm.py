import requests

from core.settings import ALFA_CRM_EMAIL, ALFA_CRM_TOKEN, ALFA_CRM_URL


def get_token(email, token):
    response = requests.get(ALFA_CRM_URL)
    if response.status_code == 200:
        response.json()
        

def create_lead()