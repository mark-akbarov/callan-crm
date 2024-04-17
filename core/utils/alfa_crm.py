import requests

from core.settings import ALFA_CRM_EMAIL, ALFA_CRM_TOKEN, ALFA_CRM_URL


red = "#ea394c"
orange = "#ffcd70"
yellow = "#ffff00"
green = "#00aa00"
light_blue = "#9acfea"
blue = "#1a7bb9"
violet = "#3C578C"


def get_token(email, api_token):
    url = ALFA_CRM_URL + "auth/login"
    response = requests.post(url, json={"email": email, "api_key": api_token})
    if response.status_code == 200:
        return response.json()
    else:
        return response.json()


def create_lead(name, phone, note, branch_ids=1, legal_type=1, color=blue, is_study=0):
    token = get_token(email=ALFA_CRM_EMAIL, api_token=ALFA_CRM_TOKEN)
    token = token['token']
    url = ALFA_CRM_URL + "1/customer/create"
    res = requests.post(
        url, 
        json={
            "name": name, 
            "legal_type": legal_type, 
            "is_study": is_study, 
            "branch_ids": branch_ids,
            "color": color,
            "phone": phone,
            "note": note
            }, 
        headers={"X-ALFACRM-TOKEN": token}
        )
    if res.status_code == 200:
        print("success")
    else:
        return res.content
