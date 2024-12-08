from src.format_api_url import format_api_url
from src.access_api import access_api
from src.extract_write import extract_write


def single_extract(
    token,
    base_endpoint,
    base_path,
    last_purchase_hash,
    last_date,
    limit=50,
    **kwargs,
):
    if last_purchase_hash:
        kwargs["lastPurchaseHash"] = last_purchase_hash
    if last_date:
        kwargs["startDate"] = last_date
    api_query = format_api_url(base_endpoint, limit, descending="true", **kwargs)
    api_json = access_api(api_query, token)
    if api_json["purchases"]:
        lines_saved = extract_write(base_path, api_json["purchases"])
        return lines_saved, api_json["lastPurchaseHash"]
    else:
        return None, None
