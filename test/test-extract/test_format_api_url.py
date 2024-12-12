import pytest
from src.extract.format_api_url import format_api_url


def test_a_string_is_returned():
    test_url = "https://iamnotrealwakeup.com/api"
    result = format_api_url(test_url)
    assert isinstance(result, str)


def test_a_url_with_default_limit_and_no_kwargs_passed_returns_the_same_url():
    test_url = "https://iamnotrealwakeup.com/api"
    result = format_api_url(test_url)
    assert result == f"{test_url}?limit=50"


def test_a_url_with_different_limit():
    test_url = "https://iamnotrealwakeup.com/api"
    limit = 20
    result = format_api_url(test_url, limit=limit)
    assert result == f"{test_url}?limit={limit}"


def test_url_is_formatted_with_kwargs():
    test_url = "https://iamnotrealwakeup.com/api"
    test_last_purchase_hash = "string"
    result = format_api_url(test_url, lastPurchaseHash=test_last_purchase_hash)
    assert result == f"{test_url}?limit=50&lastPurchaseHash={test_last_purchase_hash}"


def test_value_error_is_raised_if_limit_is_greater_than_one_thousand():
    test_url = "https://iamnotrealwakeup.com/api"
    with pytest.raises(ValueError) as err:
        format_api_url(test_url, limit=1001)
    assert (
        str(err.value)
        == "limit must be a positive, non-zero integer less than one thousand"
    )


def test_type_error_is_raised_for_invalid_base_url_type():
    test_url = 1000
    with pytest.raises(TypeError) as err:
        format_api_url(test_url)
    assert str(err.value) == "base_url must be a string"


def test_type_error_is_raised_for_invalid_limit_type():
    test_url = "https://iamnotrealwakeup.com/api"
    limit = 1.1
    with pytest.raises(TypeError) as err:
        format_api_url(test_url, limit=limit)
    assert str(err.value) == "limit must be an int"
