import json
import os

from src.utils import convertor_to_rubles, open_json

# Временный файл для хранения данных
TEST_FILE = "test_data.json"


def teardown_function() -> None:
    """Удаляет временный файл после каждого теста"""
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


def test_open_json_valid() -> None:
    """Чтение корректного JSON-списка"""
    data = [{"id": 1}, {"id": 2}]
    with open(TEST_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

    loaded_data = open_json(TEST_FILE)
    assert loaded_data == data


def test_open_json_file_not_found() -> None:
    """Обработка случая, когда файл не найден"""
    assert open_json("non_existent.json") == []


def test_open_json_empty_file() -> None:
    """Чтение пустого файла"""
    with open(TEST_FILE, "w", encoding="utf-8") as f:
        f.write("")

    loaded_data = open_json(TEST_FILE)
    assert loaded_data == []


def test_open_json_invalid_json() -> None:
    """Обработка невалидного JSON"""
    with open(TEST_FILE, "w", encoding="utf-8") as f:
        f.write("{not valid json}")

    loaded_data = open_json(TEST_FILE)
    assert loaded_data == []


def test_convertor_to_rubles_rub() -> None:
    """Прямая обработка транзакции в рублях"""
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
    """Проверка обработки некорректных данных"""
    invalid_transaction = {}
    converted_amount = convertor_to_rubles(invalid_transaction)
    assert converted_amount == 0.0
