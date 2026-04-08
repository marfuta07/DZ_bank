import functools
import sys

def log(filename=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
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
