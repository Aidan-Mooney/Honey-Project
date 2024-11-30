import os
from dotenv import load_dotenv
from datetime import datetime as dt
import logging

from src.get_token import get_token
from src.access_api import access_api
from src.format_api_url import format_api_url
from src.extract_write import extract_write


def extract(**kwargs):
    load_dotenv(".env", override=True)
    start_time = dt.now().timestamp()
    time_till_expiry = 0
    try:
        token_url = os.environ["OAUTH_URL"]
        auth_id = os.environ["OAUTH_CLIENT_ID"]
        auth_secret = os.environ["OAUTH_CLIENT_SECRET"]
        base_endpoint = os.environ["ENDPOINT_URL"]
    except KeyError as err:
        logging.warning(f"Necessary environmental variables not found: {err}")
        return
    last_purchase_hash = None
    while True:
        if start_time + time_till_expiry <= dt.now().timestamp():
            token_code, token_body = get_token(token_url, auth_id, auth_secret)
            start_time = dt.now().timestamp()
            if token_code != 200:
                logging.warning(
                    f"HTTP code: {token_code}, body returned: {token_body} when calling get_token."
                )
                return
            token = token_body["access_token"]
            time_till_expiry = token_body["expires_in"]
        if not last_purchase_hash:
            api_query = format_api_url(base_endpoint, **kwargs)
        else:
            api_query = format_api_url(
                base_endpoint, lastPurchaseHash=last_purchase_hash, **kwargs
            )
        api_code, api_body = access_api(api_query, token)
        if api_code != 200:
            logging.warning(
                f": {api_code}, body returned: {api_body} when calling access_api."
            )
            return
        if api_body["purchases"]:
            lines_saved = extract_write(api_body["purchases"])
            logging.info(f"Saved {lines_saved}.")
        else:
            break
        last_purchase_hash = api_body["lastPurchaseHash"]
