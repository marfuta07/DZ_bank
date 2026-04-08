from typing import Callable, Any, Optional
import functools
import sys

def log(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Декоратор , который  логирует  начало и конец выполнения функции, ее результаты или возникшие ошибки.
    Должен принимать необязательный аргумент 'filename', который определяет,
    куда будут записываться логи (в файл или в консоль)
    """
    def decorator(func:Callable[..., Any])-> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Определяем, куда выводить логи
            if filename:
                log_output = open(filename, 'a', encoding='utf-8')
            else:
                log_output = sys.stdout

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
                    f"{func.__name__} error: {error_type}. "
                    f"Inputs: {inputs_positional}, {inputs_keyword}",
                    file=log_output
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
def my_function(x, y):
    return x + y
# Тестируем
my_function(1, 2)  # Успешное выполнение

