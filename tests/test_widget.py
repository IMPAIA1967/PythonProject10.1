import pytest

from src.widget import get_date, mask_account_card, mask_account_number, mask_card_number


def test_mask_card_number_standard() -> None:
    assert mask_card_number("7000792289606361") == "7000 79** **** 6361"


def test_mask_card_number_with_spaces() -> None:
    assert mask_card_number("7000 7922 8960 6361") == "7000 79** **** 6361"


def test_mask_card_number_short() -> None:
    """Тест слишком короткого номера карты"""
    with pytest.raises(IndexError, match="Номер карты должен состоять из 16 цифр"):
        mask_card_number("123456789012")  # 12 цифр вместо 16


def test_mask_card_number_invalid_chars() -> None:
    """Тест номера с недопустимыми символами"""
    with pytest.raises(ValueError, match="Номер карты должен содержать только цифры"):
        mask_card_number("7000abcd89606361")


def test_mask_account_number_standard() -> None:
    assert mask_account_number("73654108430135874305") == "**4305"


def test_mask_account_card_visa() -> None:
    assert mask_account_card("Visa 7000792289606361") == "7000 79** **** 6361"


def test_mask_account_card_empty() -> None:
    assert mask_account_card("") == "Неизвестный тип"


def test_mask_account_card_only_type_no_number() -> None:
    result = mask_account_card("Visa")
    assert result == "Неизвестный тип"


@pytest.mark.parametrize("input_data, expected", [
    ("Visa 7000792289606361", "7000 79** **** 6361"),
    ("Счет 73654108430135874305", "**4305"),
    ("Unknown 123", "Неизвестный тип"),
])
def test_mask_account_card_various(input_data: str, expected: str) -> None:
    assert mask_account_card(input_data) == expected


def test_standard_date_format() -> None:
    """Тест стандартного формата даты"""
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"


def test_date_without_time() -> None:
    """Тест даты без времени"""
    assert get_date("2024-03-11") == "11.03.2024"


def test_single_digit_month_day() -> None:
    """Тест даты с однозначными месяцем и днем"""
    assert get_date("2024-3-1T00:00:00") == "01.03.2024"


def test_invalid_date_format() -> None:
    """Тест некорректного формата даты"""
    with pytest.raises(ValueError):
        get_date("2024/03/11T02:26:18.671407")  # Некорректный разделитель


def test_invalid_date_format_with_spaces() -> None:
    """Тест некорректного формата даты с пробелами"""
    with pytest.raises(ValueError):
        get_date("2024-03-11 T02:26:18.671407")  # Пробел перед 'T'
