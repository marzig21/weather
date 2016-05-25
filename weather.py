import flask
from flask import request
from two1.wallet import Wallet
from two1.bitserv.flask import Payment
import requests
import yaml
import json

app = flask.Flask(__name__)
payment = Payment(app, Wallet())


@app.route('/weather')
@payment.required(5000)
def weather():
    latlon = request.args.get('latlon')
    base_url = "https://api.forecast.io/forecast/"
    api_key = "secret-api-key!"
    url = base_url + api_key + "/" + latlon

    response = requests.get(url)

    jcontent = json.loads(response.content.decode('utf-8'))
    currently = jcontent['currently']

    temp = currently['temperature']
    summary = currently['icon']
    precipIntensity = currently['precipIntensity']

    if precipIntensity == 0:
        precipType = "none"
    else:
        precipType = currently['precipType']

    result = {
        "temperature": temp,
        "summary": summary,
        "precipType": precipType,
    }

    return json.dumps(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
