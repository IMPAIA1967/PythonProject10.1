from typing import Dict, Generator, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.mark.parametrize('currency, expected', [
    ('USD', {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    }),
    ('RUB', {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {
            "amount": "43318.34",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160"
    })
])
def test_filter_by_currency(currency: str, expected: Dict[str, any], transactions: List[Dict]) -> None:
    _generator = filter_by_currency(transactions, currency)
    assert next(_generator) == expected


def test_card_number_generator() -> None:
    _generator = card_number_generator(1, 5)
    assert next(_generator) == "0000 0000 0000 0001"
    assert next(_generator) == "0000 0000 0000 0002"
    assert next(_generator) == "0000 0000 0000 0003"
    assert next(_generator) == "0000 0000 0000 0004"
    assert next(_generator) == "0000 0000 0000 0005"
    with pytest.raises(StopIteration):
        next(_generator)


def test_transaction_descriptions() -> None:
    TEST_TRANSACTIONS: List[Dict[str, any]] = [
        {"description": "Перевод организации", "id": 1, "amount": 100},
        {"description": "Перевод со счета на счет", "id": 2, "amount": 200},
        {"description": "Оплата услуг", "id": 3, "amount": 300}
    ]

    def test_returns_correct_descriptions_in_order() -> None:
        """Проверяет порядок возвращаемых описаний"""
        _generator: Generator[str, None, None] = transaction_descriptions(TEST_TRANSACTIONS)
        assert next(_generator) == "Перевод организации"
        assert next(_generator) == "Перевод со счета на счет"
        assert next(_generator) == "Оплата услуг"
        with pytest.raises(StopIteration):
            next(_generator)

    def test_works_with_empty_list() -> None:
        """Проверяет работу с пустым списком"""
        generator: Generator[str, None, None] = transaction_descriptions([])
        with pytest.raises(StopIteration):
            next(generator)
