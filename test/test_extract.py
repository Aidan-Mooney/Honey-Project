from unittest.mock import patch, Mock

from src.extract import extract


PATCH_PATH = "src.extract"


def test_successful_token_and_less_than_50_purchases_in_endpoint_works_correctly():
    timestamp_mock = Mock()
    timestamp_mock.timestamp.side_effect = [float(i) for i in range(4)]
    test_token_url = "test_url"
    test_id = "test_id"
    test_secret = "test_secret"
    test_endpoint = "test_endpoint"
    test_environ = {
        "OAUTH_URL": test_token_url,
        "OAUTH_CLIENT_ID": test_id,
        "OAUTH_CLIENT_SECRET": test_secret,
        "ENDPOINT_URL": test_endpoint,
    }
    test_token = "test_token"
    test_token_code = 200
    test_token_body = {"access_token": test_token, "expires_in": 7200}
    test_last_hash = "lastHash"
    test_purchases = [i for i in range(40)]
    test_api_code = 200
    test_api_body_1 = {
        "purchases": test_purchases,
        "firstPurchaseHash": "firstHash",
        "lastPurchaseHash": test_last_hash,
        "linkUrls": ["test_link_url"],
    }
    test_api_body_2 = {"purchases": [], "linkUrls": []}
    with patch(f"{PATCH_PATH}.os.environ", test_environ):
        with patch(f"{PATCH_PATH}.load_dotenv") as load_dotenv_mock:
            with patch(f"{PATCH_PATH}.dt") as now_mock:
                now_mock.now.return_value = timestamp_mock
                with patch(f"{PATCH_PATH}.logging") as logging_mock:
                    with patch(f"{PATCH_PATH}.get_token") as get_token_mock:
                        get_token_mock.return_value = test_token_code, test_token_body
                        with patch(f"{PATCH_PATH}.access_api") as access_api_mock:
                            access_api_mock.side_effect = [
                                (test_api_code, test_api_body_1),
                                (test_api_code, test_api_body_2),
                            ]
                            with patch(
                                f"{PATCH_PATH}.extract_write"
                            ) as extract_write_mock:
                                extract_write_mock.return_value = len(test_purchases)
                                extract()
    assert load_dotenv_mock.call_count == 1
    dotenv_args, dotenv_kwargs = load_dotenv_mock.call_args
    assert dotenv_args == (".env",)
    assert dotenv_kwargs == {"override": True}
    assert timestamp_mock.timestamp.call_count == 4
    assert logging_mock.info.call_count == 1
    logging_args, logging_kwargs = logging_mock.info.call_args
    assert logging_args == (f"Saved {len(test_purchases)}.",)
    assert logging_kwargs == {}
    assert get_token_mock.call_count == 1
    get_token_args, get_token_kwargs = get_token_mock.call_args
    assert get_token_args == (test_token_url, test_id, test_secret)
    assert get_token_kwargs == {}
    assert access_api_mock.call_count == 2
    access_api_args_1, access_api_kwargs_1 = access_api_mock.call_args_list[0]
    access_api_args_2, access_api_kwargs_2 = access_api_mock.call_args_list[1]
    assert access_api_args_1 == (f"{test_endpoint}?limit=50", test_token)
    assert access_api_args_2 == (
        f"{test_endpoint}?limit=50&lastPurchaseHash={test_last_hash}",
        test_token,
    )
    assert access_api_kwargs_1 == {}
    assert access_api_kwargs_2 == {}
    assert extract_write_mock.call_count == 1
    extract_write_args, extract_write_kwargs = extract_write_mock.call_args
    assert extract_write_args == (test_purchases, False)
    assert extract_write_kwargs == {}


