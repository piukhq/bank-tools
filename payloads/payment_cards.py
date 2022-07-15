from faker import Faker
fakeit = Faker(locale="en_GB")

#~ POST Bombs

VISA_HAPPY = {
    "expiry_month": "11",
    "expiry_year": "26",
    "name_on_card": "A good Visa",
    "card_nickname": "Super Card",
    "issuer": "Barclays",
    "token": "A_GOOD_TOKEN_NOTHING_WRONG",
    "last_four_digits": "1008",
    "first_six_digits": "444444",
    "fingerprint": fakeit.slug(),
    "type": "debit",
    "country": "GB",
    "currency_code": "GBP",
}


MASTERCARD_HAPPY = {
    "expiry_month": "11",
    "expiry_year": "26",
    "name_on_card": "A good Mastercard",
    "card_nickname": "Super Card",
    "issuer": "Barclays",
    "token": "A_GOOD_TOKEN_NOTHING_WRONG",
    "last_four_digits": "1008",
    "first_six_digits": "222155",
    "fingerprint": fakeit.slug(),
    "type": "debit",
    "country": "GB",
    "currency_code": "GBP",
}


AMEX_HAPPY = {
    "expiry_month": "11",
    "expiry_year": "26",
    "name_on_card": "A good AMEX",
    "card_nickname": "Super Card",
    "issuer": "Barclays",
    "token": "A_GOOD_TOKEN_NOTHING_WRONG",
    "last_four_digits": "1008",
    "first_six_digits": "343434",
    "fingerprint": fakeit.slug(),
    "type": "debit",
    "country": "GB",
    "currency_code": "GBP",
}

#~ PATCH Bombs

PATCHER = {
    "expiry_month": "11",
    "expiry_year": "26",
    "name_on_card": fakeit.name(),
    "card_nickname": f"{fakeit.first_name()}'s Card",
    "issuer": fakeit.company(),
}


if __name__=="__main__":
    # print(VISA_HAPPY)
    # print(MASTERCARD_HAPPY)
    # print(AMEX_HAPPY)
    print(PATCHER)    
