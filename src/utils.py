import json
import logging
import os
import re
from collections import Counter

import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('logs/utils.log', mode="w", encoding='utf-8')
file_formatter = logging.Formatter(
    '%(asctime)s - %(filename)s - %(levelname)s: - %(message)s'
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

load_dotenv()


def open_json(path: str) -> list:
    """Преобразует JSON-объект в Python-объект."""
    logger.info("Функция open_json запущена")
    try:
        with open(path, 'r', encoding="utf-8") as f:
            logger.info("Функция преобразования JSON объект в питон объект")
            return json.load(f)
    except FileNotFoundError as e:
        logger.error(f"Ошибка: {e} файл не найден")
        return []
    except json.JSONDecodeError as t:
        logger.error(f"Ошибка: {t} формат JSON объекта не соответствует")
        return []
    except Exception as y:
        logger.error(f"Ошибка: {y}")
        return []


def currency_convertor(currency: str, amount: float) -> float:
    """Конвертирует валюту в рубли через API."""
    new_currency = "RUB"
    url = (f"https://api.apilayer.com/exchangerates_data/convert?"
           f"to={new_currency}&from={currency}&amount={amount}")
    headers = {"apikey": os.getenv("APILAYER_KEY")}
    response = requests.get(url, headers=headers)
    return float(response.json()["result"])


def convertor_to_rubles(operation: dict) -> float:
    """Конвертирует валюту операции в рубли."""
    logger.info("Функция convertor_to_rubles запущена")
    try:
        if operation["operationAmount"]["currency"]["code"] == "RUB":
            logger.info("Функция вернула сумму в рублях")
            return float(operation["operationAmount"]["amount"])
        operation_currency = operation["operationAmount"]["currency"]["code"]
        operation_amount = operation["operationAmount"]["amount"]
        logger.info("Функция вернула конвертированную сумму в рублях")
        return float(currency_convertor(operation_currency, operation_amount))
    except (KeyError, ValueError) as z:
        logger.error(f"Ошибка: {z}")
        return 0.0


def process_bank_search(operations: list[dict], search_string: str) -> list[dict]:
    """
    Выполняет поиск по операциям банка.

    Возвращает операции, чьи описания содержат указанную строку.

    Args:
        operations: Список транзакционных операций
        search_string: Строка для поиска в описаниях

    Returns:
        Список операций, содержащих заданную строку
    """
    result = []
    re_pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    for operation in operations:
        if re_pattern.search(str(operation.get("description", ""))):
            result.append(operation)
    return result


def process_bank_operations(data: list[dict], categories: list[str]) -> dict:
    """
    Подсчитывает частоту встречаемости категорий операций.

    Args:
        data: Список транзакций
        categories: Список интересующих категорий

    Returns:
        Словарь с количеством операций по категориям
    """
    counter_categories = []
    for operation in data:
        category = operation.get("description", "")
        if category in categories:
            counter_categories.append(category)
    return Counter(counter_categories)


def main():
    """Пример использования функций модуля."""
    example_operation = {
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {
            "amount": "8221.37",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        }
    }
    print(convertor_to_rubles(example_operation))


if __name__ == "__main__":
    main()
