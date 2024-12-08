from unittest.mock import patch


from src.single_extract import single_extract


PATCH_PATH = "src.single_extract"


def test_empty_json_api_response_returns_none():
    test_token = "token"
    test_base_endpoint = "https://endpoint.com/api"
    test_base_path = "data/place"
    test_last_purchase_hash = None
    test_last_date = None
    with patch(f"{PATCH_PATH}.access_api") as access_mock:
        access_mock.return_value = {"purchases": [], "linkUrls": []}
        with patch(f"{PATCH_PATH}.extract_write") as write_mock:
            result_lines, result_hash = single_extract(
                test_token,
                test_base_endpoint,
                test_base_path,
                test_last_purchase_hash,
                test_last_date,
            )
    assert result_lines is None
    assert result_hash is None
    assert write_mock.call_count == 0


def test_when_purchases_are_returned_they_are_passed_into_extract_write():
    test_token = "token"
    test_base_endpoint = "https://endpoint.com/api"
    test_base_path = "data/place"
    test_last_purchase_hash = None
    test_last_date = None
    return_last_purchase_hash = "hash brown"
    purchase_json = [i for i in range(50)]
    with patch(f"{PATCH_PATH}.access_api") as access_mock:
        access_mock.return_value = {
            "purchases": purchase_json,
            "firstPurchaseHash": "first has brown",
            "lastPurchaseHash": return_last_purchase_hash,
            "linkUrls": [],
        }
        with patch(f"{PATCH_PATH}.extract_write") as write_mock:
            write_mock.return_value = 50
            result_lines, result_hash = single_extract(
                test_token,
                test_base_endpoint,
                test_base_path,
                test_last_purchase_hash,
                test_last_date,
            )
    assert result_lines == 50
    assert result_hash == return_last_purchase_hash
    assert write_mock.call_count == 1


def test_last_purchase_hash_is_passed_into_format_api_url_when_not_none():
    test_token = "token"
    test_base_endpoint = "https://endpoint.com/api"
    test_base_path = "data/place"
    test_last_purchase_hash = "the last hash brown"
    test_last_date = None
    return_last_purchase_hash = "hash brown"
    purchase_json = [i for i in range(50)]
    with patch(f"{PATCH_PATH}.format_api_url") as format_mock:
        format_mock.return_value = "passed in url"
        with patch(f"{PATCH_PATH}.access_api") as access_mock:
            access_mock.return_value = {
                "purchases": purchase_json,
                "firstPurchaseHash": "first has brown",
                "lastPurchaseHash": return_last_purchase_hash,
                "linkUrls": [],
            }
            with patch(f"{PATCH_PATH}.extract_write") as write_mock:
                write_mock.return_value = 50
                result_lines, result_hash = single_extract(
                    test_token,
                    test_base_endpoint,
                    test_base_path,
                    test_last_purchase_hash,
                    test_last_date,
                )
    assert result_lines == 50
    assert result_hash == return_last_purchase_hash
    assert write_mock.call_count == 1
    format_args, format_kwargs = format_mock.call_args
    assert format_args == (test_base_endpoint, 50)
    assert format_kwargs == {
        "descending": "true",
        "lastPurchaseHash": test_last_purchase_hash,
    }


def test_last_date_is_passed_into_format_api_url_when_not_none():
    test_token = "token"
    test_base_endpoint = "https://endpoint.com/api"
    test_base_path = "data/place"
    test_last_purchase_hash = None
    test_last_date = "2021-01-13T12:30"
    return_last_purchase_hash = "hash brown"
    purchase_json = [i for i in range(50)]
    with patch(f"{PATCH_PATH}.format_api_url") as format_mock:
        format_mock.return_value = "passed in url"
        with patch(f"{PATCH_PATH}.access_api") as access_mock:
            access_mock.return_value = {
                "purchases": purchase_json,
                "firstPurchaseHash": "first has brown",
                "lastPurchaseHash": return_last_purchase_hash,
                "linkUrls": [],
            }
            with patch(f"{PATCH_PATH}.extract_write") as write_mock:
                write_mock.return_value = 50
                result_lines, result_hash = single_extract(
                    test_token,
                    test_base_endpoint,
                    test_base_path,
                    test_last_purchase_hash,
                    test_last_date,
                )
    assert result_lines == 50
    assert result_hash == return_last_purchase_hash
    assert write_mock.call_count == 1
    format_args, format_kwargs = format_mock.call_args
    assert format_args == (test_base_endpoint, 50)
    assert format_kwargs == {
        "descending": "true",
        "startDate": test_last_date,
    }
