def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки номера банковской карты"""
    result = ""
    if len(card_number) != 16 or card_number.isdigit() is False:
        result = "Введен некорректный номер карты"
    else:
        result = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    return result


print(get_mask_card_number(card_number="7000792289606361"))


def get_mask_account(account_number: str) -> str:
    """Функция маскировки номера банковского счета"""
    result = ""
    if len(account_number) != 20 or account_number.isdigit() is False:
        result = "Введен некорректный номер банковского счета"
    else:
        result = f"** {account_number[-4:]}"
    return result


print(get_mask_account(account_number="12304560789015907530"))
