# Проект "Домашнее задание 10.1. Фильтрация и сортировка данных"

## Описание:

Проект "Фильтрация и сортировка данных" — это Python-модуль, который предоставляет функции для фильтрации списка словарей по состоянию и сортировки по дате. Этот модуль может быть использован для обработки данных, таких как транзакции, события или любые другие записи с датой и состоянием.

## Функции:

### Функция `filter_by_state`
- **Описание**: Фильтрует список словарей, оставляя только те, где ключ `state` равен заданному значению.
- **Параметры**:
  - `data`: Список словарей для фильтрации.
  - `state`: Значение, по которому фильтруем (по умолчанию `'EXECUTED'`).
- **Возвращает**: Новый список словарей, соответствующих условию.

### Функция `sort_by_date`
- **Описание**: Сортирует список словарей по ключу `'date'`.
- **Параметры**:
  - `data`: Список словарей для сортировки.
- **Возвращает**: Новый список словарей, отсортированных по дате (по умолчанию по убыванию).

## Установка:

1. Клонируйте репозиторий:
   ```python
   git clone git@github.com:IMPAIA1967/feature-homework_10_1.git
2. Установите зависимости:
   ```python
   pip install -r requirements.txt

## Файлы и их содержимое
#### tests/test_masks.py
Содержит тесты для функций маскировки номеров карт и счетов:
- `test_get_mask_card_number_valid` - Тест корректного номера карты
- `test_get_mask_card_number_short` - Тест слишком короткого номера карты
- `test_get_mask_card_number_long` - Тест слишком длинного номера карты
- `test_get_mask_card_number_invalid_chars` - Тест номера с недопустимыми символами
- `test_get_mask_card_number_no_spaces` - Тест номера без пробелов
- `test_get_mask_card_number_with_extra_spaces` - Тест номера с дополнительными пробелами
- `test_get_mask_card_number_with_leading_trailing_spaces` - Тест номера с пробелами в начале и конце
### Тесты маскировки счетов:
- `test_get_mask_account` - Тестирование маскировки номера счета
- `test_various_account_numbers` - Тестирование различных номеров счетов

### Комплексные тесты:
- `test_various_card_numbers` - Тестирование различных номеров карт
- `test_main_output` - Проверка вывода функций маскировки
## Тесты модуля masks.py

- Карты:
  - `test_get_mask_card_number_valid` - Корректный номер
  - `test_get_mask_card_number_short` - Слишком короткий номер
  - `test_get_mask_card_number_long` - Слишком длинный номер
  - `test_get_mask_card_number_invalid_chars` - Недопустимые символы
  - `test_get_mask_card_number_no_spaces` - Без пробелов
  - `test_get_mask_card_number_with_extra_spaces` - Лишние пробелы
  - `test_get_mask_card_number_with_leading_trailing_spaces` - Пробелы по краям

- Счета:
  - `test_get_mask_account` - Базовая маскировка
  - `test_various_account_numbers` - Различные форматы

- Интеграционные:
  - `test_various_card_numbers` - Параметризованный тест карт
  - `test_main_output` - Проверка основного вывода
## Тесты модуля processing.py

### Тесты фильтрации:
- `test_filter_empty_data` - Тест фильтрации пустого списка
- `test_filter_by_state` - Тестирование фильтрации по статусу (EXECUTED/CANCELED)
- `test_filter_by_state_empty` - Тест фильтрации с пустым значением state
- `test_filter_by_state_unknown` - Тест фильтрации с несуществующим значением state

### Тесты сортировки:
- `test_sort_with_same_dates` - Тест сортировки при одинаковых датах
- `test_sort_empty_data` - Тест сортировки пустого списка
- `test_sort_invalid_dates` - Тест сортировки с некорректными датами
- `test_sort_single_item` - Тест сортировки списка с одним элементом

