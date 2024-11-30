import requests


def access_api(url, token):
    headers = {"Authorization": f"bearer {token}"}
    response = requests.get(url, headers=headers)
    try:
        return response.status_code, response.json()
    except requests.exceptions.JSONDecodeError:
        return response.status_code, response.text
    return
