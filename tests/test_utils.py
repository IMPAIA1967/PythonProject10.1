import json
import os

import pytest

from src.utils import convertor_to_rubles, open_json, process_bank_operations, process_bank_search

# Временный файл для хранения данных
TEST_FILE = "test_data.json"


def teardown_function() -> None:
    """Удаляет временный файл после каждого теста."""
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


def test_open_json_valid() -> None:
    """Чтение корректного JSON-списка."""
    data = [{"id": 1}, {"id": 2}]
    with open(TEST_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

    loaded_data = open_json(TEST_FILE)
    assert loaded_data == data


def test_open_json_file_not_found() -> None:
    """Обработка случая, когда файл не найден."""
    assert open_json("non_existent.json") == []


def test_open_json_empty_file() -> None:
    """Чтение пустого файла."""
    with open(TEST_FILE, "w", encoding="utf-8") as f:
        f.write("")

    loaded_data = open_json(TEST_FILE)
    assert loaded_data == []


def test_open_json_invalid_json() -> None:
    """Обработка невалидного JSON."""
    with open(TEST_FILE, "w", encoding="utf-8") as f:
        f.write("{not valid json}")

    loaded_data = open_json(TEST_FILE)
    assert loaded_data == []


def test_convertor_to_rubles_rub() -> None:
    """Прямая обработка транзакции в рублях."""
    transaction = {
        "operationAmount": {
            "amount": "1000.00",
            "currency": {
                "code": "RUB"
            }
        }
    }
    converted_amount = convertor_to_rubles(transaction)
    assert converted_amount == 1000.0


def test_convertor_to_rubles_invalid() -> None:
    """Проверка обработки некорректных данных."""
    invalid_transaction = {}
    converted_amount = convertor_to_rubles(invalid_transaction)
    assert converted_amount == 0.0


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями."""
    return [
        {
            "description": "Оплата услуг",
            "operationAmount": {
                "amount": 1000,
                "currency": {"code": "RUB"}
            }
        },
        {
            "description": "Перевод на карту",
            "operationAmount": {
                "amount": 5000,
                "currency": {"code": "USD"}
            }
        },
        {
            "description": "Оплата налогов",
            "operationAmount": {
                "amount": 1500,
                "currency": {"code": "RUB"}
            }
        },
        {
            "description": "Покупка в магазине",
            "operationAmount": {
                "amount": 2500,
                "currency": {"code": "EUR"}
            }
        },
    ]


def test_process_bank_search_found(sample_transactions):
    """Тест поиска транзакций по строке 'оплата'.

    Утверждается, что поиск по строке "оплата" вернет две транзакции
    с соответствующими описаниями.
    """
    result = process_bank_search(sample_transactions, "оплата")
    assert len(result) == 2
    assert all("оплата" in tx["description"].lower() for tx in result)


def test_process_bank_search_not_found(sample_transactions):
    """Тест поиска при отсутствии совпадений.

    Убеждаемся, что при отсутствии подходящего описания
    результат будет пустым списком.
    """
    result = process_bank_search(sample_transactions, "авиабилеты")
    assert result == []


def test_process_bank_operations(sample_transactions):
    """Тест агрегирования операций по категориям.

    Проверяется, что результатом является точное распределение
    операций по указанным категориям.
    """
    categories = ["Оплата услуг", "Перевод на карту", "Покупка в магазине"]
    result = process_bank_operations(sample_transactions, categories)
    assert result == {
        "Оплата услуг": 1,
        "Перевод на карту": 1,
        "Покупка в магазине": 1,
    }
