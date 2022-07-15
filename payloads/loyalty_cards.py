########################################################################################
# ~ SQUARE MEAL BLOBS FOR API 1
########################################################################################

SQ_JOIN = {
    "account": {
        "enrol_fields": [
            {"column": "First name", "value": "qa"},
            {"column": "Last name", "value": "api2"},
            {"column": "Email", "value": "qatestv2@bink.com"},
            {"column": "Password", "value": "testPswd1"},
            {"column": "Consent 1", "value": "true"},
        ]
    },
    "membership_plan": 324,
}

SQM_ADD_AND_AUTH = {
    "account": {
        "authorise_fields": [
            {"column": "Email", "value": "sCh@testbink.com"},
            {"column": "Password", "value": "Pswd1sm"},
        ]
    },
    "membership_plan": 324,
}

SQM_AUTH_FAIL = {
    "account": {
        "authorise_fields": [
            {"column": "Email", "value": "invalidcredentials"},
            {"column": "Password", "value": "Pswd1sm"},
        ]
    },
    "membership_plan": 324,
}

########################################################################################
# ~ ICELAND BLOBS FOR API 1
########################################################################################

ICELAND_ADD_AND_AUTH_FAIL = {
    "account": {
        "add_fields": [{"column": "Bonus card number", "value": "9999040031231239999"}],
        "authorise_fields": [
            {"column": "Last name", "value": "fronklin"},
            {"column": "Postcode", "value": "BK1 1BK"},
        ],
    },
    "membership_plan": 105,
}

ICELAND_ADD_AND_AUTH = {
    "account": {
        "add_fields": [{"column": "Bonus card number", "value": "9999040031231239999"}],
        "authorise_fields": [
            {"column": "Last name", "value": "Franklin"},
            {"column": "Postcode", "value": "BK1 1BK"},
        ],
    },
    "membership_plan": 105,
}

ICELAND_PATCH_FAIL = {
    "account": {
        "authorise_fields": [
            {"column": "Last name", "value": "Fronklin"},
            {"column": "Postcode", "value": "BK1 1BK"},
        ],
    },
    "membership_plan": 105,
}

ICELAND_PATCH = {
    "account": {
        # "add_fields": [{"column": "Bonus card number", "value": "9999040031231239999"}],
        "authorise_fields": [
            {"column": "Last name", "value": "Franklin"},
            {"column": "Postcode", "value": "BK1 1BK"},
        ],
    },
    "membership_plan": 105,
}

ICELAND_AUTH = {
    "account": {
        "add_fields": [{"column": "Bonus card number", "value": "9999040031231239999"}],
        "authorise_fields": [
            {"column": "Last name", "value": "franklin"},
            {"column": "Postcode", "value": "BK1 1BK"},
        ],
    },
    "membership_plan": 105,
}

ICELAND_AUTH_UPDATED = {
    "account": {
        "add_fields": [{"column": "Bonus card number", "value": "9999040031231239999"}],
        "authorise_fields": [
            {"column": "Last name", "value": "Frenklin"},
            {"column": "Postcode", "value": "AL1 0GD"},
        ],
    },
    "membership_plan": 105,
}

ICELAND_AUTH_FAIL = {
    "account": {
        "add_fields": [{"column": "Bonus card number", "value": "9999040031231239999"}],
        "authorise_fields": [
            {"column": "Last name", "value": "fronklin"},
            {"column": "Postcode", "value": "BK1 1BK"},
        ],
    },
    "membership_plan": 105,
}

ICELAND_AUTH_FAIL_POSTCODE = {
    "account": {
        "add_fields": [{"column": "Bonus card number", "value": "9999040031231239999"}],
        "authorise_fields": [
            {"column": "Last name", "value": "Franklin"},
            {"column": "Postcode", "value": "FAILED"},
        ],
    },
    "membership_plan": 105,
}

ICELAND_ADD = {
    "account": {
        "add_fields": [{"column": "Bonus card number", "value": "9999040031231239999"}],
    },
    "membership_plan": 105,
}

