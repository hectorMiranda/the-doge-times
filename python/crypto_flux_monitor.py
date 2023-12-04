import requests
from flask import Flask, jsonify

app = Flask(__name__)

def get_crypto_price(coin):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data[coin]['usd']

@app.route('/prices')
def prices():
    bitcoin_price = get_crypto_price('bitcoin')
    dogecoin_price = get_crypto_price('dogecoin')
    return jsonify(bitcoin=bitcoin_price, dogecoin=dogecoin_price)

if __name__ == "__main__":
    app.run(debug=True)
