import os
import json
import pytest
from unittest.mock import patch, Mock
from src.utils import open_json, currency_convertor, convertor_to_rubles

# Временный файл для хранения данных
TEST_FILE = "test_data.json"

def teardown_function():
    """Удаляет временный файл после каждого теста"""
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

# Тест для функции open_json
def test_open_json_valid():
    """Чтение корректного JSON-списка"""
    data = [{"id": 1}, {"id": 2}]
    with open(TEST_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

    loaded_data = open_json(TEST_FILE)
    assert loaded_data == data

def test_open_json_file_not_found():
    """Обработка случая, когда файл не найден"""
    assert open_json("non_existent.json") == []

def test_open_json_empty_file():
    """Чтение пустого файла"""
    with open(TEST_FILE, "w", encoding="utf-8") as f:
        f.write("")

    loaded_data = open_json(TEST_FILE)
    assert loaded_data == []

def test_open_json_invalid_json():
    """Обработка невадильного JSON"""
    with open(TEST_FILE, "w", encoding="utf-8") as f:
        f.write("{not valid json}")

    loaded_data = open_json(TEST_FILE)
    assert loaded_data == []

# Тест для функции convertor_to_rubles
@patch("src.utils.requests.get")
def test_convertor_to_rubles(mock_get):
    """Преобразование суммы в рубли из USD"""
    FIXED_EXCHANGE_RATE = 65.0  # Фиксированный курс доллара к рублю
    mock_response = Mock()
    mock_response.json.return_value = {"result": FIXED_EXCHANGE_RATE * 100.0}  # Искусственный результат API
    mock_get.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "USD"
            }
        }
    }
    converted_amount = convertor_to_rubles(transaction)
    assert converted_amount == 7849.5827


# Тест обработки транзакций в рублях
def test_convertor_to_rubles_rub():
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

# Тест обработки некорректных данных
def test_convertor_to_rubles_invalid():
    """Проверка обработки некорректных данных"""
    invalid_transaction = {}
    converted_amount = convertor_to_rubles(invalid_transaction)
    assert converted_amount == 0.0