def test_successful_token_and_more_than_50_purchases_in_endpoint_works_correctly():
    timestamp_mock = Mock()
    timestamp_mock.timestamp.side_effect = [float(i) for i in range(5)]
    test_token_url = "test_url"
    test_id = "test_id"
    test_secret = "test_secret"
    test_endpoint = "test_endpoint"
    test_environ = {
        "OAUTH_URL": test_token_url,
        "OAUTH_CLIENT_ID": test_id,
        "OAUTH_CLIENT_SECRET": test_secret,
        "ENDPOINT_URL": test_endpoint,
    }
    test_token = "test_token"
    test_token_code = 200
    test_token_body = {"access_token": test_token, "expires_in": 7200}
    test_last_hash_1 = "lastHash1"
    test_last_hash_2 = "lastHash2"
    test_purchases_1 = [i for i in range(50)]
    test_purchases_2 = [i for i in range(25)]
    test_api_code = 200
    test_api_body_1 = {
        "purchases": test_purchases_1,
        "firstPurchaseHash": "firstHash",
        "lastPurchaseHash": test_last_hash_1,
        "linkUrls": ["test_link_url"],
    }
    test_api_body_2 = {
        "purchases": test_purchases_2,
        "firstPurchaseHash": test_last_hash_1,
        "lastPurchaseHash": test_last_hash_2,
        "linkUrls": ["test_link_url"],
    }
    test_api_body_3 = {"purchases": [], "linkUrls": []}
    with patch(f"{PATCH_PATH}.os.environ", test_environ):
        with patch(f"{PATCH_PATH}.load_dotenv") as load_dotenv_mock:
            with patch(f"{PATCH_PATH}.dt") as now_mock:
                now_mock.now.return_value = timestamp_mock
                with patch(f"{PATCH_PATH}.logging") as logging_mock:
                    with patch(f"{PATCH_PATH}.get_token") as get_token_mock:
                        get_token_mock.return_value = test_token_code, test_token_body
                        with patch(f"{PATCH_PATH}.access_api") as access_api_mock:
                            access_api_mock.side_effect = [
                                (test_api_code, test_api_body_1),
                                (test_api_code, test_api_body_2),
                                (test_api_code, test_api_body_3),
                            ]
                            with patch(
                                f"{PATCH_PATH}.extract_write"
                            ) as extract_write_mock:
                                extract_write_mock.side_effect = [
                                    len(test_purchases_1),
                                    len(test_purchases_2),
                                ]
                                extract()
    assert load_dotenv_mock.call_count == 1
    dotenv_args, dotenv_kwargs = load_dotenv_mock.call_args
    assert dotenv_args == (".env",)
    assert dotenv_kwargs == {"override": True}
    assert timestamp_mock.timestamp.call_count == 5
    assert logging_mock.info.call_count == 2
    logging_args_1, logging_kwargs_1 = logging_mock.info.call_args_list[0]
    logging_args_2, logging_kwargs_2 = logging_mock.info.call_args_list[1]
    assert logging_args_1 == (f"Saved {len(test_purchases_1)}.",)
    assert logging_args_2 == (f"Saved {len(test_purchases_2)}.",)
    assert logging_kwargs_1 == {}
    assert logging_kwargs_2 == {}
    assert get_token_mock.call_count == 1
    get_token_args, get_token_kwargs = get_token_mock.call_args
    assert get_token_args == (test_token_url, test_id, test_secret)
    assert get_token_kwargs == {}
    assert access_api_mock.call_count == 3
    access_api_args_1, access_api_kwargs_1 = access_api_mock.call_args_list[0]
    access_api_args_2, access_api_kwargs_2 = access_api_mock.call_args_list[1]
    access_api_args_3, access_api_kwargs_3 = access_api_mock.call_args_list[2]
    assert access_api_args_1 == (f"{test_endpoint}?limit=50", test_token)
    assert access_api_args_2 == (
        f"{test_endpoint}?limit=50&lastPurchaseHash={test_last_hash_1}",
        test_token,
    )
    assert access_api_args_3 == (
        f"{test_endpoint}?limit=50&lastPurchaseHash={test_last_hash_2}",
        test_token,
    )
    assert access_api_kwargs_1 == {}
    assert access_api_kwargs_2 == {}
    assert access_api_kwargs_3 == {}
    assert extract_write_mock.call_count == 2
    extract_write_args_1, extract_write_kwargs_1 = extract_write_mock.call_args_list[0]
    extract_write_args_2, extract_write_kwargs_2 = extract_write_mock.call_args_list[1]
    assert extract_write_args_1 == (test_purchases_1, False)
    assert extract_write_args_2 == (test_purchases_2, False)
    assert extract_write_kwargs_1 == {}
    assert extract_write_kwargs_2 == {}


