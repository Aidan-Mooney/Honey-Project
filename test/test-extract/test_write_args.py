from unittest.mock import patch, call


from src.extract.write_args import write_args


def test_one_string_arg_is_written():
    test_path = "test_path"
    test_arg = "arrrrrr...g"
    with patch("builtins.open") as open_mock:
        write_args(test_path, test_arg)
    open_mock.assert_has_calls(
        [
            call(test_path, "a+", encoding="utf-8"),
            call().__enter__(),
            call().__enter__().write(test_arg),
            call().__enter__().write("\n"),
            call().__exit__(None, None, None),
        ]
    )


def test_multiple_string_args_are_written_in_csv_format():
    test_path = "test_path"
    test_args = (
        "arrrrrr...g1",
        "arrrrrr...g2",
        "arrrrrr...g3",
        "arrrrrr...g4",
        "arrrrrr...g5",
    )
    with patch("builtins.open") as open_mock:
        write_args(test_path, *test_args)
    call_data = []
    call_data.append(call(test_path, "a+", encoding="utf-8"))
    call_data.append(call().__enter__())
    for arg in test_args[:-1]:
        call_data.append(call().__enter__().write(arg))
        call_data.append(call().__enter__().write(","))
    call_data.append(call().__enter__().write(test_args[-1]))
    call_data.append(call().__enter__().write("\n"))
    call_data.append(call().__exit__(None, None, None))
    open_mock.assert_has_calls(call_data)


def test_multiple_args_with_data_types_like_int_and_float_are_written_in_csv_format():
    test_path = "test_path"
    test_args = (
        "arrrrrr...g1",
        "arrrrrr...g2",
        "arrrrrr...g3",
        "arrrrrr...g4",
        "arrrrrr...g5",
        1,
        1.05,
    )
    with patch("builtins.open") as open_mock:
        write_args(test_path, *test_args)
    call_data = []
    call_data.append(call(test_path, "a+", encoding="utf-8"))
    call_data.append(call().__enter__())
    for arg in test_args[:-2]:
        call_data.append(call().__enter__().write(arg))
        call_data.append(call().__enter__().write(","))
    call_data.append(call().__enter__().write(str(test_args[-2])))
    call_data.append(call().__enter__().write(","))
    call_data.append(call().__enter__().write(str(test_args[-1])))
    call_data.append(call().__enter__().write("\n"))
    call_data.append(call().__exit__(None, None, None))
    open_mock.assert_has_calls(call_data)