### Интеграционные тесты:
- `test_main_data_processing` - Комплексное тестирование обработки данных из main
## Тесты обработки данных (processing.py)

### Для функции filter_by_state():
- `test_filter_empty_data` - Пустой входной список
- `test_filter_by_state` - Стандартные кейсы (EXECUTED, CANCELED)
- `test_filter_by_state_empty` - Пустое значение state
- `test_filter_by_state_unknown` - Несуществующий статус

### Для функции sort_by_date():
- `test_sort_empty_data` - Пустой список
- `test_sort_single_item` - Один элемент
- `test_sort_with_same_dates` - Одинаковые даты
- `test_sort_invalid_dates` - Некорректные форматы дат

### Сквозные тесты:
- `test_main_data_processing` - Полный цикл обработки
## Тесты модуля widget.py

### Тесты маскировки карт:
- `test_mask_card_number_standard` - Стандартный номер карты
- `test_mask_card_number_with_spaces` - Номер с пробелами
- `test_mask_card_number_short` - Слишком короткий номер
- `test_mask_card_number_invalid_chars` - Недопустимые символы

### Тесты маскировки счетов:
- `test_mask_account_number_standard` - Стандартный номер счета

### Тесты обработки платежных данных:
- `test_mask_account_card_visa` - Карта Visa
- `test_mask_account_card_empty` - Пустая строка
- `test_mask_account_card_only_type_no_number` - Только тип карты
- `test_mask_account_card_various` - Различные входные данные

### Тесты форматирования дат:
- `test_standard_date_format` - Стандартный формат
- `test_date_without_time` - Дата без времени
- `test_single_digit_month_day` - Однозначные день/месяц
- `test_invalid_date_format` - Некорректный формат
- `test_invalid_date_format_with_spaces` - Некорректный формат с пробелами
- ## Тесты виджетов (widget.py)

### Маскировка:
- Карты:
  - `test_mask_card_number_standard` - Стандартный случай
  - `test_mask_card_number_with_spaces` - С пробелами
  - `test_mask_card_number_short` - Короткий номер (ошибка)
  - `test_mask_card_number_invalid_chars` - Невалидные символы
  
- Счета:
  - `test_mask_account_number_standard` - Базовый тест

### Обработка платежных данных:
- `test_mask_account_card_visa` - Visa
- `test_mask_account_card_empty` - Пустой ввод
- `test_mask_account_card_only_type_no_number` - Только тип
- `test_mask_account_card_various` - Параметризованный тест

### Форматирование дат:
- Валидные:
  - `test_standard_date_format` - ISO формат
  - `test_date_without_time` - Только дата
  - `test_single_digit_month_day` - Однозначные числа
  
- Невалидные:
  - `test_invalid_date_format` - Неправильный формат
  - `test_invalid_date_format_with_spaces` - С пробелами
## Как запустить тесты

1. Установите зависимости:
   ```python
   pip install pytest
2. Запустите тесты:
   ```python
   pytest tests/ 
## Генераторы данных о транзакциях
Этот модуль содержит три функции для работы с банковскими транзакциями:

Основные функции
####  filter_by_currency(transactions, currency_code)
- Фильтрует список транзакций по указанной валюте
- Принимает:
- transactions - список словарей с транзакциями
- currency_code - код валюты ('USD', 'RUB' и т.д.)
- Возвращает генератор, который выдает только транзакции в заданной валюте
- Пример: получить все операции в долларах
#### transaction_descriptions(transactions)
- Извлекает описания транзакций
- Принимает список словарей с транзакциями
- Возвращает генератор описаний операций
- Пример: вывести все описания платежей
#### card_number_generator(start, end)
- Генерирует номера банковских карт
- Принимает:
- start - начальный номер
- end - конечный номер
- Возвращает номера карт в формате "XXXX XXXX XXXX XXXX"
- Номера дополняются нулями слева до 16 цифр
- Пример: сгенерировать номера карт от 1 до 5