def test_unconfigured_env_file_is_logged():
    test_environ = {}
    error_message = "'OAUTH_URL'"
    with patch(f"{PATCH_PATH}.os.environ", test_environ):
        with patch(f"{PATCH_PATH}.load_dotenv") as load_dotenv_mock:
            with patch(f"{PATCH_PATH}.dt") as now_mock:
                with patch(f"{PATCH_PATH}.logging") as logging_mock:
                    with patch(f"{PATCH_PATH}.get_token") as get_token_mock:
                        with patch(f"{PATCH_PATH}.access_api") as access_api_mock:
                            with patch(
                                f"{PATCH_PATH}.extract_write"
                            ) as extract_write_mock:
                                extract()
    assert load_dotenv_mock.call_count == 1
    dotenv_args, dotenv_kwargs = load_dotenv_mock.call_args
    assert dotenv_args == (".env",)
    assert dotenv_kwargs == {"override": True}
    assert now_mock.call_count == 0
    assert logging_mock.warning.call_count == 1
    logging_args, logging_kwargs = logging_mock.warning.call_args
    assert logging_args == (
        f"Necessary environmental variables not found: {error_message}",
    )
    assert logging_kwargs == {}
    assert get_token_mock.call_count == 0
    assert access_api_mock.call_count == 0
    assert extract_write_mock.call_count == 0


def test_unsuccessful_token_call_raises_warning_log_and_ends_the_function():
    timestamp_mock = Mock()
    timestamp_mock.timestamp.side_effect = [float(i) for i in range(3)]
    test_token_url = "test_url"
    test_id = "test_id"
    test_secret = "test_secret"
    test_endpoint = "test_endpoint"
    test_environ = {
        "OAUTH_URL": test_token_url,
        "OAUTH_CLIENT_ID": test_id,
        "OAUTH_CLIENT_SECRET": test_secret,
        "ENDPOINT_URL": test_endpoint,
    }
    test_token_code = 404
    test_token_body = {"code": 404, "message": "HTTP 404 Not Found"}
    with patch(f"{PATCH_PATH}.os.environ", test_environ):
        with patch(f"{PATCH_PATH}.load_dotenv") as load_dotenv_mock:
            with patch(f"{PATCH_PATH}.dt") as now_mock:
                now_mock.now.return_value = timestamp_mock
                with patch(f"{PATCH_PATH}.logging") as logging_mock:
                    with patch(f"{PATCH_PATH}.get_token") as get_token_mock:
                        get_token_mock.return_value = test_token_code, test_token_body
                        with patch(f"{PATCH_PATH}.access_api") as access_api_mock:
                            with patch(
                                f"{PATCH_PATH}.extract_write"
                            ) as extract_write_mock:
                                extract()
    assert load_dotenv_mock.call_count == 1
    dotenv_args, dotenv_kwargs = load_dotenv_mock.call_args
    assert dotenv_args == (".env",)
    assert dotenv_kwargs == {"override": True}
    assert timestamp_mock.timestamp.call_count == 3
    assert logging_mock.warning.call_count == 1
    logging_args, logging_kwargs = logging_mock.warning.call_args
    assert logging_args == (
        f"HTTP code: {test_token_code}, body returned: {test_token_body} when calling get_token.",
    )
    assert logging_kwargs == {}
    assert get_token_mock.call_count == 1
    get_token_args, get_token_kwargs = get_token_mock.call_args
    assert get_token_args == (test_token_url, test_id, test_secret)
    assert get_token_kwargs == {}
    assert access_api_mock.call_count == 0
    assert extract_write_mock.call_count == 0


