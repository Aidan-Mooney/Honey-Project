from requests.models import Response
from requests.exceptions import HTTPError
import pytest
from unittest.mock import patch, Mock
from src.get_token import get_token


@pytest.fixture
def response_mock():
    return Mock(spec=Response)


def test_correct_url_and_correct_auth_details_returns_a_valid_token_json(response_mock):
    test_url = "https://test.com/token"
    test_client_id = "test_id"
    test_client_secret = "secret_id"
    test_token = "test_token"
    test_expiry = 7200
    response_mock.status_code = 200
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


def test_request_functions_are_called_correctly(response_mock):
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
    response_mock.status_code = 200
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
    assert response_mock.json.call_count == 1


def test_http_errors_are_raised(response_mock):
    test_url = "https://test.com/token"
    test_client_id = "test_id"
    test_client_secret = "secret_id"
    response_mock.status_code = 404
    response_mock.json.return_value = {"code": 404, "message": "HTTP 404 Not Found"}
    response_mock.raise_for_status.side_effect = HTTPError("HTTP 404: Not Found")
    with patch("src.get_token.requests.post") as requests_mock:
        requests_mock.return_value = response_mock
        with pytest.raises(HTTPError) as err:
            get_token(test_url, test_client_id, test_client_secret)
    assert str(err.value) == "HTTP 404: Not Found"
