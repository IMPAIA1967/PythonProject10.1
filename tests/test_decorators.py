import pytest

from src.decorators import log


def test_log_error_console(capsys) -> None:
    """Проверяет запись ошибки в консоль при использовании декоратора @log"""
    @log(filename="mylog.txt")
    def foo(x: int, y: int) -> int:
        return x + y

    with pytest.raises(TypeError):
        foo(1, "2")

    captured = capsys.readouterr()
    expected = "foo - <class 'TypeError'> - args: (1, '2') - kwargs: {}\n"
    assert captured.out == expected


def test_log_success(capsys) -> None:
    """Тестирует корректную работу декоратора log при успешном выполнении функции."""
    @log(filename="mylog.txt")
    def foo_(x: int, y: int) -> int:
        return x + y

    result = foo_(1, 2)
    assert result == 3
    captured = capsys.readouterr()
    expected = f"foo_ - {result}\n"
    assert captured.out == expected


def test_log_success_file() -> None:
    """Проверяет запись успешного результата в файл"""
    file_name: str = "src/mylog.txt"

    @log(filename="src/mylog.txt")
    def boo(x: int, y: int) -> int:
        return x + y

    result = boo(1, 2)
    assert result == 3

    with open(file_name, "r", encoding="utf-8") as f:
        content = f.readlines()
        assert content[-1].strip() == "boo - 3"


def test_log_multiple_calls(capsys) -> None:
    """Проверяет корректность логирования при множественных вызовах функции"""
    @log(filename="mylog.txt")
    def roo(x: int, y: int) -> int:
        return x + y
    roo(1, 2)
    roo(3, 4)
    captured = capsys.readouterr()
    assert captured.out.strip() == "roo - 3\nroo - 7"


def test_log_no_filename() -> None:
    """Тестирует работу декоратора log без указания имени файла, с выводом только в консоль."""
    @log(filename=None)
    def goo(x: int, y: int) -> int:
        return x + y
    result = goo(1, 2)
    assert result == 3
