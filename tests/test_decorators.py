import pytest

from src.decorators import log


def test_log_error_console(capsys):
    """Проверяет запись ошибки в консоль
    при использовании декоратора @log"""
    @log(filename="mylog.txt")
    def foo(x, y):
        return x + y

    with pytest.raises(TypeError):
        foo(1, "2")

    captured = capsys.readouterr()
    expected = "foo - <class 'TypeError'> - args: (1, '2') - kwargs: {}\n"
    assert captured.out == expected


def test_log_success(capsys):
    """Тестирует корректную работу декоратора log
    при успешном выполнении функции."""
    @log(filename="mylog.txt")
    def foo_(x, y):
        return x + y

    result = foo_(1, 2)
    assert result == 3
    captured = capsys.readouterr()
    expected = f"foo_ - {result}\n"
    # Проверяем, что вывод в консоль соответствует ожидаемому результату
    assert captured.out == expected


def test_log_success_file():
    """Проверяет запись успешного результата в файл"""
    file_name = "src/mylog.txt"

    @log(filename="src/mylog.txt")
    def boo(x, y):
        return x + y

    result = boo(1, 2)
    assert result == 3

    with open(file_name, "r", encoding="utf-8") as f:
        content = f.readlines()
        assert content[-1] == "boo - 3\n"


def test_log_multiplecalls(capsys):
    """Проверяет корректность логирования
    при множественных вызовах функции"""
    @log(filename="mylog.txt")
    def roo(x, y):
        return x + y
    roo(1, 2)
    roo(3, 4)
    captured = capsys.readouterr()
    assert captured.out == "roo - 3\nroo - 7\n"


def test_log_no_filename():
    """Тестирует работу декоратора log
    без указания имени файла, с выводом только в консоль."""
    @log(filename=None)
    def goo(x, y):
        return x + y
    assert goo(1, 2) == 3
