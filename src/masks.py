import logging
import pathlib

log_file_path = pathlib.Path('V:/project/PythonProject10.1/logs/masks.log')

log_file_path.parent.mkdir(parents=True, exist_ok=True)

# Настраиваем базовый уровень логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создаем стандартный форматтер для логов
formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s: - %(message)s')

# Хендлер записи логов в файл
file_handler = logging.FileHandler(log_file_path.as_posix(), mode="w", encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты в формате XXXX XX** **** XXXX.
    Вызывает ValueError если:
    - Номер содержит не только цифры
    - Длина номера не 16 цифр
    """
    logger.info("Функция get_mask_card_number запущена")
    # Удаляем пробелы из номера карты
    card_number = card_number.replace(" ", "")

    # Проверяем, что номер карты состоит из 16 цифр
    if len(card_number) != 16:
        logger.error("Длина номера карты отличается от 16 знаков")
        raise ValueError("Номер карты должен состоять из 16 цифр")

    # Проверяем, что номер карты содержит только цифры
    if not card_number.isdigit():
        logger.error("Номер карты содержит нецифровые символы")
        raise ValueError("Номер карты должен содержать только цифры")

    # Берем первые 6 цифр и последние 4 цифры
    first_part = card_number[:6]
    last_part = card_number[-4:]

    # Создаем маску
    masked_number = f"{first_part[:4]} {first_part[4:]}** **** {last_part}"
    logger.debug(f"Сформирована маска карты: {masked_number}")
    return masked_number


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета в формате **XXXX.
    account_number: Номер счета в виде строки.
    """
    logger.info("Функция get_mask_account запущена")

    # Берем последние 4 цифры
    last_part = account_number[-4:]

    # Создаем маску из двух звездочек
    masked_number = f"**{last_part}"
    logger.debug(f"Сформирована маска счета: {masked_number}")
    return masked_number


# Пример использования
if __name__ == "__main__":
    card_number = "7000792289606361"
    print(get_mask_card_number(card_number))  # Вывод: 7000 79** **** 6361

    account_number = "73654108430135874305"
    print(get_mask_account(account_number))  # Вывод: **4305
