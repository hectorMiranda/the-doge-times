
from flask import Flask, jsonify, request
from flask_caching import Cache
import requests
import os

app = Flask(__name__)
# Configure cache with duration from environment variable
cache_duration = int(os.environ.get('CACHE_DURATION', 60))
cache_config = {
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': cache_duration
}
cache = Cache(app, config=cache_config)

def get_crypto_price(coin):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    response = requests.get(url)
    return response.json()

@app.route('/prices')
@cache.cached(timeout=cache_duration)
def prices():
    bitcoin_price = get_crypto_price('bitcoin')
    dogecoin_price = get_crypto_price('dogecoin')
    return jsonify(bitcoin=bitcoin_price['bitcoin']['usd'], dogecoin=dogecoin_price['dogecoin']['usd'])

@app.route('/flush', methods=['POST'])
def flush_cache():
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.split(' ')[0] == 'Bearer':
        token = auth_header.split(' ')[1]
        if token == os.environ.get('ADMIN_BEARER_TOKEN'):
            cache.clear()
            return jsonify({"success": "Cache cleared"})
    return jsonify({"error": "Unauthorized"}), 403

if __name__ == "__main__":
    app.run(debug=True)
