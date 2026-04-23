from src.decorators import log
import logging

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/masks.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


@log(filename="mylog.txt")
def get_mask_card_number(card_number: str) -> str:
    logger.info("Ввод номера карты клиента")
    result = ""
    card_number_new = card_number.replace(" ", "").replace("-", "")

    if len(card_number_new) != 16 or card_number_new.isdigit() is False:
        logger.error("Введен некорректный номер карты")
        result = "Введен некорректный номер карты"
    else:
        result = f"{card_number_new[:4]} {card_number_new[4:6]}** **** {card_number_new[-4:]}"
    return result


print(get_mask_card_number(card_number="7000792289606391"))
print(get_mask_card_number(card_number="700079228960639"))


@log(filename="mylog.txt")
def get_mask_account(account_number: str) -> str:
    """Функция маскировки номера банковского счета"""
    logger.info("Ввод номера счета клиента")
    if len(account_number) != 20 or not account_number.isdigit():
        logger.error("Введен некорректный номер банковского счета")
        return "Введён некорректный номер банковского счёта (должно быть 20 цифр)."
    return f"**** **** **** **** {account_number[-4:]}"


print(get_mask_account(account_number="12304560789015907530"))
print(get_mask_account(account_number="123045607890159070"))
