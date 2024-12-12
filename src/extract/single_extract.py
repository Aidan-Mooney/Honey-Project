from src.extract.format_api_url import format_api_url
from src.extract.access_api import access_api
from src.extract.extract_write import extract_write


def single_extract(
    token: str,
    base_endpoint: str,
    base_path: str,
    last_purchase_hash: str | None,
    last_date: str | None,
    limit: int = 50,
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
