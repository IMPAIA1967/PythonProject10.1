import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def open_json(path: str) -> list:
    try:
        with open(path, 'r', encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    except Exception:
        return []

def currency_convertor(currency: str, amount: float) -> float:
    """Функция, которая конвертирует валюту в рубли"""
    new_currency = "RUB"
    url = f"https://api.apilayer.com/exchangerates_data/convert?to={new_currency}&from={currency}&amount={amount}"
    payload = {}
    headers = {"apikey": os.getenv("APILAYER_KEY")}
    response = requests.request("GET", url, headers=headers, data=payload)
    return float(response.json()["result"])

def convertor_to_rubles(operation: dict) -> float:
    """Функция, которая конвертирует валюту в рубли"""
    try:
        if operation["operationAmount"]["currency"]["code"] == "RUB":
            return float(operation["operationAmount"]["amount"])
        else:
            operation_currency = operation["operationAmount"]["currency"]["code"]
            operation_amount = operation["operationAmount"]["amount"]
            return float(currency_convertor(operation_currency, operation_amount))
    except (KeyError, ValueError):
        return 0.0

print(convertor_to_rubles({
    "id": 41428829,
    "state": "EXECUTED",
    "date": "2019-07-03T18:35:29.512364",
    "operationAmount": {
        "amount": "8221.37",
        "currency": {
            "name": "USD",
            "code": "USD"
        }}}))






