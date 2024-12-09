from datetime import datetime as dt


from src.get_token import get_token


def refresh_token(
    token_url: str,
    auth_id: str,
    auth_secret: str,
    start_time: str,
    time_till_expiry: int,
):
    if start_time + time_till_expiry <= dt.now().timestamp():
        token_response = get_token(token_url, auth_id, auth_secret)
        start_time = dt.now().timestamp()
        token = token_response["access_token"]
        time_till_expiry = token_response["expires_in"]
        return token, start_time, time_till_expiry
    else:
        return None
