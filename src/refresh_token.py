from datetime import datetime as dt
import logging


from src.get_token import get_token


def refresh_token(token_url, auth_id, auth_secret, start_time, time_till_expiry):
    if start_time + time_till_expiry <= dt.now().timestamp():
        token_code, token_body = get_token(token_url, auth_id, auth_secret)
        start_time = dt.now().timestamp()
        if token_code != 200:
            logging.warning(
                f"HTTP code: {token_code}, body returned: {token_body} when calling get_token."
            )
            return "warning"
        token = token_body["access_token"]
        time_till_expiry = token_body["expires_in"]
        return token, start_time, time_till_expiry
    else:
        return None
