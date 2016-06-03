import re
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
@payment.required(2000)
def weather():
    if 'latlon' in request.args:
        latlon = request.args.get('latlon')
        
        regex = "^[-]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$"
        if re.match(regex, latlon) is not None:
            base_url = "https://api.forecast.io/forecast/"
            api_key = "secret-api-key"
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
                "latlon": latlon,
                "temperature": temp,
                "summary": summary,
                "precipType": precipType,
            }
        else:
            result = {
                "error": "latlon malformed"
            }

    else:
        result = {
            "error": "latlon missing; add something like this to your call: ?latlon=33,-110"
        }

    return json.dumps(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
