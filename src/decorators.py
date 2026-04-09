from typing import Callable, Any, Optional
import functools
import sys
from typing import TextIO


def log(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Декоратор , который  логирует  начало и конец выполнения функции, ее результаты или возникшие ошибки.
    Должен принимать необязательный аргумент 'filename', который определяет,
    куда будут записываться логи (в файл или в консоль)
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            # Определяем, куда выводить логи
            log_output: TextIO = open(filename, "a", encoding="utf-8") if filename else sys.stdout

            try:
                # Логируем начало выполнения
                result = func(*args, **kwargs)
                # Логируем успешное завершение
                print(f"{func.__name__} ok", file=log_output)
                return result
            except Exception as e:
                # Логируем ошибку
                error_type = type(e).__name__
                inputs_positional = str(args)
                inputs_keyword = str(kwargs)
                print(
                    f"{func.__name__} error: {error_type}. " f"Inputs: {inputs_positional}, {inputs_keyword}",
                    file=log_output,
                )
                # Перебрасываем исключение дальше
                raise
            finally:
                # Закрываем файл, если логируем в файл
                if filename:
                    log_output.close()

        return wrapper

    return decorator


@log(filename="mylog.txt")
def my_function(x:int, y:int)->int:
    return x + y


@log()  # Логирование в консоль
def faulty_function(a): #type: ignore
    if a < 0:
        raise ValueError("Negative value not allowed")
    return a**0.5


# Тестируем
my_function(1, 2)  # Успешное выполнение
faulty_function(2)
