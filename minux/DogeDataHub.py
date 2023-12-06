from flask import Flask, jsonify, request
from flask_restx import Api, Resource
from flask_caching import Cache
import tweepy
import os
import requests
from datetime import datetime

app = Flask(__name__)
api = Api(app, version='1.0', title='DogeDataHub API',
          description='The doge times microservice.')

# Configure cache
cache_duration = int(os.environ.get('CACHE_DURATION', 300))
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': cache_duration})

# Twitter API setup
bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')
client = tweepy.Client(bearer_token)

ns = api.namespace('', description='DogeDataHub operations')

# Helper function to get cryptocurrency prices
def get_crypto_price(coin):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    response = requests.get(url)
    return response.json()

# Prices endpoint
@ns.route('/prices')
class Prices(Resource):
    @cache.cached(timeout=cache_duration)
    def get(self):
        bitcoin_price = get_crypto_price('bitcoin')
        dogecoin_price = get_crypto_price('dogecoin')
        return jsonify(bitcoin=bitcoin_price['bitcoin']['usd'], dogecoin=dogecoin_price['dogecoin']['usd'])

# Flush cache endpoint
@ns.route('/flush')
class FlushCache(Resource):
    def post(self):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.split(' ')[0] == 'Bearer':
            token = auth_header.split(' ')[1]
            if token == os.environ.get('ADMIN_BEARER_TOKEN'):
                cache.clear()
                return {"message": "Cache cleared"}
        return {"error": "Unauthorized"}, 403

# Dogecoin news endpoint
@ns.route('/dogecoin-news')
class DogecoinNews(Resource):
    @cache.cached(query_string=True)
    def get(self):
        query = "Dogecoin -is:retweet"
        max_results = 10
        next_token = request.args.get('next_token', None)
        pagination_params = {"next_token": next_token} if next_token else {}
        try:
            tweets = client.search_recent_tweets(query=query, max_results=max_results, **pagination_params)
            news = [{'tweet': tweet.text, 'user': tweet.author_id} for tweet in tweets.data]
            meta = tweets.meta
            return {"news": news, "meta": meta}
        except Exception as e:
            return {"error": str(e)}, 500





# Utility function for fetching historical data, news, etc.
def fetch_data(url, params=None):
    response = requests.get(url, params=params)
    return response.json()

@ns.route('/currentPrice')
class CurrentPrice(Resource):
    def get(self):
        # Fetch and return the current price of Dogecoin
        return get_crypto_price('dogecoin')

@ns.route('/priceHistory')
class PriceHistory(Resource):
    def get(self):
        # Extract parameters for date range and time interval
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        interval = request.args.get('interval', 'daily')
        # Fetch and return historical price data
        url = "API_URL_FOR_HISTORICAL_DATA"
        params = {'start_date': start_date, 'end_date': end_date, 'interval': interval}
        return fetch_data(url, params)

@ns.route('/marketCap')
class MarketCap(Resource):
    def get(self):
        # Placeholder for fetching market cap data
        # Replace with actual implementation
        return {"message": "Market Cap data not implemented yet."}

@ns.route('/tradingVolume')
class TradingVolume(Resource):
    def get(self):
        # Placeholder for fetching trading volume data
        # Replace with actual implementation
        return {"message": "Trading Volume data not implemented yet."}

@ns.route('/news')
class News(Resource):
    def get(self):
        # Placeholder for fetching Dogecoin-related news
        # Replace with actual implementation
        return {"message": "News data not implemented yet."}

@ns.route('/exchangeRates')
class ExchangeRates(Resource):
    def get(self):
        # Placeholder for fetching Dogecoin exchange rates
        # Replace with actual implementation
        return {"message": "Exchange Rates data not implemented yet."}

@ns.route('/transactions')
class Transactions(Resource):
    def get(self):
        # Placeholder for fetching Dogecoin transactions data
        # Replace with actual implementation
        return {"message": "Transactions data not implemented yet."}

@ns.route('/networkStats')
class NetworkStats(Resource):
    def get(self):
        # Placeholder for fetching Dogecoin network statistics
        # Replace with actual implementation
        return {"message": "Network Stats data not implemented yet."}

@ns.route('/blockInfo')
class BlockInfo(Resource):
    def get(self):
        # Placeholder for fetching information about Dogecoin blocks
        # Replace with actual implementation
        return {"message": "Block Info data not implemented yet."}

@ns.route('/walletInfo')
class WalletInfo(Resource):
    def get(self):
        # Placeholder for fetching information about Dogecoin wallets
        # Replace with actual implementation
        return {"message": "Wallet Info data not implemented yet."}


if __name__ == '__main__':
    app.run(debug=True)