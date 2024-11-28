import requests


def get_token(url: str, client_id: str, client_secret: str):
    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "client_id": client_id,
        "assertion": client_secret,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=data, headers=headers)
    return {"code": response.status_code, "body": response.json()}
