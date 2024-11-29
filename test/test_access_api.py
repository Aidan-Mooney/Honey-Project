# from requests.exceptions import HTTPError
from requests.models import Response
import pytest
from src.access_api import access_api
from unittest.mock import patch, Mock


@pytest.fixture
def response_mock():
    return Mock(spec=Response)


def test_valid_url_and_token_returns_json_with_correct_keys(response_mock):
    test_url = "test_url"
    test_token = "test_token"
    return_dict = {"test": "test"}
    response_mock.status_code = 200
    response_mock.json.return_value = return_dict
    with patch("src.access_api.requests") as requests_mock:
        requests_mock.get.return_value = response_mock
        code, result = access_api(test_url, test_token)
    assert isinstance(result, dict)
    assert code == 200
    assert result == return_dict


def test_request_functions_are_called_correctly(response_mock):
    test_url = "test_url"
    test_token = "test_token"
    return_dict = {"test": "test"}
    response_mock.status_code = 200
    response_mock.json.return_value = return_dict
    with patch("src.access_api.requests") as requests_mock:
        requests_mock.get.return_value = response_mock
        access_api(test_url, test_token)
    get_args, get_kwargs = requests_mock.get.call_args
    assert get_args == (test_url,)
    assert get_kwargs == {
        "headers": {"Authorization": f"bearer {test_token}"},
    }
    assert requests_mock.get.call_count == 1
    assert response_mock.json.call_count == 1


def test_http_errors_return_correctly(response_mock):
    test_url = "test_url"
    test_token = "test_token"
    return_dict = {"code": 404, "message": "HTTP 404 Not Found"}
    response_mock.status_code = 404
    response_mock.json.return_value = return_dict
    with patch("src.access_api.requests") as requests_mock:
        requests_mock.get.return_value = response_mock
        code, result = access_api(test_url, test_token)
    get_args, get_kwargs = requests_mock.get.call_args
    assert get_args == (test_url,)
    assert get_kwargs == {
        "headers": {"Authorization": f"bearer {test_token}"},
    }
    assert requests_mock.get.call_count == 1
    assert response_mock.json.call_count == 1
    assert code == 404
    assert result == return_dict
