from typing import Any, Callable, Optional


def write_log(message: str, filename: Optional[str] = None):
    """Записывает сообщение в консоль или в файл
    message: Текст сообщения для записи
        filename: Опциональный путь к файлу. Если None - только вывод в консоль
    """
    print(message, end='')
    if filename:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(message)
    else:
        print(message)


def log(filename: Optional[str] = None) -> Callable:
    """Декоратор для логирования вызовов функций и их результатов"""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} - {result}\n"
                write_log(message, filename)
                return result
            except Exception as e:
                message = f"{func.__name__} - {type(e)} - args: {args} - kwargs: {kwargs}\n"
                write_log(message, filename)
                raise
        return wrapper
    return decorator


@log(filename="mylog.txt")
def foo(x, y):
    return x + y


print(foo(1, 2))
