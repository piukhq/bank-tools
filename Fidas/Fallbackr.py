#
#
# Fallbackr
#
# Fake Midas callbacks to hermes
# (I would NOT use the tkinter GUI!)
#
#

from enum import IntEnum
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Combobox
from tkinter import *
import sys

import requests

HERMES = "http://127.0.0.1:8000"
SERVERS = ["https://api.dev.gb.bink.com", "http://localhost:8000"]


SERVICE_API_KEY = "F616CE5C88744DD52DB628FAD8B3D"


class SchemeAccountStatus:
    PENDING = 0
    ACTIVE = 1
    INVALID_CREDENTIALS = 403
    INVALID_MFA = 432
    END_SITE_DOWN = 530
    IP_BLOCKED = 531
    TRIPPED_CAPTCHA = 532
    INCOMPLETE = 5
    LOCKED_BY_ENDSITE = 434
    RETRY_LIMIT_REACHED = 429
    RESOURCE_LIMIT_REACHED = 503
    UNKNOWN_ERROR = 520
    MIDAS_UNREACHABLE = 9
    AGENT_NOT_FOUND = 404
    WALLET_ONLY = 10
    PASSWORD_EXPIRED = 533
    JOIN = 900
    NO_SUCH_RECORD = 444
    JOIN_IN_PROGRESS = 441
    JOIN_ERROR = 538
    GENERAL_ERROR = 439
    CARD_NUMBER_ERROR = 436
    CARD_NOT_REGISTERED = 438
    LINK_LIMIT_EXCEEDED = 437
    JOIN_ASYNC_IN_PROGRESS = 442
    PRE_REGISTERED_CARD = 406
    ENROL_FAILED = 901
    REGISTRATION_FAILED = 902
    ACCOUNT_ALREADY_EXISTS = 445


class JourneyTypes(IntEnum):
    JOIN = 0
    LINK = 1
    ADD = 2
    UPDATE = 3


def update_status(
    scheme_account_id,
    journey=JourneyTypes.UPDATE,
    status=SchemeAccountStatus.ACTIVE,
    user_info={},
    server=HERMES
):
    print(f"**** Fallbacker called for scheme account {scheme_account_id} ****")

    url = f"{server}/schemes/accounts/{scheme_account_id}/status"
    print(url)

    payload = {"status": status, "journey": journey, "user_info": user_info}

    headers = {
        "Content-type": "application/json",
        "transaction": "success",
        "User-agent": "Midas on localhost",
        "Authorization": "token " + SERVICE_API_KEY,
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    print(f"**** Hermes called for scheme account {scheme_account_id} ****")

    return response.json(), response.status_code


def join_fail(slub, user):
    url = f"{HERMES}/schemes/accounts/join/{slub}/{user}"

    payload = {
        "card_number": None,
        "barcode": "00083",
        "error_codes": [
            {
                "code": "JOIN_ERROR",
                "description": "@JoinMessage = Service.HandleWSJoinResponse - Card join response could not be handled - open join request not found !, @WS_Message = Execution Timeout Expired.  The timeout period elapsed prior to completion of the operation or the server is not responding. - connection stringserver=prddb02.iceland.local;database=customerdata;",
            }
        ],
        "message_uid": "6b86847f-1dd5-4cea-8642-5e8a8cc18e19",
        "record_uid": "z2kog0my1594nk03x896jvqd7lpx3re8",
        "merchant_scheme_id1": "gz91ke80yxp762931xpwqj42ldomvr53",
        "merchant_scheme_id2": "",
        "wallet_uid": None,
    }

    headers = {
        "Content-type": "application/json",
        "transaction": "join_error",
        "User-agent": "Midas on localhost",
        "Authorization": "token " + SERVICE_API_KEY,
    }
    response = requests.request("POST", url, json=payload, headers=headers)

    return response.json()


def join(slub, user):
    url = f"{HERMES}/schemes/accounts/join/{slub}/{user}"

    payload = {"result": "OK", "message": "Callback requested without delay"}

    headers = {
        "Content-type": "application/json",
        "transaction": "success",
        "User-agent": "Midas on localhost",
        "Authorization": "token " + SERVICE_API_KEY,
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return response.json(), response.status_code


class Fallbackr(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Fallbackr")
        self.geometry("600x400")
        
        lf = LabelFrame(self, text="Server")
        lf.pack(fill="x")
        self.server = StringVar()
        server = Combobox(lf, textvariable=self.server, values=SERVERS)
        server.pack(fill="x")
        self.server.set(HERMES)
        
        lf = LabelFrame(self, text="Scheme Account ID")
        lf.pack(fill="x")
        self.scheme_account_id = StringVar()
        server = Entry(lf, textvariable=self.scheme_account_id)
        server.pack(fill="x")
        
        b = Button(self, text="Update Status", command=self.update_status)
        b.pack()

        self.loggee = ScrolledText(self, wrap="none")
        self.loggee.pack(fill="both", expand="yes")
        sys.stdout = self

    def write(self, *stuff):
        for line in stuff:
            self.loggee.insert("end", line+"\n")
        self.loggee.see("end")
    
    def flush(self, *stuff):
        pass

    def update_status(self):
        id = self.scheme_account_id.get()
        server = self.server.get()
        update_status(id, server=server)

if __name__ == "__main__":
    # in your CLIENT code when you perform a PATCH Auth request (for example)
    # and normally Midas sends a request back to Hermes just
    # call update_status with the scheme account id
    # if you want a failed state just pass in an error
    # status e.g.: SchemeAccountStatus.GENERAL_ERROR
    print(update_status(243902))
    # fb = Fallbackr()
    # fb.mainloop()