def test_successful_token_and_unsuccessful_api_call():
    timestamp_mock = Mock()
    timestamp_mock.timestamp.side_effect = [float(i) for i in range(3)]
    test_token_url = "test_url"
    test_id = "test_id"
    test_secret = "test_secret"
    test_endpoint = "test_endpoint"
    test_environ = {
        "OAUTH_URL": test_token_url,
        "OAUTH_CLIENT_ID": test_id,
        "OAUTH_CLIENT_SECRET": test_secret,
        "ENDPOINT_URL": test_endpoint,
    }
    test_token = "test_token"
    test_token_code = 200
    test_token_body = {"access_token": test_token, "expires_in": 7200}
    test_api_code = 404
    test_api_body = {"code": 404, "message": "HTTP 404 Not Found"}
    with patch(f"{PATCH_PATH}.os.environ", test_environ):
        with patch(f"{PATCH_PATH}.load_dotenv") as load_dotenv_mock:
            with patch(f"{PATCH_PATH}.dt") as now_mock:
                now_mock.now.return_value = timestamp_mock
                with patch(f"{PATCH_PATH}.logging") as logging_mock:
                    with patch(f"{PATCH_PATH}.get_token") as get_token_mock:
                        get_token_mock.return_value = test_token_code, test_token_body
                        with patch(f"{PATCH_PATH}.access_api") as access_api_mock:
                            access_api_mock.return_value = test_api_code, test_api_body
                            with patch(
                                f"{PATCH_PATH}.extract_write"
                            ) as extract_write_mock:
                                extract()
    assert load_dotenv_mock.call_count == 1
    dotenv_args, dotenv_kwargs = load_dotenv_mock.call_args
    assert dotenv_args == (".env",)
    assert dotenv_kwargs == {"override": True}
    assert timestamp_mock.timestamp.call_count == 3
    assert logging_mock.warning.call_count == 1
    logging_args, logging_kwargs = logging_mock.warning.call_args
    assert logging_args == (
        f": {test_api_code}, body returned: {test_api_body} when calling access_api.",
    )
    assert logging_kwargs == {}
    assert get_token_mock.call_count == 1
    get_token_args, get_token_kwargs = get_token_mock.call_args
    assert get_token_args == (test_token_url, test_id, test_secret)
    assert get_token_kwargs == {}
    assert access_api_mock.call_count == 1
    access_api_args_1, access_api_kwargs_1 = access_api_mock.call_args
    assert access_api_args_1 == (f"{test_endpoint}?limit=50", test_token)
    assert access_api_kwargs_1 == {}
    assert extract_write_mock.call_count == 0


def test_when_rewrite_is_true_reset_extracts_data_is_ran():
    timestamp_mock = Mock()
    timestamp_mock.timestamp.side_effect = [float(i) for i in range(4)]
    test_token_url = "test_url"
    test_id = "test_id"
    test_secret = "test_secret"
    test_endpoint = "test_endpoint"
    test_environ = {
        "OAUTH_URL": test_token_url,
        "OAUTH_CLIENT_ID": test_id,
        "OAUTH_CLIENT_SECRET": test_secret,
        "ENDPOINT_URL": test_endpoint,
    }
    test_token = "test_token"
    test_token_code = 200
    test_token_body = {"access_token": test_token, "expires_in": 7200}
    test_last_hash = "lastHash"
    test_purchases = [i for i in range(40)]
    test_api_code = 200
    test_api_body_1 = {
        "purchases": test_purchases,
        "firstPurchaseHash": "firstHash",
        "lastPurchaseHash": test_last_hash,
        "linkUrls": ["test_link_url"],
    }
    test_api_body_2 = {"purchases": [], "linkUrls": []}
    with patch(f"{PATCH_PATH}.os.environ", test_environ):
        with patch(f"{PATCH_PATH}.load_dotenv"):
            with patch(f"{PATCH_PATH}.dt") as now_mock:
                now_mock.now.return_value = timestamp_mock
                with patch(f"{PATCH_PATH}.logging"):
                    with patch(f"{PATCH_PATH}.reset_extracts_data") as reset_mock:
                        with patch(f"{PATCH_PATH}.get_token") as get_token_mock:
                            get_token_mock.return_value = (
                                test_token_code,
                                test_token_body,
                            )
                            with patch(f"{PATCH_PATH}.access_api") as access_api_mock:
                                access_api_mock.side_effect = [
                                    (test_api_code, test_api_body_1),
                                    (test_api_code, test_api_body_2),
                                ]
                                with patch(
                                    f"{PATCH_PATH}.extract_write"
                                ) as extract_write_mock:
                                    extract_write_mock.return_value = len(
                                        test_purchases
                                    )
                                    extract(rewrite=True)
    assert reset_mock.call_count == 1