ICELAND_REGISTER = {
    "account": {
        "registration_fields": [
            {"column": "Title", "value": "Mr"},
            {"column": "First name", "value": "Mart"},
            {"column": "Last name", "value": "Binker"},
            {"column": "Date of birth", "value": "29/02/2020"},
            {"column": "Email", "value": "mart@bink.com"},
            {"column": "Phone", "value": "01234555666"},
            {"column": "Postcode", "value": "BK1 1BK"},
            {"column": "House name or number", "value": "999"},
            {"column": "Street name", "value": "Bink Street"},
            {"column": "City", "value": "Great Binkin"},
            {"column": "County", "value": "Binkshire"},
            {"column": "Enrol Consent 1", "value": "true"},
        ]
    },
    "membership_plan": 105,
}

ICELAND_ADD_AND_REGISTER = {
    "account": {
        "add_fields": [{"column": "Bonus card number", "value": "9999040031231239999"}],
        "registration_fields": [
            {"column": "Title", "value": "Mr"},
            {"column": "First name", "value": "Mart"},
            {"column": "Last name", "value": "Binker"},
            {"column": "Date of birth", "value": "31/02/1999"},
            {"column": "Email", "value": "mart@bink.com"},
            {"column": "Phone", "value": "01234555666"},
            {"column": "Postcode", "value": "BK1 1BK"},
            {"column": "House name or number", "value": "999"},
            {"column": "Street name", "value": "Bink Street"},
            {"column": "City", "value": "Great Binkin"},
            {"column": "County", "value": "Binkshire"},
            {"column": "Enrol Consent 1", "value": "true"},
        ],
    },
    "membership_plan": 105,
}

########################################################################################
# Wasabi Add / Auth etc API 1.x
########################################################################################
WASABI_ADD = {
    "account": {
        "add_fields": [{"column": "Membership card number", "value": "12349876"}],
    },
    "membership_plan": 315,
}

WASABI_ADD_AUTH = {
    "account": {
        "add_fields": [{"column": "Membership card number", "value": "12349876"}],
        "authorise_fields": [{"column": "Email", "value": "sucess@bink.com"}],
    },
    "membership_plan": 315,
}

WASABI_ADD_AUTH_FAIL = {
    "account": {
        "add_fields": [{"column": "Membership card number", "value": "12349876"}],
        "authorise_fields": [{"column": "Email", "value": "invalidemail@bink.com"}],
    },
    "membership_plan": 315,
}

# can't do auth without add fields
WASABI_AUTH = {
    "account": {
        "add_fields": [{"column": "Membership card number", "value": "12349876"}],
        "authorise_fields": [{"column": "Email", "value": "sucess@bink.com"}],
    },
    "membership_plan": 315,
}

WASABI_AUTH_UPDATE = {
    "account": {
        "add_fields": [{"column": "Membership card number", "value": "12349876"}],
        "authorise_fields": [{"column": "Email", "value": "updated@bink.com"}],
    },
    "membership_plan": 315,
}

WASABI_AUTH_FAIL = {
    "account": {
        "add_fields": [{"column": "Membership card number", "value": "12349876"}],
        "authorise_fields": [{"column": "Email", "value": "invalidemail@bink.com"}],
    },
    "membership_plan": 315,
}

WASABI_AUTH_FAIL_AGAIN = {
    "account": {
        "add_fields": [{"column": "Membership card number", "value": "12349876"}],
        "authorise_fields": [{"column": "Email", "value": "fail_updated@bink.com"}],
    },
    "membership_plan": 315,
}

########################################################################################
# ~ WASABI BLOBS for API 2
########################################################################################

WASABI_ADD2 = {
    "loyalty_plan_id": 315,
    "account": {
        "add_fields": {
            "credentials": [
                {"credential_slug": "card_number", "value": "9903051973"},
            ]
        }
    },
}

WASABI_ADD_AUTH2 = {
    "loyalty_plan_id": 315,
    "account": {
        "add_fields": {
            "credentials": [
                {"credential_slug": "card_number", "value": "9903051973"},
            ]
        },
        "authorise_fields": {
            "credentials": [
                {"credential_slug": "email", "value": "angie.wasabi@bink.org"},
            ],
        },
    },
}

