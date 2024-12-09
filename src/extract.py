import os
from pathlib import Path
import shutil
from requests.exceptions import HTTPError
from dotenv import load_dotenv
from datetime import datetime as dt
import logging


from src.refresh_token import refresh_token
from src.get_last_date import get_last_date
from src.single_extract import single_extract


def extract(limit=50, **kwargs):
    try:
        load_dotenv(".env", override=True)
        try:
            token_url = os.environ["OAUTH_URL"]
            auth_id = os.environ["OAUTH_CLIENT_ID"]
            auth_secret = os.environ["OAUTH_CLIENT_SECRET"]
            base_endpoint = os.environ["ENDPOINT_URL"]
        except KeyError as err:
            logging.warning(f"Necessary environmental variables not found: {err}")
            return "failure"
        start_time = dt.now().timestamp()
        time_till_expiry = 0
        last_purchase_hash = None
        last_date = get_last_date()
        timestamp = dt.now().strftime("%Y-%m-%d-%H-%M-%S")
        base_path = f"data/extract/{timestamp}"
        Path(base_path).mkdir(parents=True, exist_ok=True)
        while True:
            try:
                response = refresh_token(
                    token_url, auth_id, auth_secret, start_time, time_till_expiry
                )
            except HTTPError as err:
                logging.warning(f"{type(err).__name__}: {err}")
                shutil.rmtree(base_path, ignore_errors=False)
                return "failure"
            try:
                if response:
                    token, start_time, time_till_expiry = response
                lines_saved, last_purchase_hash = single_extract(
                    token,
                    base_endpoint,
                    base_path,
                    limit,
                    last_purchase_hash,
                    last_date,
                    **kwargs,
                )
            except (HTTPError, KeyError) as err:
                logging.warning(f"{type(err).__name__}: {err}")
                shutil.rmtree(base_path, ignore_errors=False)
                return "failure"
            if lines_saved:
                logging.info(f"Saved {lines_saved} lines.")
            else:
                return "success"
    except Exception as err:
        logging.critical(f"{type(err).__name__}: {err}")
        return "failure"
