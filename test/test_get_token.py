from requests.exceptions import HTTPError
import pytest
from unittest.mock import patch, Mock
from src.get_token import get_token


def test_correct_url_and_correct_auth_details_returns_a_valid_token_json():
    test_url = "https://test.com/token"
    test_client_id = "test_id"
    test_client_secret = "secret_id"
    test_token = "test_token"
    test_expiry = 7200
    response_mock = Mock()
    response_mock.raise_for_status.return_value = "200 success"
    response_mock.json.return_value = {
        "access_token": test_token,
        "expires_in": test_expiry,
    }
    with patch("src.get_token.requests") as requests_mock:
        requests_mock.post.return_value = response_mock
        result = get_token(test_url, test_client_id, test_client_secret)
    assert isinstance(result, dict)
    assert result["access_token"] == test_token
    assert result["expires_in"] == test_expiry


def test_request_functions_are_called_correctly():
    test_url = "https://test.com/token"
    test_client_id = "test_id"
    test_client_secret = "secret_id"
    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "client_id": test_client_id,
        "assertion": test_client_secret,
    }
    test_token = "test_token"
    test_expiry = 7200
    response_mock = Mock()
    response_mock.raise_for_status.return_value = "200 success"
    response_mock.json.return_value = {
        "access_token": test_token,
        "expires_in": test_expiry,
    }
    with patch("src.get_token.requests") as requests_mock:
        requests_mock.post.return_value = response_mock
        get_token(test_url, test_client_id, test_client_secret)
    post_args, post_kwargs = requests_mock.post.call_args
    assert post_args == (test_url,)
    assert post_kwargs == {
        "data": data,
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
    }
    assert requests_mock.post.call_count == 1
    assert response_mock.raise_for_status.call_count == 1
    assert response_mock.json.call_count == 1


def test_http_errors_are_raised():
    test_url = "https://test.com/token"
    test_client_id = "test_id"
    test_client_secret = "secret_id"
    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "client_id": test_client_id,
        "assertion": test_client_secret,
    }
    response_mock = Mock()
    response_mock.raise_for_status.side_effect = HTTPError("Error Message")
    with patch("src.get_token.requests") as requests_mock:
        requests_mock.post.return_value = response_mock
        with pytest.raises(HTTPError) as err:
            get_token(test_url, test_client_id, test_client_secret)
    assert str(err.value) == "Error Message"
    post_args, post_kwargs = requests_mock.post.call_args
    assert post_args == (test_url,)
    assert post_kwargs == {
        "data": data,
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
    }
    assert requests_mock.post.call_count == 1
    assert response_mock.raise_for_status.call_count == 1
    assert response_mock.json.call_count == 0
