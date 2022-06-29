#
# Fidas: Fake-Midas
# used to STUB Midas endpoints for local dev testing
#
# M Franklin 2022
#

import time
from flask import Flask, request

from style import *
import Fallbackr


PORT = 8002  # Midas

NOW = int(time.time())
LATER = NOW + (60 * 60 * 24 * 5)
HAPPY = True

# print(f"Is Fidas Happy ? : {HAPPY}")

app = Flask(__name__)

app.happy = HAPPY
app.scheme_ids = []

ICELAND_PAYLOAD = {
        "value": 20.0,
        "pending": None,
        "prefix": "\u00a3",
        "suffix": "",
        "currency": "GBP",
        "updated_at": NOW,
        "description": "Balance from Fidas",
        "reward_tier": 0,
        "vouchers": [],
    }

WASABI_PAYLOAD = {
        "points": 120.0,
        "pending": None,
        "prefix": "\u00a3",
        "suffix": "",
        "currency": "GBP",
        "updated_at": NOW,
        "description": "Balance from Fidas",
        "reward_tier": 0,
        "vouchers": [],
    }




# @app.route("/<scheme>/account_overview", methods=["GET"])
# def midas_account_overview(scheme: str):
#     print("**** account_overview called ****")
#     print("Scheme Name:- ", scheme)
#     print(request.args)


# @app.route("/<scheme>/transactions", methods=["GET"])
# def midas_transactions(scheme: str):
#     print("**** transactions called ****")
#     print("Scheme Name:- ", scheme)
#     print(request.args)


# @app.route("/<scheme>/register", methods=["GET"])
# def midas_register(scheme: str):
#     print("**** register called ****")
#     print("Scheme Name:- ", scheme)
#     print(request.args)


# @app.route("/<scheme>/join", methods=["GET"])
# def midas_join(scheme: str):
#     print("**** join called ****")
#     print("Scheme Name:- ", scheme)
#     print(request.args)


@app.route("/<scheme>/balance", methods=["GET"])
def midas_balance(scheme: str):
    """
    
    /{scheme-slug}/balance

    response is:
        200, {payload}
        403, "{scheme} : INVALID CREDENTIALS"
        500, "{scheme} : UNSUPPORTED_SCHEME"
    """
    scheme_account_id = request.args.get("scheme_account_id")
    # add this scheme account to fallbackr list
    if scheme_account_id not in app.scheme_ids:
        app.scheme_ids.append(scheme_account_id)
    
    print("**** Midas : balance called ****")

    print(f"***** Is Fidas happy? {app.happy} *****")

    if app.happy:
        if scheme == "wasabi-club":
            return WASABI_PAYLOAD
        elif scheme == "iceland-bonus-card":
            return ICELAND_PAYLOAD
        else:
            return f"{scheme} : unsupported scheme", 500
    else:      
        return f"{scheme} : INVALID_CREDENTIALS", 403


# @app.route("/<scheme>/register", methods=["POST"])
# def midas_register(scheme: str):
#     """
#     Fake the /{scheme}/register end point in Midas called by Hermes
    
#     hermes sends this as JSON POST data
#     {
#         "scheme_account_id": 243690,
#         "credentials": "A3Pv/NdRSoT/Et1M9BEcakl2+2TtzSQ1ctG+WOWte/2MdDLwxrhz76YYAtLTUvZdrpYYXTwh0iZg1emJUMr0oUV7Zcy6XyrkX1sIX6tAC/us1/5RJu1GPaMkQv/IKr06v1Yin5yqBxxo/kpykEc6YdKjN1dTdU30kL0gDrKD9RxQBY3tywjbl3XM9NuqZaUb",
#         "user_id": 40540,
#         "status": 442,
#         "journey_type": 0,
#         "channel": "com.lloyds.api2",
#     }   
#     """
#     # print("Scheme Name:- ", scheme)
#     incoming_payload = request.get_json()
#     # print(incoming_payload["journey_type"])