WASABI_ADD_AUTH2_FAIL = {
    "loyalty_plan_id": 315,
    "account": {
        "add_fields": {
            "credentials": [
                {"credential_slug": "card_number", "value": "9903051973"},
            ]
        },
        "authorise_fields": {
            "credentials": [
                {"credential_slug": "email", "value": "invalidemail@testbink.com"},
            ],
        },
    },
}

WASABI_AUTH2 = {
    "loyalty_plan_id": 315,
    "account": {
        "authorise_fields": {
            "credentials": [
                {"credential_slug": "email", "value": "angie.wasabi@franklin.org"},
            ],
        },
    },
}

########################################################################################
# ~ ICELAND BLOBS FOR API 2
########################################################################################


ICELAND_ADD_AND_REGISTER2 = {
    "account": {
        "add_fields": {
            "credentials": [
                {"credential_slug": "card_number", "value": "7777040000000006991"}
            ]
        },
        "register_ghost_card_fields": {
            "credentials": [
                {"credential_slug": "title", "value": "Mr"},
                {"credential_slug": "first_name", "value": "Joe"},
                {"credential_slug": "last_name", "value": "Holmes"},
                {"credential_slug": "date_of_birth", "value": "01/01/2000"},
                {"credential_slug": "email", "value": "epic.fail@bink.com"},
                {"credential_slug": "phone", "value": "3726421768"},
                {"credential_slug": "address_1", "value": "647"},
                {
                    "credential_slug": "address_2",
                    "value": "3089 Foster Underpass Suite 097",
                },
                {"credential_slug": "town_city", "value": "Annetteside"},
                {"credential_slug": "county", "value": "Bahamas"},
                {"credential_slug": "postcode", "value": "94809"},
            ],
            "consents": [{"consent_slug": "marketing_opt_in", "value": "true"}],
        },
    },
    "loyalty_plan_id": 105,
}

ICELAND_REGISTER2 = {
    "account": {
        "register_ghost_card_fields": {
            "credentials": [
                {"credential_slug": "title", "value": "Mr"},
                {"credential_slug": "first_name", "value": "Joe"},
                {"credential_slug": "last_name", "value": "Holmes"},
                {"credential_slug": "date_of_birth", "value": "01/01/2000"},
                {"credential_slug": "email", "value": "epic.fail@bink.com"},
                {"credential_slug": "phone", "value": "3726421768"},
                {"credential_slug": "address_1", "value": "647"},
                {
                    "credential_slug": "address_2",
                    "value": "3089 Foster Underpass Suite 097",
                },
                {"credential_slug": "town_city", "value": "Annetteside"},
                {"credential_slug": "county", "value": "Bahamas"},
                {"credential_slug": "postcode", "value": "NW107FS"},
            ],
            "consents": [{"consent_slug": "marketing_opt_in", "value": "true"}],
        }
    }
}

ICELAND_ADD2 = {
    "account": {
        "add_fields": {
            "credentials": [
                {"credential_slug": "card_number", "value": "9999040031231239999"}
            ]
        }
    },
    "loyalty_plan_id": 105,
}


ICELAND_ADD_AND_AUTH2 = {
    "account": {
        "add_fields": {
            "credentials": [
                {"credential_slug": "card_number", "value": "9999040031231239999"}
            ]
        },
        "authorise_fields": {
            "credentials": [
                {"credential_slug": "last_name", "value": "Franklin"},
                {"credential_slug": "postcode", "value": "BK1 1BK"},
            ],
        },
    },
    "loyalty_plan_id": 105,
}
ICELAND_ADD_AND_AUTH2_CARD1 = {
    "account": {
        "add_fields": {
            "credentials": [
                {"credential_slug": "card_number", "value": "1111000000000001111"}
            ]
        },
        "authorise_fields": {
            "credentials": [
                {"credential_slug": "last_name", "value": "Franklin"},
                {"credential_slug": "postcode", "value": "BK1 1BK"},
            ],
        },
    },
    "loyalty_plan_id": 105,
}
ICELAND_AUTH2_CARD1 = {
    "account": {
        "add_fields": {
            "credentials": [
                {"credential_slug": "card_number", "value": "1111000000000001111"}
            ]
        },
        "authorise_fields": {
            "credentials": [
                {"credential_slug": "last_name", "value": "Franklin"},
                {"credential_slug": "postcode", "value": "BK1 1BK"},
            ],
        },
    },
}
ICELAND_ADD_AND_AUTH2_CARD2 = {
    "account": {
        "add_fields": {
            "credentials": [
                {"credential_slug": "card_number", "value": "2222000000000002222"}
            ]
        },
        "authorise_fields": {
            "credentials": [
                {"credential_slug": "last_name", "value": "Franklin"},
                {"credential_slug": "postcode", "value": "BK1 1BK"},
            ],
        },
    },
    "loyalty_plan_id": 105,
}

