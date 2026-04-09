import pytest

from _pytest.tmpdir import tmp_path

from src.decorators import log

"""Тесты для декоратора log"""
def test_successful_execution_with_filename(tmp_path):
        """Тест успешного выполнения функции с логированием в файл"""
        # Создаём временный файл для логов
        log_file = tmp_path / "test_log.txt"

        @log(filename=str(log_file))
        def test_function(x, y):
            return x + y

        # Вызываем функцию
        result = test_function(3, 5)

        # Проверяем результат
        assert result == 8

        # Читаем файл логов
        with open(log_file, 'r', encoding='utf-8') as f:
            log_content = f.read().strip()

        # Проверяем содержимое лога
        assert log_content == "test_function ok"

def test_successful_execution_console(capsys):
        """Тест успешного выполнения функции с логированием в консоль"""
        @log()
        def another_test_function(a, b, c=10):
            return a * b + c

        # Вызываем функцию
        result = another_test_function(2, 3)

        # Проверяем результат
        assert result == 16

        # Получаем захваченный вывод
        captured = capsys.readouterr()

        # Проверяем вывод в консоль
        assert captured.out.strip() == "another_test_function ok"
        assert captured.err == ""  # Ошибок не должно быть

def test_exception_handling_with_filename(tmp_path):
        """Тест обработки исключения с логированием в файл"""
        log_file = tmp_path / "error_log.txt"

        @log(filename=str(log_file))
        def faulty_function(value):
            if value < 0:
                raise ValueError("Negative value not allowed")
            return value ** 0.5

        # Проверяем, что исключение поднимается
        with pytest.raises(ValueError, match="Negative value not allowed"):
            faulty_function(-5)

        # Читаем файл логов
        with open(log_file, 'r', encoding='utf-8') as f:
            log_content = f.read().strip()

        # Проверяем содержимое лога — учитываем, что позиционные аргументы в кортеже
        expected_log = "faulty_function error: ValueError. Inputs: (-5,), {}"
        assert log_content == expected_log

def test_exception_handling_console(capsys):
        """Тест обработки исключения с логированием в консоль"""
        @log()
        def problematic_function(items):
            return items[100]  # Вызов IndexError

        # Проверяем, что исключение поднимается
        with pytest.raises(IndexError):
            problematic_function([1, 2, 3])

        # Получаем захваченный вывод
        captured = capsys.readouterr()

        # Формируем ожидаемый лог
        expected_log = "problematic_function error: IndexError. Inputs: ([1, 2, 3],), {}"

        # Проверяем вывод в консоль
        assert expected_log in captured.out
        assert captured.err == ""

def test_function_with_keyword_arguments(capsys):
        """Тест функции с именованными аргументами"""
        @log()
        def complex_function(a, b=1, c=2):
            return a + b * c

        # Вызываем с именованными аргументами
        result = complex_function(5, b=3, c=4)

        # Проверяем результат
        assert result == 17

        # Получаем захваченный вывод
        captured = capsys.readouterr()

        # Проверяем лог — должны быть и позиционные, и именованные аргументы
        expected_log = "complex_function ok"
        assert captured.out.strip() == expected_log

def test_multiple_calls_same_function(tmp_path):
        """Тест нескольких вызовов одной функции"""
        log_file = tmp_path / "multiple_calls.txt"

        @log(filename=str(log_file))
        def counter_function(increment):
            counter_function.calls += 1
            return counter_function.calls * increment

        # Инициализируем счётчик
        counter_function.calls = 0

        # Несколько вызовов
        result1 = counter_function(2)
        result2 = counter_function(3)

        # Проверяем результаты
        assert result1 == 2
        assert result2 == 6

        # Читаем файл логов
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]

        # Проверяем, что в логе две записи
        assert len(lines) == 2
        assert lines[0] == "counter_function ok"
        assert lines[1] == "counter_function ok"

def test_empty_arguments_function(capsys):
        """Тест функции без аргументов"""
        @log()
        def no_args_function():
            return "Hello, World!"

        # Вызываем функцию
        result = no_args_function()

        # Проверяем результат
        assert result == "Hello, World!"

        # Получаем захваченный вывод
        captured = capsys.readouterr()

        # Проверяем лог
        assert captured.out.strip() == "no_args_function ok"

def test_decorator_without_arguments(capsys):
        """Тест вызова декоратора без аргументов (корректный синтаксис)"""
        @log ()
        def simple_function():
            return 42

        result = simple_function()
        assert result == 42

        captured = capsys.readouterr()
        assert "simple_function ok" in captured.out

# Вспомогательные функции для дополнительных тестов
def test_file_permissions_error(tmp_path):
    """Тест обработки ошибки доступа к файлу"""
    # Создаём файл и ограничиваем права доступа (только для чтения)
    log_file = tmp_path / "protected.txt"
    log_file.write_text("", encoding='utf-8')
    log_file.chmod(0o444)  # Только чтение

    @log(filename=str(log_file))
    def test_func():
        return "test"

    # Проверяем, что декоратор обрабатывает ошибку доступа к файлу
    with pytest.raises((PermissionError, OSError)):
        test_func()
