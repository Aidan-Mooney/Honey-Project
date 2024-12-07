from unittest.mock import patch


from src.refresh_token import refresh_token


PATCH_PATH = "src.refresh_token"


def test_none_is_returned_if_the_expiry_time_has_not_been_reached():
    test_token_url = "https://token_url.com/token"
    test_auth_id = "auth_id"
    test_auth_secret = "auth_secret"
    test_start_time = 0
    test_time_till_expiry = 2
    with patch(f"{PATCH_PATH}.dt") as dt_mock:
        dt_mock.now.return_value.timestamp.return_value = 1
        with patch(f"{PATCH_PATH}.get_token") as token_mock:
            result = refresh_token(
                test_token_url,
                test_auth_id,
                test_auth_secret,
                test_start_time,
                test_time_till_expiry,
            )
    assert result is None
    assert token_mock.call_count == 0


def test_new_token_start_time_and_expiry_is_returned_on_refresh():
    test_token_url = "https://token_url.com/token"
    test_auth_id = "auth_id"
    test_auth_secret = "auth_secret"
    test_start_time = 0
    test_time_till_expiry = 1
    test_token = "token"
    token_response = (200, {"access_token": test_token, "expires_in": 10})
    with patch(f"{PATCH_PATH}.dt") as dt_mock:
        dt_mock.now.return_value.timestamp.side_effect = [2, 5]
        with patch(f"{PATCH_PATH}.get_token") as token_mock:
            token_mock.return_value = token_response
            result = refresh_token(
                test_token_url,
                test_auth_id,
                test_auth_secret,
                test_start_time,
                test_time_till_expiry,
            )
    assert result == (test_token, 5, 10)


def test_warning_log_is_triggered_if_none_200_response_is_returned_from_get_token():
    test_token_url = "https://token_url.com/token"
    test_auth_id = "auth_id"
    test_auth_secret = "auth_secret"
    test_start_time = 0
    test_time_till_expiry = 1
    token_response = (404, {"code": 404, "message": "HTTP 404 Not Found"})
    with patch(f"{PATCH_PATH}.dt") as dt_mock:
        dt_mock.now.return_value.timestamp.side_effect = [2, 5]
        with patch(f"{PATCH_PATH}.get_token") as token_mock:
            token_mock.return_value = token_response
            with patch(f"{PATCH_PATH}.logging") as log_mock:
                result = refresh_token(
                    test_token_url,
                    test_auth_id,
                    test_auth_secret,
                    test_start_time,
                    test_time_till_expiry,
                )
    assert log_mock.warning.call_count == 1
    log_args, log_kwargs = log_mock.warning.call_args
    assert log_args == (
        f"HTTP code: {token_response[0]}, body returned: {token_response[1]} when calling get_token.",
    )
    assert log_kwargs == {}
    assert result == "warning"
