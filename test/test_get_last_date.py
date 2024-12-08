from unittest.mock import patch, mock_open

from src.get_last_date import get_last_date


def test_read_from_file_with_one_line():
    test_date = "2000-01-01-00-00-00"
    test_file_date = "2000-01-01-00-10-00"
    test_file = f"test_id,test_amount,{test_date},test_latitude,test_longitude"
    m = mock_open(read_data=test_file)
    with patch("builtins.open", m):
        with patch("src.get_last_date.get_latest_folder", return_value=test_file_date):
            result = get_last_date()
    m.assert_called_once_with(
        f"data/extract/{test_file_date}/purchases.csv", "r", encoding="utf-8"
    )
    assert result == test_date


def test_read_from_file_with_multiple_lines():
    test_date = "2000-01-01-00-00-00"
    test_file_date = "2000-01-01-00-10-00"
    test_file = f"""test_id,test_amount,{test_date},test_latitude,test_longitude
test_id,test_amount,1999-12-01-00-00-00,test_latitude,test_longitude
test_id,test_amount,1999-11-01-00-00-00,test_latitude,test_longitude
test_id,test_amount,1999-10-01-00-00-00,test_latitude,test_longitude
test_id,test_amount,1999-09-01-00-00-00,test_latitude,test_longitude
test_id,test_amount,1999-08-01-00-00-00,test_latitude,test_longitude
test_id,test_amount,1999-07-01-00-00-00,test_latitude,test_longitude
test_id,test_amount,1999-06-01-00-00-00,test_latitude,test_longitude"""
    m = mock_open(read_data=test_file)
    with patch("builtins.open", m):
        with patch("src.get_last_date.get_latest_folder", return_value=test_file_date):
            result = get_last_date()
    m.assert_called_once_with(
        f"data/extract/{test_file_date}/purchases.csv", "r", encoding="utf-8"
    )
    assert result == test_date


def test_if_no_latest_folder_return_none():
    with patch("src.get_last_date.get_latest_folder", return_value=None):
        result = get_last_date()
    assert result is None
