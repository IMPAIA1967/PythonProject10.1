from src.processing import filter_by_state, sort_by_date
from src.read_csv_excel import read_csv, read_excel
from src.utils import open_json, process_bank_operations, process_bank_search
from src.widget import get_date, mask_account_card


def main():
    print("""Программа: Привет! Добро пожаловать в программу работы
с банковскими транзакциями.
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла
""")

    # Выбор формата файлов
    while True:
        user_input = input("Введите номер из пункта меню: ")

        if user_input == "1":
            transactions_data = open_json("data/operations.json")
            print("Для обработки выбран JSON-файл.")
            break
        elif user_input == "2":
            transactions_data = read_csv("data/transactions.csv")
            print("Для обработки выбран CSV-файл.")
            break
        elif user_input == "3":
            transactions_data = read_excel("data/transactions_excel.xlsx")
            print("Для обработки выбран XLSX-файл.")
            break
        else:
            print("Неверный ввод. Такого пункта нет, введите что-то из предложенного.")

    # Выбор статуса транзакций
    while True:
        print(
            "Программа: Введите статус, по которому необходимо выполнить фильтрацию." +
            "\nДоступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"
        )
        AVAILABLE_STATUSES = ['EXECUTED', 'CANCELED', 'PENDING']
        user_state = input("Введите статус: ").upper().strip()

        if user_state in AVAILABLE_STATUSES:
            break
        else:
            print(f'Статус операции "{user_state}" недоступен.')

    # Фильтрация по состоянию
    transactions_data = filter_by_state(transactions_data, state=user_state)
    print(f'Операции отфильтрованы по статусу "{user_state}".')

    # Поисковая строка
    search_string = input("Введите строку для поиска: ")
    filtered_transactions = process_bank_search(transactions_data, search_string)

    # Вопрос о сортировке
    while True:
        sort_answer = input("Отсортировать операции по дате? Да/Нет: ").lower().strip()
        if sort_answer == "да":
            while True:
                order = input("Отсортировать по возрастанию или по убыванию? : ").lower().strip()
                if order == "по возрастанию":
                    sorted_transactions = sort_by_date(filtered_transactions)
                    break
                elif order == "по убыванию":
                    sorted_transactions = sort_by_date(filtered_transactions, reverse=True)
                    break
                else:
                    print("Неправильный выбор способа сортировки. Введите 'по возрастанию' или 'по убыванию'.")
            break
        elif sort_answer == "нет":
            sorted_transactions = filtered_transactions
            break
        else:
            print("Некорректный ответ. Попробуйте ещё раз.")

    # Вопрос о валюте
    currency_filter = input("Выводить только рублевые транзакции? Да/Нет: ").lower().strip()
    if currency_filter == "да":
        sorted_transactions = [
            t
            for t in sorted_transactions
            if t.get('operationAmount', {}).get('currency', {}).get('code') == 'RUB'
        ]

    # Вопрос о поиске слова в описании
    keyword_answer = input(
        "Отфильтровать список транзакций по определенному слову в описании? Да/Нет: "
    ).strip().lower()
    if keyword_answer == "да":
        keyword = input("Введите слово для поиска: ").strip()
        if keyword:
            filtered_transactions = process_bank_search(filtered_transactions, keyword)
            print(f"Фильтрация по описанию завершена. Найдено операций: {len(filtered_transactions)}")
    else:
        print("Фильтрация по описанию пропущена.")

    # Итоговый вывод
    print("\nРаспечатываю итоговый список транзакций...\n")
    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(filtered_transactions)}\n")
        for txn in filtered_transactions:
            try:
                date = get_date(txn.get("date", ""))
            except (ValueError, TypeError):
                date = "Дата недоступна"

            description = txn.get("description", "Без описания")
            from_info = txn.get("from", "")
            to_info = txn.get("to", "")
            amount_info = txn.get("operationAmount", {})
            amount = amount_info.get("amount", "")
            currency = amount_info.get("currency", {}).get("name", "")

            print(f"{date} {description}")
            if from_info:
                print(f"{mask_account_card(from_info)} -> {mask_account_card(to_info)}")
            else:
                print(f"{mask_account_card(to_info)}")
            print(f"Сумма: {amount} {currency}\n")

    # Статистика по категориям
    stats_answer = input("Хотите увидеть статистику по операциям по категориям? Да/Нет: ").strip().lower()
    if stats_answer == "да":
        categories = list({txn.get("description", "").strip() for txn in filtered_transactions})
        stats = process_bank_operations(filtered_transactions, categories)
        print("\nСтатистика по категориям:")
        for category, count in stats.items():
            print(f"{category}: {count} операций")
    else:
        print("Просмотр статистики по категориям пропущен.")


if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))  # Пример маскирования номера карты
    print(mask_account_card("Счет 73654108430135874305"))      # Пример маскирования счёта
    print(get_date("2024-03-11T02:26:18.671407"))             # Пример преобразования даты
    main()
