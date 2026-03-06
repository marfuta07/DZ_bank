from src.masks import get_mask_account, get_mask_card_number

card_number = "1234567894561593"
account_number = "12304560789015907530"
masked_card = get_mask_card_number(card_number)
masked_account = get_mask_account(account_number)

print(f"Замаскированный  номер карты: {masked_card}")
print(f"Замаскированный  номер банковского счета: {masked_account}")