#     # user_info = {
#     #     "scheme_account_id": incoming_payload["scheme_account_id"], 
#     #     "status": "active", 
#     #     "channel": incoming_payload["channel"]
#     #     }
#     # pprint(user_info)

#     outgoing_payload = {"message":"success"}
#     return outgoing_payload 
    
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    HTML = f"""
    <html>
    
    <h1>Fidas - Endpoint Grabber</h1>
    <h2>You called endpoint:<h2>
    <pre>
        {path}
    </pre>
    </html>
    """
    print(f"You called endpoint : {path}")
    return HEAD + HTML + FOOT


@app.route("/index", methods=["GET"])
def index():
    if app.happy:
        fhap = "Yes"
    else:
        fhap = "Nope"

    HTML = f"""
    <html>
    <nav aria-label="breadcrumb">
    <ol class="breadcrumb">
        <li class="breadcrumb-item active" aria-current="page">Index</li>
    </ol>
    </nav> 
    
    <h1>Fidas - Fake Midas</h1>

    <h2>Is Fidas currently happy...? : {fhap}</h2>

    <p>
    Click <a href="/config">here<a> to make Fidas happy again.
    </p>
    <p>
    Click <a href="/fallbackr">here<a> for a fallbackr
    </p>
    <h2>Example responses:</h2>
    <ul>
    <li><a href="/wasabi-club/balance">wasabi-club</a></li>
    <li><a href="/iceland-bonus-card/balance">iceland-bonus-card</a></li>
    <li><a href="/bad-slug/balance">bad-slug</a></li>
    </ul>    

    <p>
    Visit any other endpoint and Fidas will show you the catch_all response
    </p>
    <a href="/try_it_for_youself">try it for yourself</a>

    </html>
    """
    return HEAD + HTML + FOOT

@app.route("/config", methods=["GET", "POST"])
def config():

    happy_form = request.form.get("HappyFidas")
    if happy_form=="happy":
        app.happy = True
    elif happy_form=="unhappy":
        app.happy = False

    HTML = f"""
<html>    
    <nav aria-label="breadcrumb">
    <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/index">Index</a></li>
        <li class="breadcrumb-item active" aria-current="page">Config</li>
    </ol>
    </nav> 
    <h1>Fidas is happy? : {app.happy}</h1>
    <div class="form-group">
    <form method="post" action="/config">
        <select class="form-control" name="HappyFidas">
            <option value="Please choose an option...">Make A Choice</option>
            <option value="happy">Happy</option>
            <option value="unhappy">Unhappy</option>
        </select>
    <input class="form-control" type="submit" name="submit" value="Submit"/>
    </form>
    </div>
</html>
    """

    return HEAD + HTML + FOOT


@app.route("/fallbackr", methods=["GET", "POST"])
def fallbackr():
    id = request.form.get("scheme_account_id")
    if id:
        Fallbackr.update_status(id)


    id_list = []
    for id in app.scheme_ids:
        id_list.append(f'<li><input class="form-control" type="submit" name="scheme_account_id" value="{id}"/></li>')
    id_list = "\n".join(id_list)

    HTML = f"""
<html>   
    <nav aria-label="breadcrumb">
    <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/index">Index</a></li>
        <li class="breadcrumb-item active" aria-current="page">Fallbackr</li>
    </ol>
    </nav> 
    <h1>Fallbackr</h1>
    <p>
    An in memory list of scheme accounts sent to Fidas /scheme-slug/balance/ endpoint since last (re)start
    click on a scheme account id to see what happens!
    </P
    <div class="form-group">
    <form method="post" action="/fallbackr">
    <ul>
    {id_list}
    </ul>
    </form>
    </div>
</html>
    """

    return HEAD + HTML + FOOT




if __name__ == "__main__":
    print("Visit: http://127.0.0.1:8002/index")
    app.run(host="127.0.0.1", port=PORT, debug=True)
