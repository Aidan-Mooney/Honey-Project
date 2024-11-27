import requests


def get_token(url, client_id, client_secret):
    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "client_id": client_id,
        "assertion": client_secret,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as err:
        raise err
