import requests


def access_api(url: str, token: str):
    headers = {"Authorization": f"bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