ICELAND_ADD_AND_AUTH2_FAIL = {
    "account": {
        "add_fields": {
            "credentials": [
                {"credential_slug": "card_number", "value": "9999040031231239999"}
            ]
        },
        "authorise_fields": {
            "credentials": [
                {"credential_slug": "last_name", "value": "fronklin"},
                {"credential_slug": "postcode", "value": "BK1 1BK"},
            ],
        },
    },
    "loyalty_plan_id": 105,
}


ICELAND_AUTH2 = {
    "account": {
        "add_fields": {
            "credentials": [
                {"credential_slug": "card_number", "value": "9999040031231239999"}
            ]
        },
        "authorise_fields": {
            "credentials": [
                {"credential_slug": "last_name", "value": "franklin"},
                {"credential_slug": "postcode", "value": "BK1 1BK"},
            ],
        },
    },
}
ICELAND_AUTH2_NEWCARD = {
    "account": {
        "add_fields": {
            "credentials": [
                {"credential_slug": "card_number", "value": "8888040031231238888"}
            ]
        },
        "authorise_fields": {
            "credentials": [
                {"credential_slug": "last_name", "value": "Franklin"},
                {"credential_slug": "postcode", "value": "BK1 1BK"},
            ],
        },
    },
}


ICELAND_AUTH2_UPDATED = {
    "account": {
        "add_fields": {
            "credentials": [
                {"credential_slug": "card_number", "value": "9999040031231239999"}
            ]
        },
        "authorise_fields": {
            "credentials": [
                {"credential_slug": "last_name", "value": "Updated"},
                {"credential_slug": "postcode", "value": "BK1 1BK"},
            ],
        },
    },
}

ICELAND_AUTH2_FAIL = {
    "account": {
        "add_fields": {
            "credentials": [
                {"credential_slug": "card_number", "value": "9999040031231239999"}
            ]
        },
        "authorise_fields": {
            "credentials": [
                {"credential_slug": "last_name", "value": "fronklin"},
                {"credential_slug": "postcode", "value": "BK1 1BK"},
            ],
        },
    },
}

ICELAND_AUTH2_FAIL2 = {
    "account": {
        "add_fields": {
            "credentials": [
                {"credential_slug": "card_number", "value": "9999040031231239999"}
            ]
        },
        "authorise_fields": {
            "credentials": [
                {"credential_slug": "last_name", "value": "fronklin"},
                {"credential_slug": "postcode", "value": "FAILED"},
            ],
        },
    },
}


ICELAND_JOIN2 = {
    "account": {
        "join_fields": {
            "credentials": [
                {"credential_slug": "title", "value": "HRH"},
                {"credential_slug": "first_name", "value": "James"},
                {"credential_slug": "last_name", "value": "Stewart"},
                {"credential_slug": "date_of_birth", "value": "12/12/1066"},
                {"credential_slug": "email", "value": "fail@unknown.com"},
                {"credential_slug": "phone", "value": "01234555666"},
                {"credential_slug": "address_1", "value": "Buckingham"},
                {"credential_slug": "address_2", "value": "Palace"},
                {"credential_slug": "town_city", "value": "London"},
                {"credential_slug": "county", "value": "England"},
                {"credential_slug": "postcode", "value": "BK1 1BK"},
            ],
            "consents": [{"consent_slug": "marketing_opt_in", "value": "true"}],
        }
    },
    "loyalty_plan_id": 105,
}
