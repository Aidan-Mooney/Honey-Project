from unittest.mock import patch
from src.extract.get_latest_folder import get_latest_folder


def test_returns_none_if_directory_is_empty():
    with patch("src.extract.get_latest_folder.os") as os_mock:
        os_mock.listdir.return_value = []
        result = get_latest_folder()
    assert result is None


def test_returns_only_directory_if_there_is_one_directory():
    test_date = "2000-01-01-00-00-00"
    with patch("src.extract.get_latest_folder.os") as os_mock:
        os_mock.listdir.return_value = [test_date]
        result = get_latest_folder()
    assert result == test_date


def test_returns_latest_directory_if_many_are_in_directory():
    test_latest_date = "2024-01-01-00-00-00"
    other_dates = [
        "2000-01-01-00-01-00",
        "2000-01-01-00-02-00",
        "2000-01-01-00-03-00",
        "2000-01-01-00-04-00",
        "2000-01-01-00-05-00",
    ]
    with patch("src.extract.get_latest_folder.os") as os_mock:
        os_mock.listdir.return_value = [test_latest_date] + other_dates
        result = get_latest_folder()
    assert result == test_latest_date
