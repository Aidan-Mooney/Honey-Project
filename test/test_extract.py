from unittest.mock import patch
from requests.exceptions import HTTPError


from src.extract import extract


PATCH_PATH = "src.extract"


@patch(f"{PATCH_PATH}.single_extract")
@patch(f"{PATCH_PATH}.shutil.rmtree")
@patch(f"{PATCH_PATH}.logging")
@patch(f"{PATCH_PATH}.refresh_token")
@patch(f"{PATCH_PATH}.Path")
@patch(f"{PATCH_PATH}.get_last_date")
@patch(f"{PATCH_PATH}.dt")
@patch(f"{PATCH_PATH}.os")
@patch(f"{PATCH_PATH}.load_dotenv")
def test_successful_token_and_less_than_50_purchases_in_endpoint_works_correctly(
    _,
    os_mock,
    now_mock,
    __,
    path_mock,
    token_mock,
    log_mock,
    shutil_mock,
    single_extract_mock,
):
    test_url = "OAUTH_URL"
    test_id = "OAUTH_CLIENT_ID"
    test_secret = "OAUTH_CLIENT_SECRET"
    test_endpoint = "ENDPOINT_URL"
    os_mock.environ = {
        "OAUTH_URL": test_url,
        "OAUTH_CLIENT_ID": test_id,
        "OAUTH_CLIENT_SECRET": test_secret,
        "ENDPOINT_URL": test_endpoint,
    }
    now_mock.now.return_value.timestamp.return_value = 0
    now_mock.now.return_value.strftime.return_value = "2021-01-13T12:30"
    token_mock.side_effect = [("token", 1, 7200), None]
    single_extract_mock.side_effect = [(40, "hash brown"), (None, None)]
    result = extract()
    assert result == "success"
    assert path_mock.call_count == 1
    assert shutil_mock.call_count == 0
    assert log_mock.info.call_count == 1
    log_args, log_kwargs = log_mock.info.call_args
    assert log_args == ("Saved 40 lines.",)
    assert log_kwargs == {}


@patch(f"{PATCH_PATH}.single_extract")
@patch(f"{PATCH_PATH}.shutil.rmtree")
@patch(f"{PATCH_PATH}.logging")
@patch(f"{PATCH_PATH}.refresh_token")
@patch(f"{PATCH_PATH}.Path")
@patch(f"{PATCH_PATH}.get_last_date")
@patch(f"{PATCH_PATH}.dt")
@patch(f"{PATCH_PATH}.os")
@patch(f"{PATCH_PATH}.load_dotenv")
def test_successful_token_and_more_than_50_purchases_in_endpoint_works_correctly(
    _,
    os_mock,
    now_mock,
    last_date_mock,
    path_mock,
    token_mock,
    log_mock,
    shutil_mock,
    single_extract_mock,
):
    test_url = "OAUTH_URL"
    test_id = "OAUTH_CLIENT_ID"
    test_secret = "OAUTH_CLIENT_SECRET"
    test_endpoint = "ENDPOINT_URL"
    os_mock.environ = {
        "OAUTH_URL": test_url,
        "OAUTH_CLIENT_ID": test_id,
        "OAUTH_CLIENT_SECRET": test_secret,
        "ENDPOINT_URL": test_endpoint,
    }
    last_date_mock.return_value = None
    test_timestamp = "2021-01-13T12:30"
    now_mock.now.return_value.timestamp.return_value = 0
    now_mock.now.return_value.strftime.return_value = test_timestamp
    token_mock.side_effect = [("token", 1, 7200), None, None]
    single_extract_mock.side_effect = [
        (50, "hash brown"),
        (20, "double hash brown"),
        (None, None),
    ]
    result = extract()
    assert result == "success"
    sin_ex_args1, sin_ex_kwargs1 = single_extract_mock.call_args_list[0]
    sin_ex_args2, sin_ex_kwargs2 = single_extract_mock.call_args_list[1]
    sin_ex_args3, sin_ex_kwargs3 = single_extract_mock.call_args_list[2]
    assert sin_ex_args1 == (
        "token",
        test_endpoint,
        f"data/extract/{test_timestamp}",
        None,
        None,
        50,
    )
    assert sin_ex_kwargs1 == {}
    assert sin_ex_args2 == (
        "token",
        test_endpoint,
        f"data/extract/{test_timestamp}",
        "hash brown",
        None,
        50,
    )
    assert sin_ex_kwargs2 == {}
    assert sin_ex_args3 == (
        "token",
        test_endpoint,
        f"data/extract/{test_timestamp}",
        "double hash brown",
        None,
        50,
    )
    assert sin_ex_kwargs3 == {}
    assert path_mock.call_count == 1
    assert shutil_mock.call_count == 0
    assert log_mock.info.call_count == 2
    log_args1, log_kwargs1 = log_mock.info.call_args_list[0]
    log_args2, log_kwargs2 = log_mock.info.call_args_list[1]
    assert log_args1 == ("Saved 50 lines.",)
    assert log_kwargs1 == {}
    assert log_args2 == ("Saved 20 lines.",)
    assert log_kwargs2 == {}


