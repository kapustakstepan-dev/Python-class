from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.get('/crypto')
def get_crypto_prices():
    url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    
    try:
        response = requests.get(url)
        data = response.json()
    
        price = {
            'USD': data['bpi']['USD']['rate'],
            'GBP': data['bpi']['GBP']['rate'],
            'EUR': data['bpi']['EUR']['rate']
        }

        return jsonify(price)
    except Exception:
            return jsonify({"error": "Помилка отримання даних"}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)