from src.decorators import log


@log(filename="mylog.txt")
def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки номера банковской карты"""
    result = ""
    card_number_new = card_number.replace(" ", "").replace("-", "")
    if len(card_number_new) != 16 or card_number_new.isdigit() is False:
        result = "Введен некорректный номер карты"
    else:
        result = f"{card_number_new[:4]} {card_number_new[4:6]}** **** {card_number_new[-4:]}"
    return result


print(get_mask_card_number(card_number="7000792289606361"))


@log(filename="mylog.txt")
def get_mask_account(account_number: str) -> str:
    """Функция маскировки номера банковского счета"""
    if len(account_number) != 20 or not account_number.isdigit():
        return "Введён некорректный номер банковского счёта (должно быть 20 цифр)."
    return f"**** **** **** **** {account_number[-4:]}"


print(get_mask_account(account_number="12304560789015907530"))