@patch(f"{PATCH_PATH}.traceback")
@patch(f"{PATCH_PATH}.logging")
@patch(f"{PATCH_PATH}.os")
@patch(f"{PATCH_PATH}.load_dotenv")
def test_unconfigured_env_file_is_logged(_, os_mock, log_mock, traceback_mock):
    traceback_mock.format_exc.return_value = "traceback stuff"
    os_mock.environ = {}
    result = extract()
    assert result == "failure"
    log_args1, log_kwargs1 = log_mock.warning.call_args_list[0]
    assert log_args1 == ("Necessary environmental variables not found: 'OAUTH_URL'",)
    assert log_kwargs1 == {}
    log_args2, log_kwargs2 = log_mock.warning.call_args_list[1]
    assert log_args2 == ("Traceback details:\ntraceback stuff",)
    assert log_kwargs2 == {}


@patch(f"{PATCH_PATH}.traceback")
@patch(f"{PATCH_PATH}.shutil.rmtree")
@patch(f"{PATCH_PATH}.logging")
@patch(f"{PATCH_PATH}.refresh_token")
@patch(f"{PATCH_PATH}.Path")
@patch(f"{PATCH_PATH}.get_last_date")
@patch(f"{PATCH_PATH}.dt")
@patch(f"{PATCH_PATH}.os")
@patch(f"{PATCH_PATH}.load_dotenv")
def test_unsuccessful_token_call_raises_warning_log(
    _,
    os_mock,
    now_mock,
    __,
    path_mock,
    token_mock,
    log_mock,
    shutil_mock,
    traceback_mock,
):
    traceback_mock.format_exc.return_value = "traceback stuff"
    test_url = "OAUTH_URL"
    test_id = "OAUTH_CLIENT_ID"
    test_secret = "OAUTH_CLIENT_SECRET"
    test_endpoint = "ENDPOINT_URL"
    os_mock.environ = {
        "OAUTH_URL": test_url,
        "OAUTH_CLIENT_ID": test_id,
        "OAUTH_CLIENT_SECRET": test_secret,
        "ENDPOINT_URL": test_endpoint,
    }
    now_mock.now.return_value.timestamp.return_value = 0
    now_mock.now.return_value.strftime.return_value = "2021-01-13T12:30"
    token_mock.side_effect = HTTPError("HTTP 404 Not Found")
    result = extract()
    assert result == "failure"
    log_args1, log_kwargs1 = log_mock.warning.call_args_list[0]
    assert log_args1 == ("HTTPError: HTTP 404 Not Found",)
    assert log_kwargs1 == {}
    log_args2, log_kwargs2 = log_mock.warning.call_args_list[1]
    assert log_args2 == ("Traceback details:\ntraceback stuff",)
    assert log_kwargs2 == {}
    assert path_mock.call_count == 1
    assert shutil_mock.call_count == 1


@patch(f"{PATCH_PATH}.traceback")
@patch(f"{PATCH_PATH}.single_extract")
@patch(f"{PATCH_PATH}.shutil.rmtree")
@patch(f"{PATCH_PATH}.logging")
@patch(f"{PATCH_PATH}.refresh_token")
@patch(f"{PATCH_PATH}.Path")
@patch(f"{PATCH_PATH}.get_last_date")
@patch(f"{PATCH_PATH}.dt")
@patch(f"{PATCH_PATH}.os")
@patch(f"{PATCH_PATH}.load_dotenv")
def test_successful_token_and_unsuccessful_api_call(
    _,
    os_mock,
    now_mock,
    __,
    path_mock,
    token_mock,
    log_mock,
    shutil_mock,
    single_extract_mock,
    traceback_mock,
):
    traceback_mock.format_exc.return_value = "traceback stuff"
    test_url = "OAUTH_URL"
    test_id = "OAUTH_CLIENT_ID"
    test_secret = "OAUTH_CLIENT_SECRET"
    test_endpoint = "ENDPOINT_URL"
    os_mock.environ = {
        "OAUTH_URL": test_url,
        "OAUTH_CLIENT_ID": test_id,
        "OAUTH_CLIENT_SECRET": test_secret,
        "ENDPOINT_URL": test_endpoint,
    }
    now_mock.now.return_value.timestamp.return_value = 0
    now_mock.now.return_value.strftime.return_value = "2021-01-13T12:30"
    token_mock.return_value = "token", 1, 7200
    single_extract_mock.side_effect = HTTPError("HTTP 404 Not Found")
    result = extract()
    assert result == "failure"
    log_args1, log_kwargs1 = log_mock.warning.call_args_list[0]
    assert log_args1 == ("HTTPError: HTTP 404 Not Found",)
    assert log_kwargs1 == {}
    log_args2, log_kwargs2 = log_mock.warning.call_args_list[1]
    assert log_args2 == ("Traceback details:\ntraceback stuff",)
    assert log_kwargs2 == {}
    assert path_mock.call_count == 1
    assert shutil_mock.call_count == 1


