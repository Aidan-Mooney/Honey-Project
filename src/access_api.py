import requests


def access_api(url, token):
    headers = {"Authorization": f"bearer {token}"}
    response = requests.get(url, headers=headers)
    try:
        return {"code": response.status_code, "body": response.json()}
    except requests.exceptions.JSONDecodeError:
        return {"code": response.status_code, "body": response.text}
    return
