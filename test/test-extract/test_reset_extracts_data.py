from unittest.mock import patch, call


from src.extract.reset_extracts_data import reset_extracts_data


"https://smhk.net/note/2024/04/python-mock-reading-and-writing-files/"


def test_tables_are_written_with_correct_headings():
    base_path = "data/extract"
    table_data = {
        "card.csv": "uuid,referenceNumber,amount,purchaseUUID1",
        "cash.csv": "uuid,amount,purchaseUUID1",
        "products.csv": "productUuid,name,quantity,purchaseUUID1",
        "purchases.csv": "purchaseUUID1,amount,created,latitude,longitude",
    }
    with patch("builtins.open") as open_mock:
        reset_extracts_data()
    call_data = []
    for fname, value in table_data.items():
        call_data.append(call(f"{base_path}/{fname}", "w", encoding="utf-8"))
        call_data.append(call().__enter__())
        call_data.append(call().__enter__().write(value + "\n"))
        call_data.append(call().__exit__(None, None, None))
    open_mock.assert_has_calls(call_data)
