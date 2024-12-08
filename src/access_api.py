import requests


def access_api(url, token):
    headers = {"Authorization": f"bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
