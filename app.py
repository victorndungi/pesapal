from flask import Flask, request, jsonify
import requests
from utils.constants import base_url, consumer_key, consumer_secret

app = Flask(__name__)

@app.route('/get-pesapal-token', methods=['POST'])
def get_pesapaltoken():
    token_url = "https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken"
    authtokens={
        "consumer_key" : str(consumer_key),
        "consumer_secrets": str(consumer_secret)
    }

    try:
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json"
        }

        response = requests.post(token_url,json=authtokens, headers=headers)
        response.raise_for_status()

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/registerIPNURL', methods=['POST'])
def register_ipn():
    ipn_url = "https://cybqa.pesapal.com/pesapalv3/api/URLSetup/RegisterIPN"

    data = request.get_json()
    session_token = data.get('sessionToken')
    #redirect url: callback url
    redirect_url = "https://friendly-nougat-e4e413.netlify.app/" #simple hosted html page

    ipn_request_payload = {
        "url" : redirect_url,
        "ipn_notification_type": "GET"
    }

    try:
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {session_token}"
        }
        response = requests.post(ipn_url, json = ipn_request_payload, headers=headers)

        response.raise_for_status()
        return jsonify(response.json()), response.status_code


    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000)