@patch(f"{PATCH_PATH}.traceback")
@patch(f"{PATCH_PATH}.single_extract")
@patch(f"{PATCH_PATH}.shutil.rmtree")
@patch(f"{PATCH_PATH}.logging")
@patch(f"{PATCH_PATH}.refresh_token")
@patch(f"{PATCH_PATH}.Path")
@patch(f"{PATCH_PATH}.get_last_date")
@patch(f"{PATCH_PATH}.dt")
@patch(f"{PATCH_PATH}.os")
@patch(f"{PATCH_PATH}.load_dotenv")
def test_successful_api_call_with_key_error(
    _,
    os_mock,
    now_mock,
    __,
    path_mock,
    token_mock,
    log_mock,
    shutil_mock,
    single_extract_mock,
    traceback_mock,
):
    traceback_mock.format_exc.return_value = "traceback stuff"
    test_url = "OAUTH_URL"
    test_id = "OAUTH_CLIENT_ID"
    test_secret = "OAUTH_CLIENT_SECRET"
    test_endpoint = "ENDPOINT_URL"
    os_mock.environ = {
        "OAUTH_URL": test_url,
        "OAUTH_CLIENT_ID": test_id,
        "OAUTH_CLIENT_SECRET": test_secret,
        "ENDPOINT_URL": test_endpoint,
    }
    now_mock.now.return_value.timestamp.return_value = 0
    now_mock.now.return_value.strftime.return_value = "2021-01-13T12:30"
    token_mock.return_value = "token", 1, 7200
    single_extract_mock.side_effect = KeyError("name")
    result = extract()
    assert result == "failure"
    log_args1, log_kwargs1 = log_mock.warning.call_args_list[0]
    assert log_args1 == ("KeyError: 'name'",)
    assert log_kwargs1 == {}
    log_args2, log_kwargs2 = log_mock.warning.call_args_list[1]
    assert log_args2 == ("Traceback details:\ntraceback stuff",)
    assert log_kwargs2 == {}
    assert path_mock.call_count == 1
    assert shutil_mock.call_count == 1


@patch(f"{PATCH_PATH}.traceback")
@patch(f"{PATCH_PATH}.shutil.rmtree")
@patch(f"{PATCH_PATH}.logging")
@patch(f"{PATCH_PATH}.load_dotenv")
def test_critical_log_for_unaccounted_error_before_path(
    load_env_mock, log_mock, shutil_mock, traceback_mock
):
    traceback_mock.format_exc.return_value = "traceback stuff"
    load_env_mock.side_effect = Exception("Uh oh load_env is broken for NO REASON")
    result = extract()
    assert result == "failure"
    assert log_mock.critical.call_count == 2
    log_args1, log_kwargs1 = log_mock.critical.call_args_list[0]
    log_args2, log_kwargs2 = log_mock.critical.call_args_list[1]
    assert log_args1 == ("Exception: Uh oh load_env is broken for NO REASON",)
    assert log_kwargs1 == {}
    assert log_args2 == ("Traceback details:\ntraceback stuff",)
    assert log_kwargs2 == {}
    assert shutil_mock.call_count == 0


@patch(f"{PATCH_PATH}.traceback")
@patch(f"{PATCH_PATH}.shutil.rmtree")
@patch(f"{PATCH_PATH}.logging")
@patch(f"{PATCH_PATH}.refresh_token")
@patch(f"{PATCH_PATH}.Path")
@patch(f"{PATCH_PATH}.get_last_date")
@patch(f"{PATCH_PATH}.dt")
@patch(f"{PATCH_PATH}.os")
@patch(f"{PATCH_PATH}.load_dotenv")
def test_critical_log_for_unaccounted_error_after_path(
    _,
    os_mock,
    now_mock,
    __,
    path_mock,
    token_mock,
    log_mock,
    shutil_mock,
    traceback_mock,
):
    traceback_mock.format_exc.return_value = "traceback stuff"
    test_url = "OAUTH_URL"
    test_id = "OAUTH_CLIENT_ID"
    test_secret = "OAUTH_CLIENT_SECRET"
    test_endpoint = "ENDPOINT_URL"
    os_mock.environ = {
        "OAUTH_URL": test_url,
        "OAUTH_CLIENT_ID": test_id,
        "OAUTH_CLIENT_SECRET": test_secret,
        "ENDPOINT_URL": test_endpoint,
    }
    now_mock.now.return_value.timestamp.return_value = 0
    now_mock.now.return_value.strftime.return_value = "2021-01-13T12:30"
    token_mock.side_effect = NameError("How can this be a name error")
    result = extract()
    assert result == "failure"
    assert log_mock.critical.call_count == 2
    log_args1, log_kwargs1 = log_mock.critical.call_args_list[0]
    log_args2, log_kwargs2 = log_mock.critical.call_args_list[1]
    assert log_args1 == ("NameError: How can this be a name error",)
    assert log_kwargs1 == {}
    assert log_args2 == ("Traceback details:\ntraceback stuff",)
    assert log_kwargs2 == {}
    assert path_mock.call_count == 1
    assert shutil_mock.call_count == 1
